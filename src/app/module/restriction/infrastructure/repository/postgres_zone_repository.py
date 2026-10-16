"""PostgreSQL (PostGIS) zone repository implementation."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Final, override

from sqlalchemy import select, text

from app.module.restriction.application.port import ZoneRepository
from app.module.restriction.domain.value_object import LegalBasis, RestrictionHit, RestrictionKind, ZoneNames
from app.module.restriction.infrastructure.model import ZoneModel
from app.module.shared.domain.value_object import Area, SemanticVersion, Share
from app.platform.database.repository import BaseSQLAlchemyRepository
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.module.shared.application.dto.geojson import GeoJSONPolygon


# A zone counts when it reaches the parcel shrunk by the positional tolerance,
# i.e. deeper than the tolerance into the parcel; a parcel too narrow to shrink
# is tested whole. The overlap is then measured on the whole parcel: zones of
# one kind are clipped to it first and merged afterwards, so the union stays
# parcel-sized however large the source zones are. Areas are measured on the
# spheroid, not in Web Mercator, which inflates them ~4x at 60N.
_OVERLAPS_SQL: Final = text(
    """
    WITH src AS (
        SELECT ST_SetSRID(ST_GeomFromGeoJSON(:geojson), 4326) AS g
    ),
    parcel AS (
        SELECT
            ST_Transform(g, 3857) AS g3857,
            ST_Transform(
                CASE WHEN ST_IsEmpty(core) THEN g ELSE core END,
                3857
            ) AS core3857,
            ST_Area(g::geography) AS area
        FROM (SELECT g, ST_Buffer(g::geography, -CAST(:tolerance_m AS float8))::geometry AS core FROM src) AS s
    ),
    clipped AS (
        SELECT
            z.kind,
            z.name,
            z.legal_basis,
            ST_CollectionExtract(ST_Intersection(z.geom, parcel.g3857), 3) AS g
        FROM restriction.zones AS z, parcel
        WHERE ST_Intersects(z.geom, parcel.core3857)
    )
    SELECT
        clipped.kind,
        array_remove(array_agg(DISTINCT clipped.name), NULL) AS names,
        min(clipped.legal_basis) AS legal_basis,
        ST_Area(ST_Transform(ST_Union(clipped.g), 4326)::geography) AS overlap_area,
        max(parcel.area) AS parcel_area
    FROM clipped, parcel
    WHERE NOT ST_IsEmpty(clipped.g)
    GROUP BY clipped.kind
    """
)


class PostgresZoneRepository(BaseSQLAlchemyRepository, ZoneRepository):
    """Zone repository backed by the ``restriction.zones`` PostGIS table."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._logger = get_logger("app.restriction.repository.zone")

    @override
    async def rules_version(self) -> SemanticVersion | None:
        """See :class:`app.module.restriction.application.port.ZoneRepository.rules_version`."""
        result = await self._session.execute(select(ZoneModel.rules_version).limit(1))
        version = result.scalar_one_or_none()
        return None if version is None else SemanticVersion(version)

    @override
    async def find_overlaps(self, polygon: GeoJSONPolygon, tolerance_m: float) -> list[RestrictionHit]:
        """See :class:`app.module.restriction.application.port.ZoneRepository.find_overlaps`."""
        geojson = json.dumps({"type": "Polygon", "coordinates": polygon.coordinates})
        result = await self._session.execute(_OVERLAPS_SQL, {"geojson": geojson, "tolerance_m": tolerance_m})

        hits: list[RestrictionHit] = []
        for row in result.all():
            if not row.parcel_area:
                continue
            try:
                kind = RestrictionKind(row.kind)
            except ValueError:
                # Zones built by a newer rules file than this code knows.
                self._logger.warning("Skipping unknown restriction zone kind: %s", row.kind)
                continue
            hits.append(
                RestrictionHit(
                    kind=kind,
                    overlap_area=Area(row.overlap_area),
                    overlap_share=Share(min(1.0, row.overlap_area / row.parcel_area)),
                    # Names are context for the report: the first few are enough.
                    zone_names=ZoneNames(tuple(sorted(row.names))[: ZoneNames.MAX_COUNT]),
                    legal_basis=LegalBasis(row.legal_basis),
                )
            )
        return hits


__all__ = ("PostgresZoneRepository",)
