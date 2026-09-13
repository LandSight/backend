"""Concrete implementation of the Infrastructure module's internal API.

See :class:`app.module.infrastructure.interface.internal.port.InfrastructureInternalAPI`
for the abstract interface. Metrics are projected straight from the use case
response DTOs into the shared neutral contract, using the domain metric catalog.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.dto.command import (
    CalculateInfrastructureMetricsCommand,
    CategoryMetricRequest,
    CategoryRequest,
    GetInfrastructureMetricsByIdsCommand,
    GetInfrastructureMetricsCommand,
)
from app.module.infrastructure.domain.metric_catalog import CATEGORY_CATALOG, COVERAGE_RATIO
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryInfoResult,
    GetMetricsByIdsInput,
    GetMetricsInput,
)
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.shared.interface.internal import MetricsResponse, build_metric_value


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.response import (
        HospitalMetricsResponse,
        InfrastructureMetricsResponse,
        SchoolMetricsResponse,
        ShopMetricsResponse,
        TransitStopMetricsResponse,
        WaterBodyMetricsResponse,
    )
    from app.module.infrastructure.application.use_case import (
        CalculateInfrastructureMetricsUseCase,
        GetAvailableCategoriesUseCase,
        GetInfrastructureMetricsByIdsUseCase,
        GetInfrastructureMetricsUseCase,
    )
    from app.module.shared.interface.internal import MetricValue

    _CategoryMetrics = (
        SchoolMetricsResponse
        | HospitalMetricsResponse
        | ShopMetricsResponse
        | TransitStopMetricsResponse
        | WaterBodyMetricsResponse
    )


class InfrastructureInternal(InfrastructureInternalAPI):
    """Concrete implementation of the Infrastructure internal API."""

    def __init__(
        self,
        calculate_use_case: CalculateInfrastructureMetricsUseCase,
        get_use_case: GetInfrastructureMetricsUseCase,
        get_by_ids_use_case: GetInfrastructureMetricsByIdsUseCase,
        get_categories_use_case: GetAvailableCategoriesUseCase,
    ) -> None:
        self._calculate = calculate_use_case
        self._get = get_use_case
        self._get_by_ids = get_by_ids_use_case
        self._get_categories = get_categories_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> list[MetricsResponse]:
        """See :meth:`InfrastructureInternalAPI.calculate_metrics`."""
        result = await self._calculate(
            CalculateInfrastructureMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
                categories=[CategoryRequest(c.category, c.buffer) for c in input_data.categories],
            )
        )
        return self.to_metrics_responses(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> list[MetricsResponse]:
        """See :meth:`InfrastructureInternalAPI.get_metrics`."""
        result = await self._get(
            GetInfrastructureMetricsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
                categories=[CategoryRequest(c.category, c.buffer) for c in input_data.categories],
            )
        )
        return self.to_metrics_responses(result)

    @override
    async def get_metrics_by_ids(self, input_data: GetMetricsByIdsInput) -> list[MetricsResponse]:
        """See :meth:`InfrastructureInternalAPI.get_metrics_by_ids`."""
        result = await self._get_by_ids(
            GetInfrastructureMetricsByIdsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
                metrics=[
                    CategoryMetricRequest(category=m.category, metrics_id=m.metrics_id) for m in input_data.metrics
                ],
            )
        )
        return self.to_metrics_responses(result)

    @override
    async def get_available_categories(self) -> list[CategoryInfoResult]:
        """See :meth:`InfrastructureInternalAPI.get_available_categories`."""
        results = await self._get_categories()
        return [CategoryInfoResult(category=r.category) for r in results]

    @staticmethod
    def to_metrics_responses(result: InfrastructureMetricsResponse) -> list[MetricsResponse]:
        """Project an infrastructure use case response into neutral responses per category."""
        responses: list[MetricsResponse] = []
        for category, metrics in (
            ("school", result.school),
            ("hospital", result.hospital),
            ("shop", result.shop),
            ("transit_stop", result.transit_stop),
        ):
            if metrics is not None:
                responses.append(InfrastructureInternal._response(category, metrics, extra=[]))

        if result.water_body is not None:
            water_body = result.water_body
            responses.append(
                InfrastructureInternal._response(
                    "water_body",
                    water_body,
                    extra=[
                        build_metric_value(
                            key=COVERAGE_RATIO.key,
                            label=COVERAGE_RATIO.label,
                            unit=COVERAGE_RATIO.unit,
                            value_type=COVERAGE_RATIO.kind,
                            raw=water_body.coverage_ratio,
                        ),
                    ],
                ),
            )
        return responses

    @staticmethod
    def _response(category: str, metrics: _CategoryMetrics, *, extra: list[MetricValue]) -> MetricsResponse:
        """Build a neutral response for a single infrastructure category."""
        values = InfrastructureInternal._category_values(metrics)
        values.extend(extra)
        return MetricsResponse(
            module="infrastructure",
            category=category,
            id=metrics.id,
            metrics=values,
        )

    @staticmethod
    def _category_values(metrics: _CategoryMetrics) -> list[MetricValue]:
        """Project the fields shared by every infrastructure category."""
        values: list[MetricValue] = []
        for definition in CATEGORY_CATALOG:
            raw = getattr(metrics, definition.key, None)
            if raw is None:
                continue
            values.append(
                build_metric_value(
                    key=definition.key,
                    label=definition.label,
                    unit=definition.unit,
                    value_type=definition.kind,
                    raw=raw,
                ),
            )
        return values


__all__ = ("InfrastructureInternal",)
