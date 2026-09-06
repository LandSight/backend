"""Calculate climate metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.climate.application.dto.command import CalculateClimateMetricsCommand
from app.module.climate.application.dto.response import ClimateMetricsResponse
from app.module.climate.application.error import ClimateDataNotFoundError
from app.module.climate.domain.entity import ClimateMetrics
from app.module.climate.domain.value_object.metric import ClimateMetricsId, ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.module.shared.domain.value_object import BoundingBox
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.climate.application.port import (
        ClimateMetricsService,
        LocalClimateRepository,
        MetricsRepository,
        ParcelProvider,
    )
    from app.module.shared.application.dto.geojson import GeoJSONPolygon


class CalculateClimateMetricsUseCase(BaseUseCase[CalculateClimateMetricsCommand, ClimateMetricsResponse]):
    """Calculate climate metrics for a given parcel.

    Fetches the authoritative parcel geometry from the Parcel module (which
    enforces access), reads the 8 WorldClim 2.1 COG rasters from S3, computes
    the bioclimatic metrics, persists them, and returns the result.
    """

    def __init__(
        self,
        local_climate_repository: LocalClimateRepository,
        climate_metrics_service: ClimateMetricsService,
        metrics_repository: MetricsRepository,
        parcel_provider: ParcelProvider,
    ) -> None:
        self._local_climate_repository = local_climate_repository
        self._climate_metrics_service = climate_metrics_service
        self._metrics_repository = metrics_repository
        self._parcel_provider = parcel_provider
        self._logger = get_logger("app.climate.use_case.calculate_climate_metrics")

    @override
    async def __call__(self, command: CalculateClimateMetricsCommand) -> ClimateMetricsResponse:
        self._logger.info("Calculating climate metrics: parcel_id=%s", command.parcel_id)

        # The Parcel module returns the geometry only for authorized users,
        # so this doubles as the access control gate for the calculation.
        polygon = await self._parcel_provider.get_parcel_polygon(
            command.parcel_id,
            command.current_user_id,
        )

        # Calculate bounding box from polygon coordinates
        bounds = self._compute_bounding_box(polygon)

        # Check whether climate data is available for the requested bounds.
        if not await self._local_climate_repository.exists(bounds):
            reason = f"There is no data for the requested parcel boundaries: {bounds}"
            self._logger.warning("No climate data for parcel_id=%s: %s", command.parcel_id, reason)
            raise ClimateDataNotFoundError(reason)

        # Fetch the raster sub-regions for all 8 variables.
        climate_data = await self._local_climate_repository.get_climate_data(bounds)

        if climate_data is None:
            reason = f"There is no data for the requested parcel boundaries: {bounds}"
            self._logger.warning("No climate data for parcel_id=%s: %s", command.parcel_id, reason)
            raise ClimateDataNotFoundError(reason)

        # Create domain entity
        metrics = ClimateMetrics(
            id=ClimateMetricsId(uuid6()),
            parcel_id=ParcelId(command.parcel_id),
            mean_annual_temperature=self._climate_metrics_service.calculate_mean_annual_temperature(climate_data),
            annual_precipitation=self._climate_metrics_service.calculate_annual_precipitation(climate_data),
            temperature_seasonality=self._climate_metrics_service.calculate_temperature_seasonality(climate_data),
            precipitation_seasonality=self._climate_metrics_service.calculate_precipitation_seasonality(climate_data),
            max_temperature_warmest_month=self._climate_metrics_service.calculate_max_temperature_warmest_month(
                climate_data
            ),
            min_temperature_coldest_month=self._climate_metrics_service.calculate_min_temperature_coldest_month(
                climate_data
            ),
            precipitation_wettest_month=self._climate_metrics_service.calculate_precipitation_wettest_month(
                climate_data
            ),
            precipitation_driest_month=self._climate_metrics_service.calculate_precipitation_driest_month(climate_data),
        )

        persisted = await self._metrics_repository.save(metrics)

        self._logger.info("Climate metrics calculated: id=%s parcel_id=%s", persisted.id, persisted.parcel_id)

        return self._to_response(persisted)

    @staticmethod
    def _compute_bounding_box(polygon: GeoJSONPolygon) -> BoundingBox:
        """Compute the bounding box from a GeoJSON Polygon geometry.

        Parameters
        ----------
        polygon : GeoJSONPolygon
            GeoJSON Polygon geometry.

        Returns
        -------
        BoundingBox
            Bounding box covering the polygon extent.
        """
        coordinates = polygon.coordinates[0]
        lons = [coord[0] for coord in coordinates]
        lats = [coord[1] for coord in coordinates]

        return BoundingBox.from_float(
            min_lat=min(lats),
            min_lon=min(lons),
            max_lat=max(lats),
            max_lon=max(lons),
        )

    @staticmethod
    def _to_response(metrics: ClimateMetrics) -> ClimateMetricsResponse:
        """Map a domain entity to a response DTO."""
        return ClimateMetricsResponse(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            created_at=metrics.created_at,
            mean_annual_temperature=metrics.mean_annual_temperature.unwrap(),
            annual_precipitation=metrics.annual_precipitation.unwrap(),
            temperature_seasonality=metrics.temperature_seasonality.unwrap(),
            precipitation_seasonality=metrics.precipitation_seasonality.unwrap(),
            max_temperature_warmest_month=metrics.max_temperature_warmest_month.unwrap(),
            min_temperature_coldest_month=metrics.min_temperature_coldest_month.unwrap(),
            precipitation_wettest_month=metrics.precipitation_wettest_month.unwrap(),
            precipitation_driest_month=metrics.precipitation_driest_month.unwrap(),
        )


__all__ = ("CalculateClimateMetricsUseCase",)
