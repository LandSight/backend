"""Zone repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.restriction.domain.value_object import RestrictionHit
    from app.module.shared.application.dto.geojson import GeoJSONPolygon
    from app.module.shared.domain.value_object import SemanticVersion


class ZoneRepository(ABC):
    """Port for reading the prebuilt restriction zones.

    Implementations:
    - :class:`app.module.restriction.infrastructure.repository.postgres_zone_repository.PostgresZoneRepository`
    """

    @abstractmethod
    async def rules_version(self) -> SemanticVersion | None:
        """Return the version of the zone rules the zones were built with.

        Returns
        -------
        SemanticVersion | None
            The rules version, or ``None`` when no zones are loaded.
        """
        raise NotImplementedError

    @abstractmethod
    async def find_overlaps(self, polygon: GeoJSONPolygon, tolerance_m: float) -> list[RestrictionHit]:
        """Return the zone kinds that overlap the polygon.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            Parcel polygon in WGS 84.
        tolerance_m : float
            A zone counts only when it reaches deeper than this into the
            parcel; the overlap itself is measured on the whole parcel.

        Returns
        -------
        list[RestrictionHit]
            One hit per overlapping zone kind, with overlapping zones merged.
        """
        raise NotImplementedError


__all__ = ("ZoneRepository",)
