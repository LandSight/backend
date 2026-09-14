"""Metrics collector backed by the metric modules' Internal APIs.

The metric modules return the neutral ``MetricValue`` contract; this adapter
derives the persisted snapshot references the analysis needs to store.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import MetricsCollector
from app.module.analysis.domain.value_object import AnalysisMetricRef, MetricType
from app.module.climate.interface.internal.dto import CalculateMetricsInput as ClimateCalculateMetricsInput
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput as InfrastructureCalculateMetricsInput,
    CategoryRequestInput,
)
from app.module.topography.interface.internal.dto import CalculateMetricsInput as TopographyCalculateMetricsInput
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.climate.interface.internal.port import ClimateInternalAPI
    from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
    from app.module.shared.interface.internal import MetricsResponse
    from app.module.topography.interface.internal.port import TopographyInternalAPI


class MetricsCollectorImpl(MetricsCollector):
    """Calculates analysis metrics through the metric modules' Internal APIs."""

    def __init__(
        self,
        topography_api: TopographyInternalAPI,
        climate_api: ClimateInternalAPI,
        infrastructure_api: InfrastructureInternalAPI,
    ) -> None:
        self._topography_api = topography_api
        self._climate_api = climate_api
        self._infrastructure_api = infrastructure_api
        self._logger = get_logger("app.analysis.infrastructure.metrics_collector")

    @override
    async def collect_topography(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """See :class:`app.module.analysis.application.port.MetricsCollector.collect_topography`."""
        response = await self._topography_api.calculate_metrics(
            TopographyCalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return self._to_ref(response)

    @override
    async def collect_climate(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """See :class:`app.module.analysis.application.port.MetricsCollector.collect_climate`."""
        response = await self._climate_api.calculate_metrics(
            ClimateCalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return self._to_ref(response)

    @override
    async def collect_infrastructure(
        self,
        parcel_id: UUID,
        user_id: UUID,
        buffers: dict[str, int],
    ) -> list[AnalysisMetricRef]:
        """See :class:`app.module.analysis.application.port.MetricsCollector.collect_infrastructure`."""
        available = await self._infrastructure_api.get_available_categories()
        categories = [
            CategoryRequestInput(category=info.category, buffer=buffers[info.category])
            for info in available
            if info.category in buffers
        ]
        if not categories:
            self._logger.warning("No infrastructure categories configured for analysis.")
            return []

        responses = await self._infrastructure_api.calculate_metrics(
            InfrastructureCalculateMetricsInput(
                parcel_id=parcel_id,
                current_user_id=user_id,
                categories=categories,
            ),
        )
        return [self._to_ref(response) for response in responses]

    @staticmethod
    def _to_ref(response: MetricsResponse) -> AnalysisMetricRef:
        """Derive a snapshot reference from a neutral metrics response."""
        return AnalysisMetricRef(
            metric_type=MetricType(response.module),
            metric_id=response.id,
            category=response.category,
        )


__all__ = ("MetricsCollectorImpl",)
