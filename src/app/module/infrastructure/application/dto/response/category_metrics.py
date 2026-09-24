"""Category metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class FacilityMetricsResponse:
    """Metrics for a facility category (school, hospital, grocery, stops)."""

    id: UUID
    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class EcologyMetricsResponse:
    """Metrics for an ecology category (water body, forest, protected area)."""

    id: UUID
    buffer: int
    coverage_ratio: float
    count: int
    min_distance_to: float | None
    distance_to_large_object: float | None


@dataclass(frozen=True, slots=True)
class UtilityMetricsResponse:
    """Metrics for a utility category (power line, gas / water pipeline)."""

    id: UUID
    buffer: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class RoadAccessibilityMetricsResponse:
    """Metrics for the ``road_accessibility`` category."""

    id: UUID
    buffer: int
    distance_to_paved_road: float | None
    distance_to_main_road: float | None
    distance_to_any_road: float | None
    road_density_1km: float


@dataclass(frozen=True, slots=True)
class GeographicPositionMetricsResponse:
    """Metrics for the ``geographic_position`` category."""

    id: UUID
    buffer: int
    distance_to_regional_center: float | None
    distance_to_district_center: float | None
    distance_to_settlement: float | None


# Union of all per-category metrics responses.
CategoryMetricsResponse = (
    FacilityMetricsResponse
    | EcologyMetricsResponse
    | UtilityMetricsResponse
    | RoadAccessibilityMetricsResponse
    | GeographicPositionMetricsResponse
)

__all__ = (
    "CategoryMetricsResponse",
    "EcologyMetricsResponse",
    "FacilityMetricsResponse",
    "GeographicPositionMetricsResponse",
    "RoadAccessibilityMetricsResponse",
    "UtilityMetricsResponse",
)
