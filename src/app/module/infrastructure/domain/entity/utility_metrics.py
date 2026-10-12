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

    Power lines are split by role: transmission lines are a building
    constraint, measured as the clearance from their protection zone, while
    distribution lines are a connection opportunity, measured as a distance.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        utility_type: Category,
        min_distance_to: Distance | None,
        transmission_line_clearance: Distance | None,
        distance_to_distribution_line: Distance | None,
    ) -> None:
        self._utility_type: Category = utility_type
        self._min_distance_to: Distance | None = min_distance_to
        self._transmission_line_clearance: Distance | None = transmission_line_clearance
        self._distance_to_distribution_line: Distance | None = distance_to_distribution_line

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def utility_type(self) -> Category:
        """Category of the measured utility network."""
        return self._utility_type

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest utility network in meters, or ``None`` if none found."""
        return self._min_distance_to

    @property
    def transmission_line_clearance(self) -> Distance | None:
        """Gap between the parcel and the nearest transmission line protection zone in meters.

        Zero when the parcel reaches into a protection zone; ``None`` when no
        transmission line was found within the buffer.
        """
        return self._transmission_line_clearance

    @property
    def distance_to_distribution_line(self) -> Distance | None:
        """Distance to the nearest distribution line in meters, or ``None`` if none found."""
        return self._distance_to_distribution_line

    def _validate(self) -> None:
        if family_of(self._utility_type) is not MetricFamily.UTILITY:
            message = f"UtilityMetrics requires a utility category, got '{self._utility_type}'."
            raise ValidationError(message)


__all__ = ("UtilityMetrics",)
