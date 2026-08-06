"""Shapely-based buffer zone service implementation."""

from __future__ import annotations

from typing import override

from shapely.geometry import Polygon as ShapelyPolygon

from app.module.infrastructure.application.port import BufferService
from app.module.infrastructure.domain.value_object import Buffer, BufferZone
from app.module.shared.domain.value_object import GeoPoint, Polygon


class ShapelyBufferService(BufferService):
    """Buffer zone service implementation using Shapely."""

    _METERS_PER_DEGREE = 111_320.0

    @override
    def create_zone(self, polygon: Polygon, buffer: Buffer) -> BufferZone:
        """See :class:`app.module.infrastructure.application.port.BufferService.create_zone`."""
        shapely_poly = self._to_shapely(polygon)

        buffer_deg = buffer.unwrap() / self._METERS_PER_DEGREE
        outer_shapely = shapely_poly.buffer(buffer_deg)

        outer = self._from_shapely(outer_shapely)
        inner = polygon

        return BufferZone((outer, inner))

    @staticmethod
    def _to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert a domain Polygon to a Shapely Polygon.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @staticmethod
    def _from_shapely(shapely_poly: ShapelyPolygon) -> Polygon:
        """Convert a Shapely Polygon to a domain Polygon."""
        points = [GeoPoint.create(float(coord[1]), float(coord[0])) for coord in shapely_poly.exterior.coords]
        return Polygon(tuple(points))


__all__ = ("ShapelyBufferService",)
