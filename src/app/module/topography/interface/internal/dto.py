"""Internal DTOs for the Topography module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating topography metrics."""

    parcel_id: UUID
    polygon: GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving topography metrics by parcel ID."""

    parcel_id: UUID


@dataclass(frozen=True, slots=True)
class TopographyMetricsResult:
    """Result of topography metrics operations."""

    id: UUID
    parcel_id: UUID
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
    "GetMetricsInput",
    "TopographyMetricsResult",
)
