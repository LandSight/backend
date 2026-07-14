"""Polygon service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from app.module.parcel.domain.value_object.polygon import Polygon


class PolygonService(ABC):
    """Port for polygon geometry operations.

    Provides GeoJSON conversion, advanced geospatial validation,
    and analysis using external libraries (e.g. Shapely).

    Implementations:
    - :class:`app.module.parcel.infrastructure.geo.shapely_polygon_service.ShapelyPolygonService`
    """

    @abstractmethod
    def to_domain(self, geojson: dict[str, Any]) -> Polygon:
        """Convert a GeoJSON Polygon geometry to a domain Polygon.

        Parameters
        ----------
        geojson : dict[str, Any]
            GeoJSON Polygon geometry.

        Returns
        -------
        Polygon
            Domain polygon value object.

        Raises
        ------
        ValidationError
            If the GeoJSON is malformed or not a Polygon type.
        """
        raise NotImplementedError

    @abstractmethod
    def from_domain(self, polygon: Polygon) -> dict[str, Any]:
        """Convert a domain Polygon to a GeoJSON Polygon geometry dict.

        Parameters
        ----------
        polygon : Polygon
            Domain polygon value object.

        Returns
        -------
        dict[str, Any]
            GeoJSON Polygon geometry.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self, polygon: Polygon) -> None:
        """Validate polygon geometry.

        Checks for:
        - Self-intersections
        - Ring orientation
        - Minimum area threshold
        - Overall geometric validity

        Parameters
        ----------
        polygon : Polygon
            Domain polygon value object to validate.

        Raises
        ------
        InvalidPolygonError
            If the polygon geometry is invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_area(self, polygon: Polygon) -> float:
        """Calculate the area of a polygon in square meters.

        Parameters
        ----------
        polygon : Polygon
            Domain polygon value object.

        Returns
        -------
        float
            Area in square meters.
        """
        raise NotImplementedError


__all__ = ("PolygonService",)
