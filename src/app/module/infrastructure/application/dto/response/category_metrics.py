"""Category metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SchoolMetricsResponse:
    """Metrics for a ``school`` category.

    Attributes
    ----------
    buffer: int
        Buffer radius in meters around the parcel boundary for this category.
    count : int
        Number of objects within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class HospitalMetricsResponse:
    """Metrics for a ``hospital`` category.

    Attributes
    ----------
    buffer: int
        Buffer radius in meters around the parcel boundary for this category.
    count : int
        Number of objects within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class ShopMetricsResponse:
    """Metrics for a ``shop`` category.

    Attributes
    ----------
    buffer: int
        Buffer radius in meters around the parcel boundary for this category.
    count : int
        Number of objects within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class TransitStopMetricsResponse:
    """Metrics for a ``transit_stop`` category.

    Attributes
    ----------
    buffer: int
        Buffer radius in meters around the parcel boundary for this category.
    count : int
        Number of objects within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    buffer: int
    count: int
    min_distance_to: float | None


@dataclass(frozen=True, slots=True)
class WaterBodyMetricsResponse:
    """Metrics for the ``water_body`` category.

    Holds raw (primitive) values, as DTOs do not carry value objects.

    Attributes
    ----------
    buffer: int
        Buffer radius in meters around the parcel boundary for this category.
    count : int
        Number of water bodies within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest water body in meters, or ``None`` if none found.
    coverage_ratio : float
        Coverage ratio of water within the buffer zone.
    """

    buffer: int
    count: int
    min_distance_to: float | None
    coverage_ratio: float


__all__ = (
    "HospitalMetricsResponse",
    "SchoolMetricsResponse",
    "ShopMetricsResponse",
    "TransitStopMetricsResponse",
    "WaterBodyMetricsResponse",
)
