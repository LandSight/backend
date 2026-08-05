"""Hospital infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity import InfrastructureMetrics


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Count,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class HospitalMetrics(InfrastructureMetrics):
    """Infrastructure metrics for the ``hospitals`` category.

    Maps to the ``parcel_hospital_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        count: Count,
        min_distance_to: Distance | None,
    ) -> None:
        self._count: Count = count
        self._min_distance_to: Distance | None = min_distance_to

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def count(self) -> Count:
        """Number of objects within the buffer."""
        return self._count

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest object in meters, or ``None`` if none found."""
        return self._min_distance_to


__all__ = ("HospitalMetrics",)
