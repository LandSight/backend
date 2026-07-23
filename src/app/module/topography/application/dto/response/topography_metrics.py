"""Topography metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class TopographyMetricsResponse:
    """Response DTO for topography metrics.

    Attributes
    ----------
    id : UUID
        Topography metrics identifier.
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    mean_elevation : float
        Mean elevation in meters.
    max_elevation : float
        Maximum elevation in meters.
    min_elevation : float
        Minimum elevation in meters.
    elevation_range : float
        Elevation range (max - min) in meters.
    elevation_std : float
        Standard deviation of elevation in meters.
    mean_slope : float
        Mean slope in degrees.
    max_slope : float
        Maximum slope in degrees.
    slope_percentiles : dict[int, float]
        Slope values at percentiles 25, 50, 75, 90.
    slope_distribution : list[float]
        Slope histogram bins (10 bins, 0-90°).
    aspect : str
        Dominant slope aspect direction (N/NE/E/SE/S/SW/W/NW/FLAT).
    south_aspect_percentage : float
        Percentage of area facing south (SE, S, SW).
    area : float
        Parcel area in square meters.
    perimeter : float
        Parcel perimeter in meters.
    compactness_index : float
        Compactness index (4πA/P²), dimensionless.
    elongation_index : float
        Elongation index (width/length), dimensionless.
    """

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


__all__ = ("TopographyMetricsResponse",)
