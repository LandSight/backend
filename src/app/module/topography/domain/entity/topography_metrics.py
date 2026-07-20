"""Topography metrics entity."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError
from app.module.topography.domain.value_object import (
    Elevation,
    ParcelId,
    Percentage,
    Slope,
    TopographyMetricsId,
)


class TopographyMetrics(BaseEntity[TopographyMetricsId]):
    """Topography metrics entity.

    Attributes
    ----------
    id : TopographyMetricsId
        Unique identifier for this metrics record.
    parcel_id : ParcelId
        ID of the parcel these metrics belong to.
    mean_elevation : Elevation
        Mean elevation in meters.
    max_elevation : Elevation
        Maximum elevation in meters.
    min_elevation : Elevation
        Minimum elevation in meters.
    elevation_range : Elevation
        Elevation range (max - min) in meters.
    mean_slope : Slope
        Mean slope in degrees.
    max_slope : Slope
        Maximum slope in degrees.
    steep_area_percentage : Percentage
        Percentage of area with slope > 15°.
    """

    _ELEVATION_RANGE_TOLERANCE = 0.01

    def __init__(  # noqa: PLR0913
        self,
        id: TopographyMetricsId,
        parcel_id: ParcelId,
        mean_elevation: Elevation,
        max_elevation: Elevation,
        min_elevation: Elevation,
        elevation_range: Elevation,
        mean_slope: Slope,
        max_slope: Slope,
        steep_area_percentage: Percentage,
    ) -> None:
        self._parcel_id: ParcelId = parcel_id
        self._mean_elevation: Elevation = mean_elevation
        self._max_elevation: Elevation = max_elevation
        self._min_elevation: Elevation = min_elevation
        self._elevation_range: Elevation = elevation_range
        self._mean_slope: Slope = mean_slope
        self._max_slope: Slope = max_slope
        self._steep_area_percentage: Percentage = steep_area_percentage

        super().__init__(id)

    @override
    def _validate(self) -> None:
        # Cross-field invariant: elevation_range must equal max - min
        computed_range = round(self._max_elevation.unwrap() - self._min_elevation.unwrap(), 2)
        if abs(computed_range - self._elevation_range.unwrap()) > self._ELEVATION_RANGE_TOLERANCE:
            message = f"Elevation range ({self._elevation_range.unwrap()}) does not match max - min ({computed_range})."
            raise InvariantViolationError(message)

    @property
    def parcel_id(self) -> ParcelId:
        """ID of the parcel these metrics belong to."""
        return self._parcel_id

    @property
    def mean_elevation(self) -> Elevation:
        """Mean elevation in meters."""
        return self._mean_elevation

    @property
    def max_elevation(self) -> Elevation:
        """Maximum elevation in meters."""
        return self._max_elevation

    @property
    def min_elevation(self) -> Elevation:
        """Minimum elevation in meters."""
        return self._min_elevation

    @property
    def elevation_range(self) -> Elevation:
        """Elevation range (max - min) in meters."""
        return self._elevation_range

    @property
    def mean_slope(self) -> Slope:
        """Mean slope in degrees."""
        return self._mean_slope

    @property
    def max_slope(self) -> Slope:
        """Maximum slope in degrees."""
        return self._max_slope

    @property
    def steep_area_percentage(self) -> Percentage:
        """Percentage of area with slope > 15°."""
        return self._steep_area_percentage


__all__ = ("TopographyMetrics",)
