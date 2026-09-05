"""PostgreSQL (PostGIS) local infrastructure repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import (
    MultiPolygon as ShapelyMultiPolygon,
    Point as ShapelyPoint,
    Polygon as ShapelyPolygon,
)
from sqlalchemy import func, or_, select

from app.module.infrastructure.application.port import LocalInfrastructureRepository
from app.module.infrastructure.domain.entity import InfrastructureObject
from app.module.infrastructure.domain.value_object import (
    BufferZone,
    Category,
    InfrastructureObjectId,
)
from app.module.infrastructure.infrastructure.model import (
    PlanetOsmPointModel,
    PlanetOsmPolygonModel,
)
from app.module.shared.domain.value_object import GeoPoint, Polygon
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from geoalchemy2 import Geometry, WKBElement
    from sqlalchemy.engine import Row
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.elements import ColumnElement


class PostgresLocalInfrastructureRepository(BaseSQLAlchemyRepository, LocalInfrastructureRepository):
    """Local infrastructure repository backed by PostgreSQL with PostGIS.

    Reads raw infrastructure objects from the OSM layers created by
    ``osm2pgsql`` (``planet_osm_point`` and ``planet_osm_polygon``), filtering
    by category and the buffer zone (ring) around a parcel.

    Point-based categories (schools, hospitals, shops, transit stops) are read
    from ``planet_osm_point``; area-based categories (water bodies) are read
    from ``planet_osm_polygon``. OSM layers use SRID 3857, while the buffer
    zone is expressed in SRID 4326, so geometries are transformed on the fly.
    """

    _SRID_OSM = 3857
    _SRID_WGS84 = 4326

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def get_point_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """See :class:`app.module.infrastructure.application.port.LocalInfrastructureRepository.get_point_objects`."""
        ring_3857 = self._build_ring(zone)

        stmt = (
            select(
                PlanetOsmPointModel.osm_id,
                PlanetOsmPointModel.name,
                func.ST_Transform(PlanetOsmPointModel.way, self._SRID_WGS84).label("way_wgs84"),
            )
            .where(self._tag_filter(category, PlanetOsmPointModel))
            .where(func.ST_Intersects(PlanetOsmPointModel.way, ring_3857))
        )
        result = await self._session.execute(stmt)

        return [self._to_domain(row, category) for row in result.all()]

    @override
    async def get_polygon_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """See :class:`app.module.infrastructure.application.port.LocalInfrastructureRepository.get_polygon_objects`."""
        ring_3857 = self._build_ring(zone)

        stmt = (
            select(
                PlanetOsmPolygonModel.osm_id,
                PlanetOsmPolygonModel.name,
                func.ST_Transform(PlanetOsmPolygonModel.way, self._SRID_WGS84).label("way_wgs84"),
            )
            .where(self._tag_filter(category, PlanetOsmPolygonModel))
            .where(func.ST_Intersects(PlanetOsmPolygonModel.way, ring_3857))
        )
        result = await self._session.execute(stmt)

        return [self._to_domain(row, category) for row in result.all()]

    def _build_ring(self, zone: BufferZone) -> object:
        """Build the buffer ring geometry in SRID 3857 from a 4326 buffer zone."""
        outer_wkb = from_shape(self._polygon_to_shapely(zone.outer), srid=self._SRID_WGS84)
        inner_wkb = from_shape(self._polygon_to_shapely(zone.inner), srid=self._SRID_WGS84)

        ring_wgs84 = func.ST_Difference(
            cast("Geometry", outer_wkb),
            cast("Geometry", inner_wkb),
        )
        return func.ST_Transform(ring_wgs84, self._SRID_OSM)

    @staticmethod
    def _tag_filter(
        category: Category,
        model: type[PlanetOsmPointModel] | type[PlanetOsmPolygonModel],
    ) -> ColumnElement[bool]:
        """Build the OSM tag filter expression for a category."""
        tags = model.tags
        if category == Category.SCHOOL:
            return tags["amenity"] == "school"
        if category == Category.HOSPITAL:
            return tags["amenity"] == "hospital"
        if category == Category.SHOP:
            return tags["shop"].isnot(None)
        if category == Category.TRANSIT_STOP:
            return or_(tags["highway"] == "bus_stop", tags["railway"] == "station")
        if category == Category.WATER_BODY:
            return or_(tags["natural"] == "water", tags["waterway"].isnot(None))
        return tags["amenity"].isnot(None)

    @staticmethod
    def _polygon_to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert a domain Polygon to a Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @staticmethod
    def _to_domain(row: Row[tuple[int, str | None, object]], category: Category) -> InfrastructureObject:
        """Convert a raw result row to a domain entity."""
        osm_id, name, way_wgs84 = row

        wkb_element = cast("WKBElement", way_wgs84)
        shapely_geom = to_shape(wkb_element)

        geometry: GeoPoint | Polygon
        if isinstance(shapely_geom, ShapelyPoint):
            geometry = GeoPoint.create(float(shapely_geom.y), float(shapely_geom.x))
        else:
            # Real OSM areas (e.g. water bodies with islands) are MultiPolygons.
            # Fall back to the largest component so the domain Polygon stays valid.
            if isinstance(shapely_geom, ShapelyMultiPolygon):
                shapely_geom = max(shapely_geom.geoms, key=lambda geom: geom.area)
            points = [GeoPoint.create(float(coord[1]), float(coord[0])) for coord in shapely_geom.exterior.coords]
            geometry = Polygon(tuple(points))

        return InfrastructureObject(
            id=InfrastructureObjectId(str(osm_id)),
            category=category,
            geometry=geometry,
            name=name,
        )


__all__ = ("PostgresLocalInfrastructureRepository",)
