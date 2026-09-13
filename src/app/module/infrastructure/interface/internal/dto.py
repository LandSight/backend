"""Internal DTOs for the Infrastructure module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CategoryRequestInput:
    """Requested infrastructure category with its own buffer radius."""

    category: str
    buffer: int


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating infrastructure metrics."""

    parcel_id: UUID
    current_user_id: UUID
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving infrastructure metrics by parcel ID."""

    parcel_id: UUID
    current_user_id: UUID
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CategoryMetricRefInput:
    """Reference to a specific infrastructure metrics record within a category."""

    category: str
    metrics_id: UUID


@dataclass(frozen=True, slots=True)
class GetMetricsByIdsInput:
    """Input for retrieving specific infrastructure metrics records by their IDs."""

    parcel_id: UUID
    current_user_id: UUID
    metrics: list[CategoryMetricRefInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CategoryInfoResult:
    """Information about an available infrastructure category."""

    category: str


__all__ = (
    "CalculateMetricsInput",
    "CategoryInfoResult",
    "CategoryMetricRefInput",
    "CategoryRequestInput",
    "GetMetricsByIdsInput",
    "GetMetricsInput",
)
