"""Ecology infrastructure metrics entity."""

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
        CoverageRatio,
        Distance,
        InfrastructureMetricsId,
        ParcelId,
    )


class EcologyMetrics(InfrastructureMetrics):
    """Metrics for natural area objects sharing the same shape.

    Covers water bodies, forests and protected areas: each row records the
    object type, the fraction of the buffer they cover, the number of distinct
    (connected) objects, the distance to the nearest one and the distance to the
    nearest large one. Maps to the ``parcel_ecology_metrics`` table.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        object_type: Category,
        coverage_ratio: CoverageRatio,
        count: Count,
        min_distance_to: Distance | None,
        distance_to_large_object: Distance | None,
    ) -> None:
        self._object_type: Category = object_type
        self._coverage_ratio: CoverageRatio = coverage_ratio
        self._count: Count = count
        self._min_distance_to: Distance | None = min_distance_to
        self._distance_to_large_object: Distance | None = distance_to_large_object

        super().__init__(id=id, parcel_id=parcel_id, buffer=buffer)

    @property
    def object_type(self) -> Category:
        """Category of the measured natural object."""
        return self._object_type

    @property
    def coverage_ratio(self) -> CoverageRatio:
        """Fraction of the buffer zone covered by the objects."""
        return self._coverage_ratio

    @property
    def count(self) -> Count:
        """Number of distinct (connected) objects within the buffer."""
        return self._count

    @property
    def min_distance_to(self) -> Distance | None:
        """Distance to the nearest object in meters, or ``None`` if none found."""
        return self._min_distance_to

    @property
    def distance_to_large_object(self) -> Distance | None:
        """Distance to the nearest large object in meters, or ``None`` if none found."""
        return self._distance_to_large_object

    def _validate(self) -> None:
        if family_of(self._object_type) is not MetricFamily.ECOLOGY:
            message = f"EcologyMetrics requires an ecology category, got '{self._object_type}'."
            raise ValidationError(message)


__all__ = ("EcologyMetrics",)
