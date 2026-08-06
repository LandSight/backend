"""Internal DTOs for the Infrastructure module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class CategoryRequestInput:
    """Requested infrastructure category with its own buffer radius."""

    category: str
    buffer: int


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating infrastructure metrics."""

    parcel_id: UUID
    polygon: GeoJSONPolygon
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving infrastructure metrics by parcel ID."""

    parcel_id: UUID
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SchoolMetricsResult:
    """Metrics for the ``school`` category."""

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class HospitalMetricsResult:
    """Metrics for the ``hospital`` category."""

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class ShopMetricsResult:
    """Metrics for the ``shop`` category."""

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class TransitStopMetricsResult:
    """Metrics for the ``transit_stop`` category."""

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class WaterBodyMetricsResult:
    """Metrics for the ``water_body`` category."""

    buffer: int
    count: int
    min_distance_to: float | None
    coverage_ratio: float


@dataclass(frozen=True, slots=True)
class InfrastructureMetricsResult:
    """Result of infrastructure metrics operations."""

    parcel_id: UUID
    school: SchoolMetricsResult | None = None
    hospital: HospitalMetricsResult | None = None
    shop: ShopMetricsResult | None = None
    transit_stop: TransitStopMetricsResult | None = None
    water_body: WaterBodyMetricsResult | None = None


@dataclass(frozen=True, slots=True)
class CategoryInfoResult:
    """Information about an available infrastructure category."""

    category: str


__all__ = (
    "CalculateMetricsInput",
    "CategoryInfoResult",
    "CategoryRequestInput",
    "GetMetricsInput",
    "HospitalMetricsResult",
    "InfrastructureMetricsResult",
    "SchoolMetricsResult",
    "ShopMetricsResult",
    "TransitStopMetricsResult",
    "WaterBodyMetricsResult",
)
