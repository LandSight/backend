"""Water body infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity import InfrastructureMetrics


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Count,
        CoverageRatio,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class WaterBodyMetrics(InfrastructureMetrics):
    """Infrastructure metrics for the ``water_body`` category.

    Maps to the ``parcel_water_body_metrics`` table.
    """

    def __init__(  # noqa: PLR0913
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        count: Count,
        min_distance_to: Distance | None,
        coverage_ratio: CoverageRatio,
    ) -> None:
        self._count: Count = count
        self._min_distance_to: Distance | None = min_distance_to
        self._coverage_ratio: CoverageRatio = coverage_ratio

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def count(self) -> Count:
        """Number of objects within the buffer."""
        return self._count

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest object in meters, or ``None`` if none found."""
        return self._min_distance_to

    @property
    def coverage_ratio(self) -> CoverageRatio:
        """CoverageRatio of water within the buffer."""
        return self._coverage_ratio


__all__ = ("WaterBodyMetrics",)
