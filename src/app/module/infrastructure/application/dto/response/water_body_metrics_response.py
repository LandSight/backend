"""Water body metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WaterBodyMetricsResponse:
    """Metrics for the ``water_body`` category.

    Holds raw (primitive) values, as DTOs do not carry value objects.

    Attributes
    ----------
    count : int
        Number of water bodies within the buffer zone.
    min_distance_to : float | None
        Distance to the nearest water body in meters, or ``None`` if none found.
    area : float
        Area of water within the buffer in square meters.
    """

    count: int
    min_distance_to: float | None
    area: float


__all__ = ("WaterBodyMetricsResponse",)
