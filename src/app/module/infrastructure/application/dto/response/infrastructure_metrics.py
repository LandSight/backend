"""Infrastructure metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.response.category_metrics import CategoryMetricsResponse


@dataclass(frozen=True, slots=True)
class InfrastructureMetricsResponse:
    """Response DTO for infrastructure metrics.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    categories : dict[str, CategoryMetricsResponse]
        Computed metrics keyed by category value; only requested categories
        that produced a result are present.
    """

    parcel_id: UUID
    categories: dict[str, CategoryMetricsResponse] = field(default_factory=dict)


__all__ = ("InfrastructureMetricsResponse",)
