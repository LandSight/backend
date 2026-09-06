"""Internal DTOs for the Climate module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating climate metrics."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving a specific climate metrics snapshot by its ID."""

    metrics_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetParcelMetricsInput:
    """Input for retrieving the climate metrics for a parcel."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ClimateMetricsResult:
    """Result of climate metrics operations."""

    id: UUID
    parcel_id: UUID
    created_at: datetime.datetime | None
    mean_annual_temperature: float
    annual_precipitation: float
    temperature_seasonality: float
    precipitation_seasonality: float
    max_temperature_warmest_month: float
    min_temperature_coldest_month: float
    precipitation_wettest_month: float
    precipitation_driest_month: float


__all__ = (
    "CalculateMetricsInput",
    "ClimateMetricsResult",
    "GetMetricsInput",
    "GetParcelMetricsInput",
)
