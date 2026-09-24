"""PostgreSQL (PostGIS) local infrastructure repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast, override

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import (
    LineString as ShapelyLineString,
    MultiLineString as ShapelyMultiLineString,
    MultiPolygon as ShapelyMultiPolygon,
    Point as ShapelyPoint,
    Polygon as ShapelyPolygon,
)
from sqlalchemy import false, func, or_, select

from app.module.infrastructure.application.port import LocalInfrastructureRepository
from app.module.infrastructure.domain.entity import InfrastructureObject
from app.module.infrastructure.domain.value_object import (
    BufferZone,
    Category,
    InfrastructureObjectId,
)
from app.module.infrastructure.infrastructure.model import (
    PlanetOsmLineModel,
    PlanetOsmPointModel,
    PlanetOsmPolygonModel,
)
from app.module.infrastructure.infrastructure.osm_tags import (
    DRIVABLE_ROAD_CLASSES,
    GROCERY_SHOPS,
    POWER_LINE_KINDS,
    RAILWAY_STATION_KINDS,
    SETTLEMENT_PLACES,
)
from app.module.shared.domain.value_object import GeoPoint, LineString, Polygon
from app.module.shared.infrastructure.geo import Srid
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from geoalchemy2 import Geometry, WKBElement
    from sqlalchemy.engine import Row
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.elements import ColumnElement


_SourceKind = Literal["point", "line", "polygon"]

_OsmModel = type[PlanetOsmPointModel] | type[PlanetOsmLineModel] | type[PlanetOsmPolygonModel]


class PostgresLocalInfrastructureRepository(BaseSQLAlchemyRepository, LocalInfrastructureRepository):
    """Local infrastructure repository backed by PostgreSQL with PostGIS.

    Reads raw infrastructure objects from the OSM layers created by
    ``osm2pgsql`` (``planet_osm_point``, ``planet_osm_line`` and
    ``planet_osm_polygon``), filtering by category and the buffer zone (ring)
    around a parcel.

    Point-based categories are read from ``planet_osm_point``, line-based
    categories (roads, power lines, pipelines, rivers) from ``planet_osm_line``,
    and area-based categories (water bodies, forest, protected areas) from
    ``planet_osm_polygon``. OSM layers use Web Mercator, while the buffer zone
    is expressed in WGS 84, so geometries are transformed on the fly.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def get_point_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """See :class:`app.module.infrastructure.application.port.LocalInfrastructureRepository.get_point_objects`."""
        return await self._get_objects(PlanetOsmPointModel, zone, category, "point")

    @override
    async def get_line_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """See :class:`app.module.infrastructure.application.port.LocalInfrastructureRepository.get_line_objects`."""
        return await self._get_objects(PlanetOsmLineModel, zone, category, "line")

    @override
    async def get_polygon_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """See :class:`app.module.infrastructure.application.port.LocalInfrastructureRepository.get_polygon_objects`."""
        return await self._get_objects(PlanetOsmPolygonModel, zone, category, "polygon")

    async def _get_objects(
        self,
        model: _OsmModel,
        zone: BufferZone,
        category: Category,
        source: _SourceKind,
    ) -> list[InfrastructureObject]:
        """Read and convert objects of one OSM layer within the buffer zone."""
        ring_web_mercator = self._build_ring(zone)

        stmt = (
            select(
                model.osm_id,
                model.name,
                func.ST_Transform(model.way, Srid.WGS84.value).label("way_wgs84"),
                model.tags,
            )
            .where(self._tag_filter(category, source, model))
            .where(func.ST_Intersects(model.way, ring_web_mercator))
        )
        result = await self._session.execute(stmt)

        return [self._to_domain(row, category) for row in result.all()]

    def _build_ring(self, zone: BufferZone) -> object:
        """Build the buffer ring geometry in Web Mercator from a WGS 84 buffer zone."""
        outer_wkb = from_shape(self._polygon_to_shapely(zone.outer), srid=Srid.WGS84)
        inner_wkb = from_shape(self._polygon_to_shapely(zone.inner), srid=Srid.WGS84)

        ring_wgs84 = func.ST_Difference(
            cast("Geometry", outer_wkb),
            cast("Geometry", inner_wkb),
        )
        return func.ST_Transform(ring_wgs84, Srid.WEB_MERCATOR.value)

    @staticmethod
    def _tag_filter(  # noqa: PLR0911, PLR0912
        category: Category,
        source: _SourceKind,
        model: _OsmModel,
    ) -> ColumnElement[bool]:
        """Build the OSM tag filter expression for a category and OSM layer."""
        tags = model.tags

        if source == "point":
            if category == Category.HOSPITAL:
                return tags["amenity"] == "hospital"
            if category == Category.GROCERY:
                return tags["shop"].in_(GROCERY_SHOPS)
            if category == Category.BUS_STOP:
                return tags["highway"] == "bus_stop"
            if category == Category.RAILWAY_STATION:
                return tags["railway"].in_(RAILWAY_STATION_KINDS)
            if category == Category.POLICE:
                return tags["amenity"] == "police"
            if category == Category.FIRE_STATION:
                return tags["amenity"] == "fire_station"
            if category == Category.PHARMACY:
                return tags["amenity"] == "pharmacy"
            if category == Category.WATER_SOURCE:
                return or_(
                    tags["amenity"] == "drinking_water",
                    tags["man_made"].in_(("water_well", "water_tap", "water_point")),
                )
            if category == Category.GEOGRAPHIC_POSITION:
                return tags["place"].in_(SETTLEMENT_PLACES)

        if source == "line":
            if category == Category.ROAD_ACCESSIBILITY:
                return tags["highway"].in_(DRIVABLE_ROAD_CLASSES)
            if category == Category.WATER_BODY:
                return tags["waterway"] == "river"
            if category == Category.POWER_LINE:
                return tags["power"].in_(POWER_LINE_KINDS)

        if source == "polygon":
            if category == Category.HOSPITAL:
                return tags["amenity"] == "hospital"
            if category == Category.GROCERY:
                return tags["shop"].in_(GROCERY_SHOPS)
            if category == Category.BUS_STOP:
                return tags["highway"] == "bus_stop"
            if category == Category.RAILWAY_STATION:
                return tags["railway"].in_(RAILWAY_STATION_KINDS)
            if category == Category.POLICE:
                return tags["amenity"] == "police"
            if category == Category.FIRE_STATION:
                return tags["amenity"] == "fire_station"
            if category == Category.PHARMACY:
                return tags["amenity"] == "pharmacy"
            if category == Category.WATER_BODY:
                return or_(tags["natural"] == "water", tags["landuse"] == "reservoir")
            if category == Category.FOREST:
                return or_(tags["landuse"] == "forest", tags["natural"] == "wood")
            if category == Category.PROTECTED_AREA:
                return or_(tags["boundary"] == "protected_area", tags["leisure"] == "nature_reserve")

        return false()

    @staticmethod
    def _polygon_to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert a domain Polygon to a Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @classmethod
    def _to_domain(
        cls, row: Row[tuple[int, str | None, object, dict[str, str] | None]], category: Category
    ) -> InfrastructureObject:
        """Convert a raw result row to a domain entity."""
        osm_id, name, way_wgs84, tags = row

        wkb_element = cast("WKBElement", way_wgs84)
        shapely_geom = to_shape(wkb_element)

        geometry: GeoPoint | LineString | Polygon
        match shapely_geom:
            case ShapelyPoint():
                geometry = GeoPoint.create(float(shapely_geom.y), float(shapely_geom.x))
            case ShapelyLineString() | ShapelyMultiLineString():
                line = cls._largest_line(shapely_geom)
                points = [GeoPoint.create(float(lat), float(lon)) for lon, lat in line.coords]
                geometry = LineString(tuple(points))
            case ShapelyPolygon() | ShapelyMultiPolygon():
                polygon = cls._largest_polygon(shapely_geom)
                points = [GeoPoint.create(float(lat), float(lon)) for lon, lat in polygon.exterior.coords]
                geometry = Polygon(tuple(points))
            case _:
                message = f"Unsupported geometry type: {type(shapely_geom).__name__}."
                raise TypeError(message)

        return InfrastructureObject(
            id=InfrastructureObjectId(str(osm_id)),
            category=category,
            geometry=geometry,
            name=name,
            tags=dict(tags) if tags is not None else None,
        )

    @staticmethod
    def _largest_line(
        geom: ShapelyLineString | ShapelyMultiLineString,
    ) -> ShapelyLineString:
        """Return the longest component of a (multi)line geometry."""
        if isinstance(geom, ShapelyMultiLineString):
            return max(geom.geoms, key=lambda part: part.length)
        return geom

    @staticmethod
    def _largest_polygon(
        geom: ShapelyPolygon | ShapelyMultiPolygon,
    ) -> ShapelyPolygon:
        """Return the largest component of a (multi)polygon geometry."""
        if isinstance(geom, ShapelyMultiPolygon):
            return max(geom.geoms, key=lambda part: part.area)
        return geom


__all__ = ("PostgresLocalInfrastructureRepository",)
