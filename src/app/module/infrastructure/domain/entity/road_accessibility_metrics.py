"""Road accessibility infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity.infrastructure_metrics import InfrastructureMetrics


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Density,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class RoadAccessibilityMetrics(InfrastructureMetrics):
    """Metrics for road accessibility.

    Records the distance to the nearest paved road, the nearest main road and
    the nearest drivable road of any class, plus the road network density within
    the buffer. Maps to the ``parcel_road_accessibility_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        distance_to_paved_road: Distance | None,
        distance_to_main_road: Distance | None,
        distance_to_any_road: Distance | None,
        road_density_1km: Density,
    ) -> None:
        self._distance_to_paved_road: Distance | None = distance_to_paved_road
        self._distance_to_main_road: Distance | None = distance_to_main_road
        self._distance_to_any_road: Distance | None = distance_to_any_road
        self._road_density_1km: Density = road_density_1km

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def distance_to_paved_road(self) -> Distance | None:
        """Distance to the nearest paved road in meters, or ``None`` if none found."""
        return self._distance_to_paved_road

    @property
    def distance_to_main_road(self) -> Distance | None:
        """Distance to the nearest main road in meters, or ``None`` if none found."""
        return self._distance_to_main_road

    @property
    def distance_to_any_road(self) -> Distance | None:
        """Distance to the nearest drivable road in meters, or ``None`` if none found."""
        return self._distance_to_any_road

    @property
    def road_density_1km(self) -> Density:
        """Road network density within the buffer in km/km2."""
        return self._road_density_1km


__all__ = ("RoadAccessibilityMetrics",)
