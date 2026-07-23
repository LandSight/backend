"""Calculate topography metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override
from uuid import uuid6

from app.module.shared.application.use_case import BaseUseCase
from app.module.shared.domain.value_object import BoundingBox
from app.module.shared.interface.internal.geojson import GeoJSONPolygon
from app.module.topography.application.dto.command import CalculateTopographyMetricsCommand
from app.module.topography.application.dto.response import TopographyMetricsResponse
from app.module.topography.application.error import DemNotFoundError
from app.module.topography.domain.entity import TopographyMetrics
from app.module.topography.domain.value_object.metric import (
    Area,
    CompactnessIndex,
    Elevation,
    ElongationIndex,
    ParcelId,
    Perimeter,
    TopographyMetricsId,
)
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.topography.application.port import (
        DemMetricsService,
        GeometryMetricsService,
        LocalDemRepository,
        MetricsRepository,
    )


class CalculateTopographyMetricsUseCase(BaseUseCase[CalculateTopographyMetricsCommand, TopographyMetricsResponse]):
    """Calculate topography metrics for a given parcel.

    Downloads DEM data, computes metrics, caches the DEM locally,
    persists the metrics, and returns the result.
    """

    _SLOPE_PERCENTILES: tuple[int, ...] = (25, 50, 75, 90)
    _SLOPE_DISTRIBUTION_BINS = 10

    def __init__(
        self,
        local_dem_repository: LocalDemRepository,
        dem_metrics_service: DemMetricsService,
        geometry_metrics_service: GeometryMetricsService,
        metrics_repository: MetricsRepository,
    ) -> None:
        self._local_dem_repository = local_dem_repository
        self._dem_metrics_service = dem_metrics_service
        self._geometry_metrics_service = geometry_metrics_service
        self._metrics_repository = metrics_repository
        self._logger = get_logger("app.topography.use_case.calculate_topography_metrics")

    @override
    async def __call__(self, command: CalculateTopographyMetricsCommand) -> TopographyMetricsResponse:
        self._logger.info("Calculating topography metrics: parcel_id=%s", command.parcel_id)

        # Calculate bounding box from polygon coordinates
        bounds = self._compute_bounding_box(command.polygon)

        # Check if DEM exists in cache
        if not await self._local_dem_repository.exists(bounds):
            reason = f"There is no data for the requested parcel boundaries: {bounds}"
            raise DemNotFoundError(reason)

        # Get DEM as RasterData (contains data + resolution)
        raster = await self._local_dem_repository.get_elevation_raster(bounds)

        if raster is None:
            reason = f"There is no data for the requested parcel boundaries: {bounds}"
            raise DemNotFoundError(reason)

        # Elevation metrics
        mean_elevation = self._dem_metrics_service.calculate_mean_elevation(raster)
        max_elevation = self._dem_metrics_service.calculate_max_elevation(raster)
        min_elevation = self._dem_metrics_service.calculate_min_elevation(raster)
        elevation_std = self._dem_metrics_service.calculate_elevation_std(raster)

        # Elevation range
        elevation_range = Elevation(max_elevation.unwrap() - min_elevation.unwrap())

        # Slope metrics
        mean_slope = self._dem_metrics_service.calculate_mean_slope(raster)
        max_slope = self._dem_metrics_service.calculate_max_slope(raster)
        slope_percentiles = self._dem_metrics_service.calculate_slope_percentiles(raster)
        slope_distribution = self._dem_metrics_service.calculate_slope_distribution(
            raster, self._SLOPE_DISTRIBUTION_BINS
        )

        # Aspect metrics
        dominant_aspect = self._dem_metrics_service.calculate_dominant_aspect(raster)
        south_aspect_percent = self._dem_metrics_service.calculate_south_aspect_percent(raster)

        # Geometry metrics
        polygon = GeoJSONPolygon(
            type=command.polygon["type"],
            coordinates=command.polygon["coordinates"],
        )
        area = self._geometry_metrics_service.calculate_area(polygon)
        perimeter = self._geometry_metrics_service.calculate_perimeter(polygon)
        compactness = self._geometry_metrics_service.calculate_compactness(area, perimeter)
        elongation = self._geometry_metrics_service.calculate_elongation(polygon)

        # Create domain entity
        metrics = TopographyMetrics(
            id=TopographyMetricsId(uuid6()),
            parcel_id=ParcelId(command.parcel_id),
            mean_elevation=mean_elevation,
            max_elevation=max_elevation,
            min_elevation=min_elevation,
            elevation_range=elevation_range,
            elevation_std=elevation_std,
            mean_slope=mean_slope,
            max_slope=max_slope,
            slope_percentiles=slope_percentiles,
            slope_distribution=slope_distribution,
            aspect=dominant_aspect,
            south_aspect_percentage=south_aspect_percent,
            area=Area(area),
            perimeter=Perimeter(perimeter),
            compactness_index=CompactnessIndex(compactness),
            elongation_index=ElongationIndex(elongation),
        )

        await self._metrics_repository.save(metrics)

        self._logger.info("Topography metrics calculated: id=%s parcel_id=%s", metrics.id, command.parcel_id)

        return TopographyMetricsResponse(
            id=metrics.id.unwrap(),
            parcel_id=command.parcel_id,
            mean_elevation=metrics.mean_elevation.unwrap(),
            max_elevation=metrics.max_elevation.unwrap(),
            min_elevation=metrics.min_elevation.unwrap(),
            elevation_range=metrics.elevation_range.unwrap(),
            elevation_std=metrics.elevation_std.unwrap(),
            mean_slope=metrics.mean_slope.unwrap(),
            max_slope=metrics.max_slope.unwrap(),
            slope_percentiles=metrics.slope_percentiles.to_float_dict(),
            slope_distribution=metrics.slope_distribution.to_float_list(),
            aspect=metrics.aspect.value,
            south_aspect_percentage=metrics.south_aspect_percentage.unwrap(),
            area=metrics.area.unwrap(),
            perimeter=metrics.perimeter.unwrap(),
            compactness_index=metrics.compactness_index.unwrap(),
            elongation_index=metrics.elongation_index.unwrap(),
        )

    @staticmethod
    def _compute_bounding_box(polygon: dict[str, Any]) -> BoundingBox:
        """Compute the bounding box from a GeoJSON Polygon geometry.

        Parameters
        ----------
        polygon : dict[str, Any]
            GeoJSON Polygon geometry dict with ``coordinates`` key.

        Returns
        -------
        BoundingBox
            Bounding box covering the polygon extent.
        """
        coordinates = polygon["coordinates"][0]
        lons = [coord[0] for coord in coordinates]
        lats = [coord[1] for coord in coordinates]

        return BoundingBox.from_float(
            min_lat=min(lats),
            min_lon=min(lons),
            max_lat=max(lats),
            max_lon=max(lons),
        )


__all__ = ("CalculateTopographyMetricsUseCase",)
