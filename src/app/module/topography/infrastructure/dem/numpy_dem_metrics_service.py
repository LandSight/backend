"""NumPy-based DEM metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, override

import numpy as np

from app.module.topography.application.port import DemMetricsService
from app.module.topography.domain.value_object.metric import (
    AspectDirection,
    Elevation,
    Percentage,
    Slope,
    SlopeDistribution,
    SlopePercentiles,
)


if TYPE_CHECKING:
    from app.module.topography.domain.value_object.raster import RasterData


class NumpyDemMetricsService(DemMetricsService):
    """NumPy-based implementation of DEM metrics service.

    Computes slope, zonal statistics, and other DEM-derived metrics
    using pure NumPy operations.

    See :class:`app.module.topography.application.port.DemMetricsService`
    for interface documentation.
    """

    # Aspect direction angle ranges (clockwise from north).
    # Each tuple is (start, end) in degrees, with start inclusive, end exclusive.
    _ASPECT_RANGES: ClassVar[dict[AspectDirection, tuple[float, float]]] = {
        AspectDirection.N: (0.0, 22.5),
        AspectDirection.NE: (22.5, 67.5),
        AspectDirection.E: (67.5, 112.5),
        AspectDirection.SE: (112.5, 157.5),
        AspectDirection.S: (157.5, 202.5),
        AspectDirection.SW: (202.5, 247.5),
        AspectDirection.W: (247.5, 292.5),
        AspectDirection.NW: (292.5, 337.5),
    }
    # North wraps around: 337.5° to 360° (and 0° to 22.5°)
    _ASPECT_NORTH_RANGE: tuple[float, float] = (337.5, 360.0)

    _SOUTH_ASPECT_MIN_SLOPE = 5.0
    _FLAT_SLOPE_THRESHOLD = 1e-10
    _SLOPE_PERCENTILES = (25, 50, 75, 90)

    @override
    def calculate_mean_elevation(self, raster: RasterData) -> Elevation:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_mean_elevation`."""
        data = raster.array._value
        return Elevation(float(np.nanmean(data)))

    @override
    def calculate_max_elevation(self, raster: RasterData) -> Elevation:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_max_elevation`."""
        data = raster.array._value
        return Elevation(float(np.nanmax(data)))

    @override
    def calculate_min_elevation(self, raster: RasterData) -> Elevation:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_min_elevation`."""
        data = raster.array._value
        return Elevation(float(np.nanmin(data)))

    @override
    def calculate_elevation_std(self, raster: RasterData) -> Elevation:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_elevation_std`."""
        data = raster.array._value
        return Elevation(float(np.nanstd(data)))

    @override
    def calculate_mean_slope(self, raster: RasterData) -> Slope:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_mean_slope`."""
        elevation = raster.array._value
        resolution = raster.resolution._value
        slope = self._calculate_slope_array(elevation, resolution)
        return Slope(float(np.nanmean(slope)))

    @override
    def calculate_max_slope(self, raster: RasterData) -> Slope:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_max_slope`."""
        elevation = raster.array._value
        resolution = raster.resolution._value
        slope = self._calculate_slope_array(elevation, resolution)
        return Slope(float(np.nanmax(slope)))

    @override
    def calculate_slope_percentiles(self, raster: RasterData) -> SlopePercentiles:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_slope_percentiles`."""
        elevation = raster.array._value
        resolution = raster.resolution._value
        slope = self._calculate_slope_array(elevation, resolution)

        valid = slope[~np.isnan(slope)]
        if len(valid) == 0:
            percentiles_dict = {Percentage(p): Slope(0.0) for p in self._SLOPE_PERCENTILES}
        else:
            values = np.percentile(valid, self._SLOPE_PERCENTILES, method="linear")
            percentiles_dict = {
                Percentage(p): Slope(float(v)) for p, v in zip(self._SLOPE_PERCENTILES, values, strict=False)
            }

        return SlopePercentiles(percentiles_dict)

    @override
    def calculate_slope_distribution(self, raster: RasterData, num_bins: int = 10) -> SlopeDistribution:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_slope_distribution`."""
        elevation = raster.array._value
        resolution = raster.resolution._value
        slope = self._calculate_slope_array(elevation, resolution)

        valid = slope[~np.isnan(slope)]
        if len(valid) == 0:
            return SlopeDistribution([Percentage(0.0)] * num_bins)

        hist, _ = np.histogram(valid, bins=num_bins, range=(0, 90))
        total = float(np.sum(hist))
        if total == 0:
            return SlopeDistribution([Percentage(0.0)] * num_bins)

        percentages = [Percentage(float(h / total * 100)) for h in hist]
        return SlopeDistribution(percentages)

    @override
    def calculate_dominant_aspect(self, raster: RasterData) -> AspectDirection:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_dominant_aspect`."""
        elevation = raster.array._value
        resolution = raster.resolution._value
        aspect = self._calculate_aspect_array(elevation, resolution)
        return self._classify_aspect(aspect)

    @override
    def calculate_south_aspect_percent(self, raster: RasterData) -> Percentage:
        """See :class:`app.module.topography.application.port.DemMetricsService.calculate_south_aspect_percent`."""
        elevation = raster.array._value
        resolution = raster.resolution._value

        slope = self._calculate_slope_array(elevation, resolution)
        aspect = self._calculate_aspect_array(elevation, resolution)

        valid_slope = slope > self._SOUTH_ASPECT_MIN_SLOPE
        valid_aspect = aspect >= 0
        mask = valid_slope & valid_aspect
        total_valid = int(np.sum(mask))

        if total_valid == 0:
            return Percentage(0.0)

        # South-facing: SE (112.5-157.5), S (157.5-202.5), SW (202.5-247.5)
        se_start, _ = self._ASPECT_RANGES[AspectDirection.SE]
        _, sw_end = self._ASPECT_RANGES[AspectDirection.SW]
        south_mask = mask & (aspect >= se_start) & (aspect < sw_end)
        south_count = int(np.sum(south_mask))

        return Percentage(float(south_count / total_valid * 100))

    @staticmethod
    def _calculate_slope_array(elevation: np.ndarray, resolution: float) -> np.ndarray:
        """Calculate slope in degrees using the Horn (1981) algorithm."""
        padded = np.pad(elevation, 1, mode="edge")

        dz_dx = (
            (padded[1:-1, 2:] - padded[1:-1, :-2]) / (2 * resolution)
            + 2 * (padded[2:, 2:] - padded[2:, :-2]) / (2 * resolution)
            + 2 * (padded[:-2, 2:] - padded[:-2, :-2]) / (2 * resolution)
            + (padded[2:, 1:-1] - padded[:-2, 1:-1]) / (2 * resolution)
        ) / 4

        dz_dy = (
            (padded[2:, 1:-1] - padded[:-2, 1:-1]) / (2 * resolution)
            + 2 * (padded[2:, 2:] - padded[:-2, 2:]) / (2 * resolution)
            + 2 * (padded[2:, :-2] - padded[:-2, :-2]) / (2 * resolution)
            + (padded[1:-1, 2:] - padded[1:-1, :-2]) / (2 * resolution)
        ) / 4

        slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
        return np.degrees(slope_rad)

    def _calculate_aspect_array(self, elevation: np.ndarray, resolution: float) -> np.ndarray:
        """Calculate aspect in degrees using the Horn (1981) algorithm.

        Flat areas (slope ≈ 0) are assigned -1.
        """
        padded = np.pad(elevation, 1, mode="edge")

        dz_dx = (
            (padded[1:-1, 2:] - padded[1:-1, :-2]) / (2 * resolution)
            + 2 * (padded[2:, 2:] - padded[2:, :-2]) / (2 * resolution)
            + 2 * (padded[:-2, 2:] - padded[:-2, :-2]) / (2 * resolution)
            + (padded[2:, 1:-1] - padded[:-2, 1:-1]) / (2 * resolution)
        ) / 4

        dz_dy = (
            (padded[2:, 1:-1] - padded[:-2, 1:-1]) / (2 * resolution)
            + 2 * (padded[2:, 2:] - padded[:-2, 2:]) / (2 * resolution)
            + 2 * (padded[2:, :-2] - padded[:-2, :-2]) / (2 * resolution)
            + (padded[1:-1, 2:] - padded[1:-1, :-2]) / (2 * resolution)
        ) / 4

        aspect_rad = np.arctan2(dz_dy, -dz_dx)
        aspect_deg = np.degrees(aspect_rad)
        aspect_deg = np.where(aspect_deg < 0, aspect_deg + 360, aspect_deg)

        # Flat areas: where both dz_dx and dz_dy are near zero
        slope = np.sqrt(dz_dx**2 + dz_dy**2)
        aspect_deg = np.where(slope < self._FLAT_SLOPE_THRESHOLD, -1.0, aspect_deg)

        return aspect_deg

    def _classify_aspect(self, aspect_array: np.ndarray) -> AspectDirection:
        """Classify the dominant aspect direction from an aspect array.

        Returns the most common aspect direction, excluding flat areas.
        """
        flat_mask = aspect_array < 0
        valid = aspect_array[~flat_mask]

        if len(valid) == 0:
            return AspectDirection.FLAT

        counts: dict[AspectDirection, int] = {}
        for direction, (start, end) in self._ASPECT_RANGES.items():
            if direction == AspectDirection.N:
                # North wraps around: [337.5, 360) U [0, 22.5)
                count = int(np.sum((valid >= start) & (valid < end)))
                count += int(np.sum((valid >= self._ASPECT_NORTH_RANGE[0]) & (valid < self._ASPECT_NORTH_RANGE[1])))
            else:
                count = int(np.sum((valid >= start) & (valid < end)))
            counts[direction] = count

        return max(counts, key=counts.__getitem__)  # type: ignore[arg-type]


__all__ = ("NumpyDemMetricsService",)
