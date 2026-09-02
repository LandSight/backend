"""DEM metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.topography.domain.value_object.metric import (
        AspectDirection,
        Elevation,
        Percentage,
        Slope,
        SlopeDistribution,
        SlopePercentiles,
    )
    from app.module.topography.domain.value_object.raster import RasterData


class DemMetricsService(ABC):
    """Port for computing topography metrics from DEM raster data.

    Performs slope calculation, zonal statistics, and other
    DEM-derived computations.

    Implementations:
    - :class:`app.module.topography.infrastructure.dem.numpy_dem_metrics_service.NumpyDemMetricsService`
    """

    @abstractmethod
    def calculate_mean_elevation(self, raster: RasterData) -> Elevation:
        """Calculate the mean elevation, ignoring NaN values.

        Parameters
        ----------
        raster : RasterData
            Raster data containing the elevation array.

        Returns
        -------
        Elevation
            Mean elevation in meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_max_elevation(self, raster: RasterData) -> Elevation:
        """Calculate the maximum elevation, ignoring NaN values.

        Parameters
        ----------
        raster : RasterData
            Raster data containing the elevation array.

        Returns
        -------
        Elevation
            Maximum elevation in meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_min_elevation(self, raster: RasterData) -> Elevation:
        """Calculate the minimum elevation, ignoring NaN values.

        Parameters
        ----------
        raster : RasterData
            Raster data containing the elevation array.

        Returns
        -------
        Elevation
            Minimum elevation in meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_elevation_std(self, raster: RasterData) -> Elevation:
        """Calculate the standard deviation of elevation, ignoring NaN values.

        Parameters
        ----------
        raster : RasterData
            Raster data containing the elevation array.

        Returns
        -------
        Elevation
            Standard deviation of elevation in meters.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_mean_slope(self, raster: RasterData) -> Slope:
        """Calculate the mean slope in degrees.

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.

        Returns
        -------
        Slope
            Mean slope in degrees.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_max_slope(self, raster: RasterData) -> Slope:
        """Calculate the maximum slope.

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.

        Returns
        -------
        Slope
            Maximum slope in degrees.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_slope_percentiles(self, raster: RasterData) -> SlopePercentiles:
        """Calculate slope percentiles (25, 50, 75, 90).

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.

        Returns
        -------
        SlopePercentiles
            Slope values at key percentiles.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_slope_distribution(self, raster: RasterData, num_bins: int = 10) -> SlopeDistribution:
        """Calculate slope distribution histogram.

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.
        num_bins : int
            Number of equal-width bins (default: 10).

        Returns
        -------
        SlopeDistribution
            Slope histogram with bins from 0° to 90°.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_dominant_aspect(self, raster: RasterData) -> AspectDirection:
        """Calculate the dominant aspect direction.

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.

        Returns
        -------
        AspectDirection
            Dominant aspect direction (N, NE, E, SE, S, SW, W, NW, or FLAT).
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_south_aspect_percent(self, raster: RasterData) -> Percentage:
        """Calculate the percentage of area facing south (SE, S, SW).

        Only considers cells with non-negligible slope (> 5°).

        Parameters
        ----------
        raster : RasterData
            Raster data containing elevation array and resolution.

        Returns
        -------
        Percentage
            Percentage of south-facing area (0-100).
        """
        raise NotImplementedError


__all__ = ("DemMetricsService",)
