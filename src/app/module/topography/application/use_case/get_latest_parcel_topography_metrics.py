"""Get latest parcel topography metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.application.use_case import BaseUseCase
from app.module.topography.application.dto.command import GetLatestParcelTopographyMetricsCommand
from app.module.topography.application.dto.response import TopographyMetricsResponse
from app.module.topography.application.error import TopographyMetricsNotFoundError
from app.module.topography.domain.value_object.metric import ParcelId
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.topography.application.port import MetricsPermissionService, MetricsRepository


class GetLatestParcelTopographyMetricsUseCase(
    BaseUseCase[GetLatestParcelTopographyMetricsCommand, TopographyMetricsResponse]
):
    """Retrieve the most recent topography metrics for a parcel.

    Access is granted only when the current user owns the parcel.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.topography.use_case.get_latest_parcel_topography_metrics")

    @override
    async def __call__(self, command: GetLatestParcelTopographyMetricsCommand) -> TopographyMetricsResponse:
        self._logger.info("Getting latest topography metrics: parcel_id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)

        if not await self._metrics_permission_service.user_can_view_parcel_metrics(
            command.current_user_id,
            command.parcel_id,
        ):
            self._logger.warning(
                "User %s is not allowed to view metrics for parcel %s",
                command.current_user_id,
                command.parcel_id,
            )
            raise TopographyMetricsNotFoundError(str(command.parcel_id))

        metrics = await self._metrics_repository.get_latest(parcel_id)

        if metrics is None:
            self._logger.warning("Topography metrics not found: parcel_id=%s", command.parcel_id)
            raise TopographyMetricsNotFoundError(str(command.parcel_id))

        self._logger.info("Latest topography metrics found: id=%s parcel_id=%s", metrics.id, metrics.parcel_id)

        return TopographyMetricsResponse(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
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
            created_at=metrics.created_at,
        )


__all__ = ("GetLatestParcelTopographyMetricsUseCase",)
