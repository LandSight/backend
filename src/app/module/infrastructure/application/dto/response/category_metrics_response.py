"""Category metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryMetricsResponse:
    """Metrics for a single infrastructure category.

    Attributes
    ----------
    count : int
        Number of objects within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest object in meters, or ``None`` if none found.
    """

    count: int
    min_distance_to: float | None


__all__ = ("CategoryMetricsResponse",)
