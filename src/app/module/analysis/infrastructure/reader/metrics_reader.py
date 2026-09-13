"""Metrics reader backed by the metric modules' Internal APIs.

The metric modules return the neutral ``MetricsResponse`` contract directly, so
this adapter only groups references and concatenates the results.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import MetricsReader
from app.module.analysis.domain.value_object import MetricType
from app.module.climate.interface.internal.dto import GetMetricsInput as ClimateGetMetricsInput
from app.module.infrastructure.interface.internal.dto import (
    CategoryMetricRefInput,
    GetMetricsByIdsInput,
)
from app.module.topography.interface.internal.dto import GetMetricsInput as TopographyGetMetricsInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import AnalysisMetricRef
    from app.module.climate.interface.internal.port import ClimateInternalAPI
    from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
    from app.module.shared.interface.internal import MetricsResponse
    from app.module.topography.interface.internal.port import TopographyInternalAPI


class MetricsReaderImpl(MetricsReader):
    """Reads metric values through the metric modules' Internal APIs."""

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
    async def read(
        self,
        parcel_id: UUID,
        refs: list[AnalysisMetricRef],
        user_id: UUID,
    ) -> list[MetricsResponse]:
        """See :class:`app.module.analysis.application.port.MetricsReader.read`."""
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


__all__ = ("MetricsReaderImpl",)
