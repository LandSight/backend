"""Concrete implementation of the Climate module's internal API.

See :class:`app.module.climate.interface.internal.port.ClimateInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.climate.application.dto.command import (
    CalculateClimateMetricsCommand,
    GetClimateMetricsCommand,
    GetParcelClimateMetricsCommand,
)
from app.module.climate.interface.internal.dto import (
    CalculateMetricsInput,
    ClimateMetricsResult,
    GetMetricsInput,
    GetParcelMetricsInput,
)
from app.module.climate.interface.internal.port import ClimateInternalAPI


if TYPE_CHECKING:
    from app.module.climate.application.dto.response import ClimateMetricsResponse
    from app.module.climate.application.use_case import (
        CalculateClimateMetricsUseCase,
        GetClimateMetricsUseCase,
        GetParcelClimateMetricsUseCase,
    )


class ClimateInternal(ClimateInternalAPI):
    """Concrete implementation of the Climate internal API.

    Wraps the application-layer use cases into a single cohesive
    interface that the HTTP layer calls.
    """

    def __init__(
        self,
        calculate_metrics_use_case: CalculateClimateMetricsUseCase,
        get_metrics_use_case: GetClimateMetricsUseCase,
        get_parcel_metrics_use_case: GetParcelClimateMetricsUseCase,
    ) -> None:
        self._calculate_metrics = calculate_metrics_use_case
        self._get_metrics = get_metrics_use_case
        self._get_parcel_metrics = get_parcel_metrics_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> ClimateMetricsResult:
        """See :meth:`ClimateInternalAPI.calculate_metrics`."""
        result = await self._calculate_metrics(
            CalculateClimateMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> ClimateMetricsResult:
        """See :meth:`ClimateInternalAPI.get_metrics`."""
        result = await self._get_metrics(
            GetClimateMetricsCommand(
                metrics_id=input_data.metrics_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> ClimateMetricsResult:
        """See :meth:`ClimateInternalAPI.get_parcel_metrics`."""
        result = await self._get_parcel_metrics(
            GetParcelClimateMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @staticmethod
    def _to_result(result: ClimateMetricsResponse) -> ClimateMetricsResult:
        """Map an application response DTO to an internal result DTO."""
        return ClimateMetricsResult(
            id=result.id,
            parcel_id=result.parcel_id,
            created_at=result.created_at,
            mean_annual_temperature=result.mean_annual_temperature,
            annual_precipitation=result.annual_precipitation,
            temperature_seasonality=result.temperature_seasonality,
            precipitation_seasonality=result.precipitation_seasonality,
            max_temperature_warmest_month=result.max_temperature_warmest_month,
            min_temperature_coldest_month=result.min_temperature_coldest_month,
            precipitation_wettest_month=result.precipitation_wettest_month,
            precipitation_driest_month=result.precipitation_driest_month,
        )


__all__ = ("ClimateInternal",)
