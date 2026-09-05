"""Shapely-based infrastructure metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
from shapely.ops import unary_union

from app.module.infrastructure.application.port import InfrastructureMetricsService
from app.module.infrastructure.domain.value_object import (
    BufferZone,
    Count,
    CoverageRatio,
    Distance,
)
from app.module.shared.domain.value_object import GeoPoint, Polygon
from app.module.shared.infrastructure.geo.projection import reproject_to, to_local_utm


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject


class ShapelyInfrastructureMetricsService(InfrastructureMetricsService):
    """Infrastructure metrics service using Shapely in a local UTM projection.

    Computes object counts, minimum distances, and coverage ratios from raw
    infrastructure objects. Distances and areas are measured in meters inside a
    local UTM zone derived from the parcel/ring centroid; all projection math is
    delegated to ``pyproj``.
    """

    @override
    def count_objects(self, objects: list[InfrastructureObject]) -> Count:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.count_objects`."""
        return Count(len(objects))

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

        parcel_shapely = self._polygon_to_shapely(parcel_geometry)
        parcel_utm, epsg = to_local_utm(parcel_shapely)

        min_distance_m: float | None = None
        for obj in objects:
            obj_shapely = self._geometry_to_shapely(obj.geometry)
            obj_utm = reproject_to(obj_shapely, epsg)
            distance_m = parcel_utm.distance(obj_utm)
            if min_distance_m is None or distance_m < min_distance_m:
                min_distance_m = distance_m

        if min_distance_m is None:
            return None

        return Distance(min_distance_m)

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
        outer_shapely = self._polygon_to_shapely(buffer_zone.outer)
        inner_shapely = self._polygon_to_shapely(buffer_zone.inner)

        ring = outer_shapely.difference(inner_shapely)
        if ring.is_empty or ring.area <= 0:
            return CoverageRatio(0.0)

        ring_utm, epsg = to_local_utm(ring)
        ring_area = ring_utm.area
        if ring_area <= 0:
            return CoverageRatio(0.0)

        intersections = []
        for obj in objects:
            obj_shapely = self._geometry_to_shapely(obj.geometry)
            obj_utm = reproject_to(obj_shapely, epsg)
            intersection = ring_utm.intersection(obj_utm)
            if not intersection.is_empty:
                intersections.append(intersection)

        if not intersections:
            return CoverageRatio(0.0)

        covered_area = unary_union(intersections).area
        ratio = min(covered_area / ring_area, 1.0)
        return CoverageRatio(ratio)

    @staticmethod
    def _polygon_to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert a domain Polygon to a Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @staticmethod
    def _geometry_to_shapely(geometry: GeoPoint | Polygon) -> ShapelyPoint | ShapelyPolygon:
        """Convert a domain geometry (point or polygon) to a Shapely geometry."""
        if isinstance(geometry, GeoPoint):
            return ShapelyPoint(geometry.longitude.unwrap(), geometry.latitude.unwrap())
        return ShapelyInfrastructureMetricsService._polygon_to_shapely(geometry)


__all__ = ("ShapelyInfrastructureMetricsService",)
