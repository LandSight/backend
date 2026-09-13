"""Metrics remover backed by the metric modules' Internal APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import MetricsRemover
from app.module.analysis.domain.value_object import MetricType
from app.module.climate.interface.internal.dto import DeleteMetricsInput as ClimateDeleteMetricsInput
from app.module.infrastructure.interface.internal.dto import (
    CategoryMetricRefInput,
    DeleteMetricsInput as InfrastructureDeleteMetricsInput,
)
from app.module.topography.interface.internal.dto import DeleteMetricsInput as TopographyDeleteMetricsInput


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import AnalysisMetricRef
    from app.module.climate.interface.internal.port import ClimateInternalAPI
    from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
    from app.module.topography.interface.internal.port import TopographyInternalAPI


class MetricsRemoverImpl(MetricsRemover):
    """Deletes metric snapshots through the metric modules' Internal APIs."""

    def __init__(
        self,
        topography_api: TopographyInternalAPI,
        climate_api: ClimateInternalAPI,
        infrastructure_api: InfrastructureInternalAPI,
    ) -> None:
        self._topography_api = topography_api
        self._climate_api = climate_api
        self._infrastructure_api = infrastructure_api

    @override
    async def delete(self, refs: list[AnalysisMetricRef]) -> None:
        """See :class:`app.module.analysis.application.port.MetricsRemover.delete`."""
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


__all__ = ("MetricsRemoverImpl",)
