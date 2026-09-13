"""Internal DTOs for the Topography module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
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
class GetParcelMetricsInput:
    """Input for retrieving the topography metrics for a parcel."""

    parcel_id: UUID
    current_user_id: UUID


__all__ = (
    "CalculateMetricsInput",
    "GetMetricsInput",
    "GetParcelMetricsInput",
)
