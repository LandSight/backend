"""Shapely-based infrastructure metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon

from app.module.infrastructure.application.port import InfrastructureMetricsService
from app.module.infrastructure.domain.value_object import (
    BufferZone,
    Count,
    CoverageRatio,
    Distance,
)
from app.module.shared.domain.value_object import GeoPoint, Polygon


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject


class ShapelyInfrastructureMetricsService(InfrastructureMetricsService):
    """Infrastructure metrics service implementation using Shapely.

    Computes object counts, minimum distances, and coverage ratios from raw
    infrastructure objects using Shapely spatial operations.
    """

    _METERS_PER_DEGREE = 111_320.0

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

        min_distance_deg: float | None = None
        for obj in objects:
            obj_shapely = self._geometry_to_shapely(obj.geometry)
            distance_deg = parcel_shapely.distance(obj_shapely)
            if min_distance_deg is None or distance_deg < min_distance_deg:
                min_distance_deg = distance_deg

        if min_distance_deg is None:
            return None

        return Distance(min_distance_deg * self._METERS_PER_DEGREE)

    @override
    def coverage_ratio(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> CoverageRatio:
        """See :class:`app.module.infrastructure.application.port.InfrastructureMetricsService.coverage_ratio`.

        Computes the fraction of the buffer ring covered by the objects.
        Returns ``0.0`` when the zone has no area or there are no objects.
        """
        outer_shapely = self._polygon_to_shapely(buffer_zone.outer)
        inner_shapely = self._polygon_to_shapely(buffer_zone.inner)

        ring = outer_shapely.difference(inner_shapely)
        ring_area = ring.area
        if ring_area <= 0:
            return CoverageRatio(0.0)

        covered_area = 0.0
        for obj in objects:
            obj_shapely = self._geometry_to_shapely(obj.geometry)
            intersection = ring.intersection(obj_shapely)
            covered_area += intersection.area

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
