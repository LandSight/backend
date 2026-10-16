"""Metrics gateway backed by the metric modules' Internal APIs.

The metric modules return the neutral ``MetricsResponse``/``MetricValue``
contracts; this adapter derives the persisted snapshot references the analysis
needs to store, reads the values back and deletes the snapshots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import MetricsService
from app.module.analysis.domain.value_object.metric import AnalysisMetricRef, MetricType
from app.module.climate.interface.internal.dto import (
    CalculateMetricsInput as ClimateCalculateMetricsInput,
    DeleteMetricsInput as ClimateDeleteMetricsInput,
    GetMetricsInput as ClimateGetMetricsInput,
)
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput as InfrastructureCalculateMetricsInput,
    CategoryMetricRefInput,
    CategoryRequestInput,
    DeleteMetricsInput as InfrastructureDeleteMetricsInput,
    GetMetricsByIdsInput,
)
from app.module.topography.interface.internal.dto import (
    CalculateMetricsInput as TopographyCalculateMetricsInput,
    DeleteMetricsInput as TopographyDeleteMetricsInput,
    GetMetricsInput as TopographyGetMetricsInput,
)
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Mapping
    from uuid import UUID

    from app.module.climate.interface.internal.port import ClimateInternalAPI
    from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
    from app.module.shared.interface.internal import MetricsResponse
    from app.module.topography.interface.internal.port import TopographyInternalAPI


class MetricsServiceImpl(MetricsService):
    """Calculates, reads and deletes metrics through the metric modules' Internal APIs."""

    def __init__(
        self,
        topography_api: TopographyInternalAPI,
        climate_api: ClimateInternalAPI,
        infrastructure_api: InfrastructureInternalAPI,
    ) -> None:
        self._topography_api = topography_api
        self._climate_api = climate_api
        self._infrastructure_api = infrastructure_api
        self._logger = get_logger("app.analysis.infrastructure.metrics_service")

    @override
    async def collect_topography(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """See :class:`app.module.analysis.application.port.MetricsService.collect_topography`."""
        response = await self._topography_api.calculate_metrics(
            TopographyCalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return self._to_ref(response)

    @override
    async def collect_climate(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """See :class:`app.module.analysis.application.port.MetricsService.collect_climate`."""
        response = await self._climate_api.calculate_metrics(
            ClimateCalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return self._to_ref(response)

    @override
    async def collect_infrastructure(
        self,
        parcel_id: UUID,
        user_id: UUID,
        buffers: Mapping[str, int],
    ) -> list[AnalysisMetricRef]:
        """See :class:`app.module.analysis.application.port.MetricsService.collect_infrastructure`."""
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

    @override
    async def get_metrics(
        self,
        parcel_id: UUID,
        refs: list[AnalysisMetricRef],
        user_id: UUID,
    ) -> list[MetricsResponse]:
        """See :class:`app.module.analysis.application.port.MetricsService.read`."""
        responses: list[MetricsResponse] = []

        for ref in refs:
            if ref.metric_type is MetricType.TOPOGRAPHY:
                responses.append(
                    await self._topography_api.get_metrics(
                        TopographyGetMetricsInput(metrics_id=ref.metric_id, current_user_id=user_id),
                    ),
                )
            elif ref.metric_type is MetricType.CLIMATE:
                responses.append(
                    await self._climate_api.get_metrics(
                        ClimateGetMetricsInput(metrics_id=ref.metric_id, current_user_id=user_id),
                    ),
                )

        responses.extend(await self._read_infrastructure(parcel_id, refs, user_id))
        return responses

    async def _read_infrastructure(
        self,
        parcel_id: UUID,
        refs: list[AnalysisMetricRef],
        user_id: UUID,
    ) -> list[MetricsResponse]:
        """Read all infrastructure references in a single batch call."""
        infrastructure_refs = [
            ref for ref in refs if ref.metric_type is MetricType.INFRASTRUCTURE and ref.category is not None
        ]
        if not infrastructure_refs:
            return []

        return await self._infrastructure_api.get_metrics_by_ids(
            GetMetricsByIdsInput(
                parcel_id=parcel_id,
                current_user_id=user_id,
                metrics=[
                    CategoryMetricRefInput(category=ref.category or "", metrics_id=ref.metric_id)
                    for ref in infrastructure_refs
                ],
            ),
        )

    @override
    async def delete(self, refs: list[AnalysisMetricRef]) -> None:
        """See :class:`app.module.analysis.application.port.MetricsService.delete`."""
        topography_ids = [ref.metric_id for ref in refs if ref.metric_type is MetricType.TOPOGRAPHY]
        if topography_ids:
            await self._topography_api.delete_metrics(TopographyDeleteMetricsInput(metrics_ids=topography_ids))

        climate_ids = [ref.metric_id for ref in refs if ref.metric_type is MetricType.CLIMATE]
        if climate_ids:
            await self._climate_api.delete_metrics(ClimateDeleteMetricsInput(metrics_ids=climate_ids))

        infrastructure_refs = [
            CategoryMetricRefInput(category=ref.category or "", metrics_id=ref.metric_id)
            for ref in refs
            if ref.metric_type is MetricType.INFRASTRUCTURE and ref.category is not None
        ]
        if infrastructure_refs:
            await self._infrastructure_api.delete_metrics(
                InfrastructureDeleteMetricsInput(metrics=infrastructure_refs),
            )

    @staticmethod
    def _to_ref(response: MetricsResponse) -> AnalysisMetricRef:
        """Derive a snapshot reference from a neutral metrics response."""
        return AnalysisMetricRef(
            metric_type=MetricType(response.module),
            metric_id=response.id,
            category=response.category,
        )


__all__ = ("MetricsServiceImpl",)
