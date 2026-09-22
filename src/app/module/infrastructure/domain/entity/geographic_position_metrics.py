"""Geographic position infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity.infrastructure_metrics import InfrastructureMetrics


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        CityTier,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class GeographicPositionMetrics(InfrastructureMetrics):
    """Infrastructure metrics for the ``geographic_position`` category.

    Maps to the ``parcel_geographic_position_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        distance_to_major_city: Distance | None,
        city_tier: CityTier,
    ) -> None:
        self._distance_to_major_city: Distance | None = distance_to_major_city
        self._city_tier: CityTier = city_tier

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def distance_to_major_city(self) -> Distance | None:
        """Distance to the nearest major city in meters, or ``None`` if none found."""
        return self._distance_to_major_city

    @property
    def city_tier(self) -> CityTier:
        """Tier of the nearest major city."""
        return self._city_tier


__all__ = ("GeographicPositionMetrics",)
