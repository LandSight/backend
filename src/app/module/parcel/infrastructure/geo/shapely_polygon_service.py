"""Shapely-based polygon service implementation."""

from __future__ import annotations

from typing import Any, override

from shapely.geometry import Polygon as ShapelyPolygon, mapping, shape
from shapely.validation import explain_validity

from app.module.parcel.application.error import InvalidPolygonError
from app.module.parcel.application.port.polygon_service import PolygonService
from app.module.parcel.domain.value_object.geo_point import GeoPoint
from app.module.parcel.domain.value_object.polygon import Polygon
from app.module.shared.domain.error import ValidationError


class ShapelyPolygonService(PolygonService):
    """Polygon service implementation using Shapely.

    Handles GeoJSON conversion, geometry validation, and spatial analysis
    via the Shapely library.
    """

    @override
    def to_domain(self, geojson: dict[str, Any]) -> Polygon:
        """See :class:`app.module.parcel.application.port.polygon_service.PolygonService.to_domain`."""
        if not isinstance(geojson, dict):
            message = "GeoJSON must be a dict."
            raise ValidationError(message)

        shapely_geom = shape(geojson)

        if shapely_geom.geom_type != "Polygon":
            message = f"Expected Polygon geometry, got '{shapely_geom.geom_type}'."
            raise ValidationError(message)

        points = [GeoPoint.create(float(coord[1]), float(coord[0])) for coord in shapely_geom.exterior.coords]

        return Polygon(tuple(points))

    @override
    def from_domain(self, polygon: Polygon) -> dict[str, Any]:
        """See :class:`app.module.parcel.application.port.polygon_service.PolygonService.from_domain`."""
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]

        shapely_geom = shape(
            {
                "type": "Polygon",
                "coordinates": [coords],
            }
        )

        return mapping(shapely_geom)

    @override
    def validate(self, polygon: Polygon) -> None:
        shapely_geom = self._to_shapely(polygon)

        if not shapely_geom.is_valid:
            reason = explain_validity(shapely_geom)
            raise InvalidPolygonError(reason)

        if not shapely_geom.is_simple:
            reason = "Polygon is not simple (self-intersections detected)."
            raise InvalidPolygonError(reason)

    @override
    def calculate_area(self, polygon: Polygon) -> float:
        shapely_geom = self._to_shapely(polygon)

        area_deg = shapely_geom.area
        area_m2 = area_deg * (111_320**2)

        return area_m2

    def _to_shapely(self, polygon: Polygon) -> ShapelyPolygon:
        """Convert domain Polygon to Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)


__all__ = ("ShapelyPolygonService",)
