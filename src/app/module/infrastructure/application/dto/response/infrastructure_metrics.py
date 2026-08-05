"""Infrastructure metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.domain.value_object import Category


@dataclass(frozen=True, slots=True)
class CategoryMetrics:
    """Metrics for a single infrastructure category.

    Attributes
    ----------
    count : int
        Number of objects within the buffer.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class InfrastructureMetricsResponse:
    """Response DTO for infrastructure metrics.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    metrics : dict[Category, CategoryMetrics]
        Computed metrics keyed by infrastructure category.
    """

    parcel_id: UUID
    metrics: dict[Category, CategoryMetrics] = field(default_factory=dict)


__all__ = (
    "CategoryMetrics",
    "InfrastructureMetricsResponse",
)
