"""Get parcel climate metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.climate.application.dto.command import GetParcelClimateMetricsCommand
from app.module.climate.application.dto.response import ClimateMetricsResponse
from app.module.climate.application.error import ClimateMetricsNotFoundError
from app.module.climate.domain.value_object.metric import ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.climate.application.port import MetricsPermissionService, MetricsRepository
    from app.module.climate.domain.entity import ClimateMetrics


class GetParcelClimateMetricsUseCase(BaseUseCase[GetParcelClimateMetricsCommand, ClimateMetricsResponse]):
    """Retrieve the current climate metrics for a parcel.

    Access is granted only when the current user owns the parcel.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.climate.use_case.get_parcel_climate_metrics")

    @override
    async def __call__(self, command: GetParcelClimateMetricsCommand) -> ClimateMetricsResponse:
        self._logger.info("Getting parcel climate metrics: parcel_id=%s", command.parcel_id)

        if not await self._metrics_permission_service.user_can_view_parcel_metrics(
            command.current_user_id,
            command.parcel_id,
        ):
            self._logger.warning(
                "User %s is not allowed to view metrics for parcel %s",
                command.current_user_id,
                command.parcel_id,
            )
            raise ClimateMetricsNotFoundError(str(command.parcel_id))

        metrics = await self._metrics_repository.get_parcel_metrics(ParcelId(command.parcel_id))

        if metrics is None:
            self._logger.warning("Climate metrics not found: parcel_id=%s", command.parcel_id)
            raise ClimateMetricsNotFoundError(str(command.parcel_id))

        self._logger.info("Parcel climate metrics found: id=%s parcel_id=%s", metrics.id, metrics.parcel_id)

        return self._to_response(metrics)

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


__all__ = ("GetParcelClimateMetricsUseCase",)
