"""Geographic position infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity.infrastructure_metrics import InfrastructureMetrics


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class GeographicPositionMetrics(InfrastructureMetrics):
    """Infrastructure metrics for the ``geographic_position`` category.

    Records the distance to the nearest settlement of each tier: regional
    center, district center and local settlement. Maps to the
    ``parcel_geographic_position_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        distance_to_regional_center: Distance | None,
        distance_to_district_center: Distance | None,
        distance_to_settlement: Distance | None,
    ) -> None:
        self._distance_to_regional_center: Distance | None = distance_to_regional_center
        self._distance_to_district_center: Distance | None = distance_to_district_center
        self._distance_to_settlement: Distance | None = distance_to_settlement

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def distance_to_regional_center(self) -> Distance | None:
        """Distance to the nearest regional center in meters, or ``None`` if none found."""
        return self._distance_to_regional_center

    @property
    def distance_to_district_center(self) -> Distance | None:
        """Distance to the nearest district center in meters, or ``None`` if none found."""
        return self._distance_to_district_center

    @property
    def distance_to_settlement(self) -> Distance | None:
        """Distance to the nearest local settlement in meters, or ``None`` if none found."""
        return self._distance_to_settlement


__all__ = ("GeographicPositionMetrics",)
