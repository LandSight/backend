"""Concrete implementation of the Topography module's internal API.

See :class:`app.module.topography.interface.internal.port.TopographyInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.topography.application.dto.command import (
    CalculateTopographyMetricsCommand,
    GetLatestParcelTopographyMetricsCommand,
    GetTopographyMetricsCommand,
    ListParcelTopographyMetricsCommand,
)
from app.module.topography.interface.internal.dto import (
    CalculateMetricsInput,
    GetLatestParcelMetricsInput,
    GetMetricsInput,
    ListParcelMetricsInput,
    TopographyMetricsResult,
)
from app.module.topography.interface.internal.port import TopographyInternalAPI


if TYPE_CHECKING:
    from app.module.topography.application.dto.response import TopographyMetricsResponse
    from app.module.topography.application.use_case import (
        CalculateTopographyMetricsUseCase,
        GetLatestParcelTopographyMetricsUseCase,
        GetTopographyMetricsUseCase,
        ListParcelTopographyMetricsUseCase,
    )


class TopographyInternal(TopographyInternalAPI):
    """Concrete implementation of the Topography internal API.

    Wraps the application-layer use cases into a single cohesive
    interface that the HTTP layer calls.
    """

    def __init__(
        self,
        calculate_use_case: CalculateTopographyMetricsUseCase,
        get_use_case: GetTopographyMetricsUseCase,
        get_latest_parcel_use_case: GetLatestParcelTopographyMetricsUseCase,
        list_parcel_use_case: ListParcelTopographyMetricsUseCase,
    ) -> None:
        self._calculate = calculate_use_case
        self._get = get_use_case
        self._get_latest_parcel = get_latest_parcel_use_case
        self._list_parcel = list_parcel_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> TopographyMetricsResult:
        """See :meth:`TopographyInternalAPI.calculate_metrics`."""
        result = await self._calculate(
            CalculateTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> TopographyMetricsResult:
        """See :meth:`TopographyInternalAPI.get_metrics`."""
        result = await self._get(
            GetTopographyMetricsCommand(
                metrics_id=input_data.metrics_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_latest_parcel_metrics(self, input_data: GetLatestParcelMetricsInput) -> TopographyMetricsResult:
        """See :meth:`TopographyInternalAPI.get_latest_parcel_metrics`."""
        result = await self._get_latest_parcel(
            GetLatestParcelTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def list_parcel_metrics(self, input_data: ListParcelMetricsInput) -> list[TopographyMetricsResult]:
        """See :meth:`TopographyInternalAPI.list_parcel_metrics`."""
        results = await self._list_parcel(
            ListParcelTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return [self._to_result(result) for result in results]

    @staticmethod
    def _to_result(result: TopographyMetricsResponse) -> TopographyMetricsResult:
        """Map an application response DTO to an internal result DTO."""
        return TopographyMetricsResult(
            id=result.id,
            parcel_id=result.parcel_id,
            mean_elevation=result.mean_elevation,
            max_elevation=result.max_elevation,
            min_elevation=result.min_elevation,
            elevation_range=result.elevation_range,
            elevation_std=result.elevation_std,
            mean_slope=result.mean_slope,
            max_slope=result.max_slope,
            slope_percentiles=result.slope_percentiles,
            slope_distribution=result.slope_distribution,
            aspect=result.aspect,
            south_aspect_percentage=result.south_aspect_percentage,
            area=result.area,
            perimeter=result.perimeter,
            compactness_index=result.compactness_index,
            elongation_index=result.elongation_index,
            created_at=result.created_at,
        )


__all__ = ("TopographyInternal",)
