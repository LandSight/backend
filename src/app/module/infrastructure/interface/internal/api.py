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
    DeleteInfrastructureMetricsCommand,
    GetInfrastructureMetricsByIdsCommand,
    GetInfrastructureMetricsCommand,
)
from app.module.infrastructure.domain.metric_catalog import CATEGORY_METRICS
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryInfoResult,
    DeleteMetricsInput,
    GetMetricsByIdsInput,
    GetMetricsInput,
)
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.shared.interface.internal import MetricsResponse, build_metric_value


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.response import InfrastructureMetricsResponse
    from app.module.infrastructure.application.use_case import (
        CalculateInfrastructureMetricsUseCase,
        DeleteInfrastructureMetricsUseCase,
        GetAvailableCategoriesUseCase,
        GetInfrastructureMetricsByIdsUseCase,
        GetInfrastructureMetricsUseCase,
    )
    from app.module.infrastructure.domain.metric_catalog import MetricDefinition
    from app.module.shared.interface.internal import MetricValue


class InfrastructureInternal(InfrastructureInternalAPI):
    """Concrete implementation of the Infrastructure internal API."""

    def __init__(
        self,
        calculate_use_case: CalculateInfrastructureMetricsUseCase,
        get_use_case: GetInfrastructureMetricsUseCase,
        get_by_ids_use_case: GetInfrastructureMetricsByIdsUseCase,
        get_categories_use_case: GetAvailableCategoriesUseCase,
        delete_metrics_use_case: DeleteInfrastructureMetricsUseCase,
    ) -> None:
        self._calculate = calculate_use_case
        self._get = get_use_case
        self._get_by_ids = get_by_ids_use_case
        self._get_categories = get_categories_use_case
        self._delete_metrics = delete_metrics_use_case

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

    @override
    async def delete_metrics(self, input_data: DeleteMetricsInput) -> None:
        """See :meth:`InfrastructureInternalAPI.delete_metrics`."""
        await self._delete_metrics(
            DeleteInfrastructureMetricsCommand(
                metrics=[
                    CategoryMetricRequest(category=m.category, metrics_id=m.metrics_id) for m in input_data.metrics
                ],
            )
        )

    @staticmethod
    def to_metrics_responses(result: InfrastructureMetricsResponse) -> list[MetricsResponse]:
        """Project an infrastructure use case response into neutral responses per category."""
        responses: list[MetricsResponse] = []
        for category, metrics in result.categories.items():
            definitions = CATEGORY_METRICS.get(category)
            if definitions is None:
                continue
            responses.append(
                MetricsResponse(
                    module="infrastructure",
                    category=category,
                    id=metrics.id,
                    metrics=InfrastructureInternal._category_values(metrics, definitions),
                )
            )
        return responses

    @staticmethod
    def _category_values(
        metrics: object,
        definitions: tuple[MetricDefinition, ...],
    ) -> list[MetricValue]:
        """Build the neutral metric values declared by the category catalog."""
        values: list[MetricValue] = []
        for definition in definitions:
            if not hasattr(metrics, definition.key):
                continue
            values.append(
                build_metric_value(
                    key=definition.key,
                    label=definition.label,
                    unit=definition.unit,
                    value_type=definition.kind,
                    raw=getattr(metrics, definition.key),
                )
            )
        return values


__all__ = ("InfrastructureInternal",)
