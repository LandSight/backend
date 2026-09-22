"""Facility infrastructure metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.infrastructure.domain.entity.infrastructure_metrics import InfrastructureMetrics
from app.module.infrastructure.domain.value_object import MetricFamily, family_of
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Category,
        Count,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class FacilityMetrics(InfrastructureMetrics):
    """Metrics for point facilities sharing the same shape.

    Covers schools, hospitals, grocery shops, bus stops and railway stations:
    each row records the facility type, the number of objects in the buffer and
    the distance to the nearest one. Maps to the ``parcel_facility_metrics``
    table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        facility_type: Category,
        count: Count,
        min_distance_to: Distance | None,
    ) -> None:
        self._facility_type: Category = facility_type
        self._count: Count = count
        self._min_distance_to: Distance | None = min_distance_to

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def facility_type(self) -> Category:
        """Category of the measured facility."""
        return self._facility_type

    @property
    def count(self) -> Count:
        """Number of facility objects within the buffer."""
        return self._count

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest facility in meters, or ``None`` if none found."""
        return self._min_distance_to

    def _validate(self) -> None:
        if family_of(self._facility_type) is not MetricFamily.FACILITY:
            message = f"FacilityMetrics requires a facility category, got '{self._facility_type}'."
            raise ValidationError(message)


__all__ = ("FacilityMetrics",)
