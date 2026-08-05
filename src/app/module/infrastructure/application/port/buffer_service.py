"""Buffer zone service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import Buffer
    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class BufferService(ABC):
    """Port for building the buffer zone around a parcel.

    The buffer zone is the ring between the parcel boundary and the buffer
    radius, i.e. the buffered polygon with the parcel itself excluded. This
    keeps the search area free of objects that lie inside the parcel.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.geo.shapely_buffer_service.ShapelyBufferService`
    """

    @abstractmethod
    def create_zone(self, polygon: GeoJSONPolygon, buffer: Buffer) -> GeoJSONPolygon:
        """Build the buffer zone (ring) around a parcel.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            Parcel geometry.
        buffer : Buffer
            Buffer radius in meters around the parcel boundary.

        Returns
        -------
        GeoJSONPolygon
            The buffer ring polygon (buffer minus parcel).
        """
        raise NotImplementedError


__all__ = ("BufferService",)
