"""Shapely-based polygon service implementation."""

from __future__ import annotations

from typing import override

from shapely.geometry import Polygon as ShapelyPolygon, mapping
from shapely.validation import explain_validity

from app.module.parcel.application.error import InvalidGeoJsonError, InvalidPolygonError
from app.module.parcel.application.port.polygon_service import PolygonService
from app.module.shared.application.dto.geojson import GeoJSONPolygon
from app.module.shared.domain.value_object import GeoPoint, Polygon


class ShapelyPolygonService(PolygonService):
    """Polygon service implementation using Shapely.

    Handles GeoJSON conversion, geometry validation, and spatial analysis
    via the Shapely library.
    """

    @override
    def to_domain(self, geojson: GeoJSONPolygon) -> Polygon:
        """See :class:`app.module.parcel.application.port.PolygonService.to_domain`."""
        if geojson.type != "Polygon":
            reason = f"Expected Polygon geometry, got '{geojson.type}'"
            raise InvalidGeoJsonError(reason)

        coordinates = geojson.coordinates
        if len(coordinates) == 0:
            reason = "GeoJSON Polygon must have a non-empty coordinates array"
            raise InvalidGeoJsonError(reason)

        ring = coordinates[0]
        if not isinstance(ring, list):
            reason = "GeoJSON Polygon ring must be an array of coordinates"
            raise InvalidGeoJsonError(reason)

        points = [GeoPoint.create(float(coord[1]), float(coord[0])) for coord in ring]

        return Polygon(tuple(points))

    @override
    def from_domain(self, polygon: Polygon) -> GeoJSONPolygon:
        """See :class:`app.module.parcel.application.port.PolygonService.from_domain`."""
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]

        shapely_geom = ShapelyPolygon(coords)
        mapped = mapping(shapely_geom)

        return GeoJSONPolygon(type=mapped["type"], coordinates=mapped["coordinates"])

    @override
    def validate(self, polygon: Polygon) -> None:
        shapely_geom = self._to_shapely(polygon)

        if not shapely_geom.is_valid:
            reason = explain_validity(shapely_geom)
            raise InvalidPolygonError(reason)

        if not shapely_geom.is_simple:
            reason = "Polygon is not simple (self-intersections detected)."
            raise InvalidPolygonError(reason)

    @staticmethod
    def _to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert domain Polygon to Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)


__all__ = ("ShapelyPolygonService",)
