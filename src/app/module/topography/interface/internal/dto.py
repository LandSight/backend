"""Internal DTOs for the Topography module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating topography metrics."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving a specific topography metrics snapshot by its ID."""

    metrics_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetLatestParcelMetricsInput:
    """Input for retrieving the latest topography metrics for a parcel."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ListParcelMetricsInput:
    """Input for listing all topography metrics snapshots for a parcel."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class TopographyMetricsResult:
    """Result of topography metrics operations."""

    id: UUID
    parcel_id: UUID
    created_at: datetime.datetime | None
    mean_elevation: float
    max_elevation: float
    min_elevation: float
    elevation_range: float
    elevation_std: float
    mean_slope: float
    max_slope: float
    slope_percentiles: dict[int, float] = field(default_factory=dict)
    slope_distribution: list[float] = field(default_factory=list)
    aspect: str = ""
    south_aspect_percentage: float = 0.0
    area: float = 0.0
    perimeter: float = 0.0
    compactness_index: float = 0.0
    elongation_index: float = 0.0


__all__ = (
    "CalculateMetricsInput",
    "GetLatestParcelMetricsInput",
    "GetMetricsInput",
    "ListParcelMetricsInput",
    "TopographyMetricsResult",
)
