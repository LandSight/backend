"""Concrete implementation of the Climate module's internal API.

See :class:`app.module.climate.interface.internal.port.ClimateInternalAPI`
for the abstract interface. Metrics are projected straight from the use case
response DTOs into the shared neutral contract, using the domain metric catalog.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.climate.application.dto.command import (
    CalculateClimateMetricsCommand,
    GetClimateMetricsCommand,
    GetParcelClimateMetricsCommand,
)
from app.module.climate.domain.metric_catalog import CATALOG
from app.module.climate.interface.internal.port import ClimateInternalAPI
from app.module.shared.interface.internal import MetricsResponse, build_metric_value


if TYPE_CHECKING:
    from app.module.climate.application.dto.response import ClimateMetricsResponse
    from app.module.climate.application.use_case import (
        CalculateClimateMetricsUseCase,
        GetClimateMetricsUseCase,
        GetParcelClimateMetricsUseCase,
    )
    from app.module.climate.interface.internal.dto import (
        CalculateMetricsInput,
        GetMetricsInput,
        GetParcelMetricsInput,
    )


class ClimateInternal(ClimateInternalAPI):
    """Concrete implementation of the Climate internal API."""

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
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> MetricsResponse:
        """See :meth:`ClimateInternalAPI.calculate_metrics`."""
        result = await self._calculate_metrics(
            CalculateClimateMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> MetricsResponse:
        """See :meth:`ClimateInternalAPI.get_metrics`."""
        result = await self._get_metrics(
            GetClimateMetricsCommand(
                metrics_id=input_data.metrics_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @override
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> MetricsResponse:
        """See :meth:`ClimateInternalAPI.get_parcel_metrics`."""
        result = await self._get_parcel_metrics(
            GetParcelClimateMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @staticmethod
    def to_metrics_response(result: ClimateMetricsResponse) -> MetricsResponse:
        """Project a climate use case response into the shared neutral contract."""
        return MetricsResponse(
            module="climate",
            category=None,
            id=result.id,
            metrics=[
                build_metric_value(
                    key=definition.key,
                    label=definition.label,
                    unit=definition.unit,
                    value_type=definition.kind,
                    raw=getattr(result, definition.key),
                )
                for definition in CATALOG
            ],
        )


__all__ = ("ClimateInternal",)
