"""Shapely-based infrastructure metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from shapely.geometry import (
    GeometryCollection,
    LineString as ShapelyLineString,
    MultiLineString as ShapelyMultiLineString,
    MultiPoint as ShapelyMultiPoint,
    MultiPolygon as ShapelyMultiPolygon,
    Point as ShapelyPoint,
    Polygon as ShapelyPolygon,
)
from shapely.ops import unary_union

from app.module.infrastructure.application.port import InfrastructureMetricsService
from app.module.infrastructure.domain.value_object import (
    BufferZone,
    Count,
    CoverageRatio,
    Density,
    Distance,
)
from app.module.shared.domain.value_object import GeoPoint, LineString, Polygon
from app.module.shared.infrastructure.geo.projection import reproject_to, to_local_utm


if TYPE_CHECKING:
    from collections.abc import Iterable

    from app.module.infrastructure.domain.entity import InfrastructureObject


_ShapelyGeometry = (
    ShapelyPoint
    | ShapelyLineString
    | ShapelyMultiLineString
    | ShapelyPolygon
    | ShapelyMultiPolygon
    | ShapelyMultiPoint
    | GeometryCollection
)


class ShapelyInfrastructureMetricsService(InfrastructureMetricsService):
    """Infrastructure metrics service using Shapely in a local UTM projection.

    Computes object counts, minimum distances, coverage ratios and line
    densities from raw infrastructure objects. Distances and areas are measured
    in meters inside a local UTM zone derived from the parcel/ring centroid; all
    projection math is delegated to ``pyproj``.
    """

    _KM_PER_M = 1000.0

    @override
    def count_objects(self, objects: list[InfrastructureObject]) -> Count:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.count_objects`."""
        return Count(len(objects))

    @override
    def count_components(self, objects: list[InfrastructureObject]) -> Count:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.count_components`."""
        if not objects:
            return Count(0)

        geoms, _ = self._reproject_all(objects)
        merged = unary_union(geoms)
        return Count(len(self._components(merged)))

    @override
    def min_distance(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> Distance | None:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.min_distance`.

        Returns ``None`` when there are no objects to measure against.
        """
        if not objects:
            return None

        parcel_utm, epsg = to_local_utm(self._polygon_to_shapely(parcel_geometry))

        min_distance_m: float | None = None
        for obj in objects:
            obj_utm = reproject_to(self._geometry_to_shapely(obj.geometry), epsg)
            distance_m = parcel_utm.distance(obj_utm)
            if min_distance_m is None or distance_m < min_distance_m:
                min_distance_m = distance_m

        if min_distance_m is None:
            return None

        return Distance(min_distance_m)

    @override
    def nearest_object(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> InfrastructureObject | None:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.nearest_object`."""
        if not objects:
            return None

        parcel_utm, epsg = to_local_utm(self._polygon_to_shapely(parcel_geometry))

        nearest: InfrastructureObject | None = None
        nearest_distance: float | None = None
        for obj in objects:
            obj_utm = reproject_to(self._geometry_to_shapely(obj.geometry), epsg)
            distance_m = parcel_utm.distance(obj_utm)
            if nearest_distance is None or distance_m < nearest_distance:
                nearest = obj
                nearest_distance = distance_m

        return nearest

    @override
    def coverage_ratio(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> CoverageRatio:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.coverage_ratio`.

        Computes the fraction of the buffer ring covered by the objects. The
        covered area is the area of the *union* of the individual intersections
        so overlapping objects are not double-counted. Returns ``0.0`` when the
        zone has no area or there are no objects.
        """
        ring = self._ring(buffer_zone)
        if ring is None:
            return CoverageRatio(0.0)

        ring_utm, epsg = to_local_utm(ring)
        ring_area = ring_utm.area
        if ring_area <= 0:
            return CoverageRatio(0.0)

        intersections = []
        for obj in objects:
            obj_utm = reproject_to(self._geometry_to_shapely(obj.geometry), epsg)
            intersection = ring_utm.intersection(obj_utm)
            if not intersection.is_empty:
                intersections.append(intersection)

        if not intersections:
            return CoverageRatio(0.0)

        covered_area = unary_union(intersections).area
        return CoverageRatio(min(covered_area / ring_area, 1.0))

    @override
    def line_density(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> Density:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.line_density`.

        Sums the length of the objects clipped to the buffer ring and divides it
        by the ring area, yielding kilometres of line per square kilometre.
        Returns ``0.0`` when the zone has no area or there are no objects.
        """
        ring = self._ring(buffer_zone)
        if ring is None:
            return Density(0.0)

        ring_utm, epsg = to_local_utm(ring)
        ring_area = ring_utm.area
        if ring_area <= 0:
            return Density(0.0)

        total_length_m = 0.0
        for obj in objects:
            obj_utm = reproject_to(self._geometry_to_shapely(obj.geometry), epsg)
            clipped = ring_utm.intersection(obj_utm)
            if not clipped.is_empty:
                total_length_m += clipped.length

        density_km_per_km2 = (total_length_m / ring_area) * self._KM_PER_M
        return Density(density_km_per_km2)

    @override
    def min_distance_to_large_object(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
        min_area_m2: float,
        always_large_ids: Iterable[str] = (),
    ) -> Distance | None:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.min_distance_to_large_object`."""
        if not objects:
            return None

        parcel_utm, epsg = to_local_utm(self._polygon_to_shapely(parcel_geometry))
        always_large = set(always_large_ids)

        large_geoms: list[_ShapelyGeometry] = []
        polygon_geoms: list[_ShapelyGeometry] = []
        for obj in objects:
            geom = self._geometry_to_shapely(obj.geometry)
            if not isinstance(geom, ShapelyPolygon) or obj.id.unwrap() in always_large:
                large_geoms.append(reproject_to(geom, epsg))
            else:
                polygon_geoms.append(reproject_to(geom, epsg))

        if polygon_geoms:
            for component in self._components(unary_union(polygon_geoms)):
                if isinstance(component, ShapelyPolygon) and component.area >= min_area_m2:
                    large_geoms.append(component)

        if not large_geoms:
            return None

        return Distance(min(parcel_utm.distance(geom) for geom in large_geoms))

    def _reproject_all(
        self,
        objects: list[InfrastructureObject],
    ) -> tuple[list[_ShapelyGeometry], int]:
        """Reproject every object geometry into one local UTM zone."""
        first_geom = self._geometry_to_shapely(objects[0].geometry)
        _, epsg = to_local_utm(first_geom)
        return [reproject_to(self._geometry_to_shapely(obj.geometry), epsg) for obj in objects], epsg

    @staticmethod
    def _components(geometry: _ShapelyGeometry) -> list[_ShapelyGeometry]:
        """Split a geometry into its non-empty connected parts."""
        if geometry.is_empty:
            return []
        if isinstance(
            geometry,
            (ShapelyPoint, ShapelyLineString, ShapelyPolygon),
        ):
            return [geometry]
        if isinstance(
            geometry,
            (ShapelyMultiPoint, ShapelyMultiLineString, ShapelyMultiPolygon, GeometryCollection),
        ):
            return [part for part in geometry.geoms if not part.is_empty]
        return [geometry]

    @staticmethod
    def _ring(buffer_zone: BufferZone) -> ShapelyPolygon | None:
        """Build the buffer ring as a Shapely geometry, or ``None`` when empty."""
        outer_shapely = ShapelyInfrastructureMetricsService._polygon_to_shapely(buffer_zone.outer)
        inner_shapely = ShapelyInfrastructureMetricsService._polygon_to_shapely(buffer_zone.inner)

        ring = outer_shapely.difference(inner_shapely)
        if ring.is_empty or ring.area <= 0:
            return None
        return ring

    @staticmethod
    def _polygon_to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert a domain Polygon to a Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @staticmethod
    def _geometry_to_shapely(
        geometry: GeoPoint | LineString | Polygon,
    ) -> ShapelyPoint | ShapelyLineString | ShapelyPolygon:
        """Convert a domain geometry to a Shapely geometry."""
        if isinstance(geometry, GeoPoint):
            return ShapelyPoint(geometry.longitude.unwrap(), geometry.latitude.unwrap())
        if isinstance(geometry, LineString):
            coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in geometry.points]
            return ShapelyLineString(coords)
        return ShapelyInfrastructureMetricsService._polygon_to_shapely(geometry)


__all__ = ("ShapelyInfrastructureMetricsService",)
