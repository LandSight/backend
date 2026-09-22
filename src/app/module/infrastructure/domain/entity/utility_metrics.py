"""Utility infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity.infrastructure_metrics import InfrastructureMetrics
from app.module.infrastructure.domain.value_object import MetricFamily, family_of
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Category,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class UtilityMetrics(InfrastructureMetrics):
    """Metrics for utility networks sharing the same shape.

    Covers power lines, gas pipelines and water pipelines: each row records the
    utility type and the distance to the nearest one. Maps to the
    ``parcel_utility_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        utility_type: Category,
        min_distance_to: Distance | None,
    ) -> None:
        self._utility_type: Category = utility_type
        self._min_distance_to: Distance | None = min_distance_to

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def utility_type(self) -> Category:
        """Category of the measured utility network."""
        return self._utility_type

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest utility network in meters, or ``None`` if none found."""
        return self._min_distance_to

    def _validate(self) -> None:
        if family_of(self._utility_type) is not MetricFamily.UTILITY:
            message = f"UtilityMetrics requires a utility category, got '{self._utility_type}'."
            raise ValidationError(message)


__all__ = ("UtilityMetrics",)
