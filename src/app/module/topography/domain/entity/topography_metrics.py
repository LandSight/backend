"""Topography metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError
from app.module.topography.domain.value_object.metric import (
    Area,
    AspectDirection,
    CompactnessIndex,
    Elevation,
    ElongationIndex,
    ParcelId,
    Percentage,
    Perimeter,
    Slope,
    SlopeDistribution,
    SlopePercentiles,
    TopographyMetricsId,
)


if TYPE_CHECKING:
    import datetime


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
    elevation_std : Elevation
        Standard deviation of elevation in meters.
    mean_slope : Slope
        Mean slope in degrees.
    max_slope : Slope
        Maximum slope in degrees.
    slope_percentiles : SlopePercentiles
        Slope values at key percentiles (25, 50, 75, 90).
    slope_distribution : SlopeDistribution
        Slope histogram with 10 bins from 0° to 90°.
    aspect : AspectDirection
        Dominant slope aspect direction.
    south_aspect_percentage : Percentage
        Percentage of area facing south (SE, S, SW).
    area : Area
        Parcel area in square meters.
    perimeter : Perimeter
        Parcel perimeter in meters.
    compactness_index : CompactnessIndex
        Compactness index (4πA/P²), dimensionless.
    elongation_index : ElongationIndex
        Elongation index (width/length), dimensionless.
    created_at : datetime | None
        When these metrics were created (UTC); ``None`` if not yet persisted.
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
        elevation_std: Elevation,
        mean_slope: Slope,
        max_slope: Slope,
        slope_percentiles: SlopePercentiles,
        slope_distribution: SlopeDistribution,
        aspect: AspectDirection,
        south_aspect_percentage: Percentage,
        area: Area,
        perimeter: Perimeter,
        compactness_index: CompactnessIndex,
        elongation_index: ElongationIndex,
        created_at: datetime.datetime | None = None,
    ) -> None:
        self._parcel_id: ParcelId = parcel_id
        self._mean_elevation: Elevation = mean_elevation
        self._max_elevation: Elevation = max_elevation
        self._min_elevation: Elevation = min_elevation
        self._elevation_range: Elevation = elevation_range
        self._elevation_std: Elevation = elevation_std
        self._mean_slope: Slope = mean_slope
        self._max_slope: Slope = max_slope
        self._slope_percentiles: SlopePercentiles = slope_percentiles
        self._slope_distribution: SlopeDistribution = slope_distribution
        self._aspect: AspectDirection = aspect
        self._south_aspect_percentage: Percentage = south_aspect_percentage
        self._area: Area = area
        self._perimeter: Perimeter = perimeter
        self._compactness_index: CompactnessIndex = compactness_index
        self._elongation_index: ElongationIndex = elongation_index
        self._created_at: datetime.datetime | None = created_at

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
    def elevation_std(self) -> Elevation:
        """Standard deviation of elevation in meters."""
        return self._elevation_std

    @property
    def mean_slope(self) -> Slope:
        """Mean slope in degrees."""
        return self._mean_slope

    @property
    def max_slope(self) -> Slope:
        """Maximum slope in degrees."""
        return self._max_slope

    @property
    def slope_percentiles(self) -> SlopePercentiles:
        """Slope values at key percentiles (25, 50, 75, 90)."""
        return self._slope_percentiles

    @property
    def slope_distribution(self) -> SlopeDistribution:
        """Slope histogram with 10 bins from 0° to 90°."""
        return self._slope_distribution

    @property
    def aspect(self) -> AspectDirection:
        """Dominant slope aspect direction."""
        return self._aspect

    @property
    def south_aspect_percentage(self) -> Percentage:
        """Percentage of area facing south (SE, S, SW)."""
        return self._south_aspect_percentage

    @property
    def area(self) -> Area:
        """Parcel area in square meters."""
        return self._area

    @property
    def perimeter(self) -> Perimeter:
        """Parcel perimeter in meters."""
        return self._perimeter

    @property
    def compactness_index(self) -> CompactnessIndex:
        """Compactness index (4πA/P²), dimensionless."""
        return self._compactness_index

    @property
    def elongation_index(self) -> ElongationIndex:
        """Elongation index (width/length), dimensionless."""
        return self._elongation_index

    @property
    def created_at(self) -> datetime.datetime | None:
        """When these metrics were created (UTC)."""
        return self._created_at


__all__ = ("TopographyMetrics",)
