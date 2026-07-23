"""Shapely-based geometry metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import numpy as np
from shapely import Polygon as ShapelyPolygon, area, length, minimum_rotated_rectangle

from app.module.topography.application.port.geometry_metrics_service import GeometryMetricsService


if TYPE_CHECKING:
    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class ShapelyGeometryMetricsService(GeometryMetricsService):
    """Shapely-based implementation of geometry metrics service.

    Computes area, perimeter, compactness, and elongation from
    GeoJSON polygons using Shapely operations.

    See :class:`app.module.topography.application.port.GeometryMetricsService`
    for interface documentation.
    """

    _MIN_MBR_VERTICES = 5

    @override
    def calculate_area(self, polygon: GeoJSONPolygon) -> float:
        """See :class:`app.module.topography.application.port.GeometryMetricsService.calculate_area`."""
        shapely_poly = self._to_shapely(polygon)
        return float(area(shapely_poly))

    @override
    def calculate_perimeter(self, polygon: GeoJSONPolygon) -> float:
        """See :class:`app.module.topography.application.port.GeometryMetricsService.calculate_perimeter`."""
        shapely_poly = self._to_shapely(polygon)
        return float(length(shapely_poly))

    @override
    def calculate_compactness(self, area: float, perimeter: float) -> float:
        """See :class:`app.module.topography.application.port.GeometryMetricsService.calculate_compactness`.

        Returns 0.0 for degenerate cases to avoid division by zero.
        """
        if perimeter <= 0 or area <= 0:
            return 0.0
        return float((4 * np.pi * area) / (perimeter**2))

    @override
    def calculate_elongation(self, polygon: GeoJSONPolygon) -> float:
        """See :class:`app.module.topography.application.port.GeometryMetricsService.calculate_elongation`.

        Uses the minimum bounding rectangle approach.
        Returns 0.0 for empty or degenerate polygons.
        """
        shapely_poly = self._to_shapely(polygon)
        if shapely_poly.is_empty or shapely_poly.area <= 0:
            return 0.0

        mbr = minimum_rotated_rectangle(shapely_poly)
        mbr_coords = list(mbr.exterior.coords)  # type: ignore[union-attr]

        if len(mbr_coords) < self._MIN_MBR_VERTICES:
            return 1.0

        # Calculate side lengths of the MBR
        side1 = np.sqrt(
            (mbr_coords[1][0] - mbr_coords[0][0]) ** 2 + (mbr_coords[1][1] - mbr_coords[0][1]) ** 2,
        )
        side2 = np.sqrt(
            (mbr_coords[2][0] - mbr_coords[1][0]) ** 2 + (mbr_coords[2][1] - mbr_coords[1][1]) ** 2,
        )

        if side1 <= 0 or side2 <= 0:
            return 1.0

        width = min(side1, side2)
        length_val = max(side1, side2)

        return float(width / length_val)

    @staticmethod
    def _to_shapely(polygon: GeoJSONPolygon) -> ShapelyPolygon:
        """Convert a GeoJSONPolygon DTO to a Shapely Polygon."""
        coords = polygon.coordinates[0]
        return ShapelyPolygon(coords)


__all__ = ("ShapelyGeometryMetricsService",)
