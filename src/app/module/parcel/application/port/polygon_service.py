"""Polygon service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.shared.application.dto.geojson import GeoJSONPolygon
    from app.module.shared.domain.value_object import Polygon


class PolygonService(ABC):
    """Port for polygon geometry operations.

    Bridges the shared GeoJSON interchange format (the world-standard wire
    representation used across module boundaries) and the parcel domain
    :class:`~app.module.shared.domain.value_object.Polygon` value object.
    Also provides advanced geospatial validation via external libraries
    (e.g. Shapely).

    Implementations:
    - :class:`app.module.parcel.infrastructure.geo.shapely_polygon_service.ShapelyPolygonService`
    """

    @abstractmethod
    def to_domain(self, geojson: GeoJSONPolygon) -> Polygon:
        """Convert a GeoJSON Polygon geometry to a domain Polygon.

        Parameters
        ----------
        geojson : GeoJSONPolygon
            Typed GeoJSON Polygon geometry.

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
    def from_domain(self, polygon: Polygon) -> GeoJSONPolygon:
        """Convert a domain Polygon to a GeoJSON Polygon geometry.

        Parameters
        ----------
        polygon : Polygon
            Domain polygon value object.

        Returns
        -------
        GeoJSONPolygon
            Typed GeoJSON Polygon geometry.
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


__all__ = ("PolygonService",)
