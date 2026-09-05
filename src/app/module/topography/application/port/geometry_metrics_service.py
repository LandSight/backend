"""Geometry metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.shared.application.dto.geojson import GeoJSONPolygon


class GeometryMetricsService(ABC):
    """Port for computing geometry metrics from parcel polygons.

    Computes area, perimeter, compactness, and elongation from
    a GeoJSON polygon representation.

    Implementations:
    - :class:`app.module.topography.infrastructure.geo.shapely_geometry_metrics_service.ShapelyGeometryMetricsService`
    """

    @abstractmethod
    def calculate_area(self, polygon: GeoJSONPolygon) -> float:
        """Calculate the area of a polygon in square meters.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            Polygon geometry.

        Returns
        -------
        float
            Area in square meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_perimeter(self, polygon: GeoJSONPolygon) -> float:
        """Calculate the perimeter of a polygon in meters.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            Polygon geometry.

        Returns
        -------
        float
            Perimeter in meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_compactness(self, area: float, perimeter: float) -> float:
        """Calculate the compactness index (4πA/P²).

        A perfect circle has compactness = 1.0.
        Lower values indicate more irregular shapes.

        Parameters
        ----------
        area : float
            Area in square meters.
        perimeter : float
            Perimeter in meters.

        Returns
        -------
        float
            Compactness index, dimensionless.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_elongation(self, polygon: GeoJSONPolygon) -> float:
        """Calculate the elongation index (width/length).

        Uses the minimum bounding rectangle approach.
        A perfect square/circle has elongation ≈ 1.0.
        Lower values indicate more elongated shapes.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            Polygon geometry.

        Returns
        -------
        float
            Elongation index, dimensionless (0-1).
        """
        raise NotImplementedError


__all__ = ("GeometryMetricsService",)
