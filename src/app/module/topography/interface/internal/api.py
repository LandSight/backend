"""Concrete implementation of the Topography module's internal API.

See :class:`app.module.topography.interface.internal.port.TopographyInternalAPI`
for the abstract interface. Metrics are projected straight from the use case
response DTOs into the shared neutral contract, using the domain metric catalog.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.interface.internal import (
    MetricsResponse,
    NumberMetricValue,
    build_metric_value,
)
from app.module.topography.application.dto.command import (
    CalculateTopographyMetricsCommand,
    GetLatestParcelTopographyMetricsCommand,
    GetTopographyMetricsCommand,
)
from app.module.topography.domain.metric_catalog import CATALOG
from app.module.topography.interface.internal.port import TopographyInternalAPI


if TYPE_CHECKING:
    from app.module.shared.interface.internal import MetricValue
    from app.module.topography.application.dto.response import TopographyMetricsResponse
    from app.module.topography.application.use_case import (
        CalculateTopographyMetricsUseCase,
        GetParcelTopographyMetricsUseCase,
        GetTopographyMetricsUseCase,
    )
    from app.module.topography.interface.internal.dto import (
        CalculateMetricsInput,
        GetMetricsInput,
        GetParcelMetricsInput,
    )


class TopographyInternal(TopographyInternalAPI):
    """Concrete implementation of the Topography internal API."""

    def __init__(
        self,
        calculate_metrics_use_case: CalculateTopographyMetricsUseCase,
        get_metrics_use_case: GetTopographyMetricsUseCase,
        get_parcel_metrics_use_case: GetParcelTopographyMetricsUseCase,
    ) -> None:
        self._calculate_metrics = calculate_metrics_use_case
        self._get_metrics = get_metrics_use_case
        self._get_parcel_metrics = get_parcel_metrics_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> MetricsResponse:
        """See :meth:`TopographyInternalAPI.calculate_metrics`."""
        result = await self._calculate_metrics(
            CalculateTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> MetricsResponse:
        """See :meth:`TopographyInternalAPI.get_metrics`."""
        result = await self._get_metrics(
            GetTopographyMetricsCommand(
                metrics_id=input_data.metrics_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @override
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> MetricsResponse:
        """See :meth:`TopographyInternalAPI.get_parcel_metrics`."""
        result = await self._get_parcel_metrics(
            GetLatestParcelTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self.to_metrics_response(result)

    @staticmethod
    def to_metrics_response(result: TopographyMetricsResponse) -> MetricsResponse:
        """Project a topography use case response into the shared neutral contract."""
        metrics: list[MetricValue] = [
            build_metric_value(
                key=definition.key,
                label=definition.label,
                unit=definition.unit,
                value_type=definition.kind,
                raw=getattr(result, definition.key),
            )
            for definition in CATALOG
        ]
        metrics.extend(
            NumberMetricValue(
                key=f"slope_p{percentile}",
                label=f"Slope p{percentile}",
                unit="deg",
                value=value,
            )
            for percentile, value in result.slope_percentiles.items()
        )
        return MetricsResponse(
            module="topography",
            category=None,
            id=result.id,
            metrics=metrics,
        )


__all__ = ("TopographyInternal",)
