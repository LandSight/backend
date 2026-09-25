"""Concrete implementation of the Analysis module's internal API.

See :class:`app.module.analysis.interface.internal.port.AnalysisInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import (
    DeleteAnalysisCommand,
    GetAnalysisCommand,
    GetAnalysisMetricsCommand,
    ListUserAnalysesCommand,
    StartAnalysisCommand,
)
from app.module.analysis.interface.internal.dto import (
    AnalysisMetricResult,
    AnalysisResult,
    DeleteAnalysisInput,
    GetAnalysisInput,
    GetAnalysisMetricsInput,
    ListUserAnalysesInput,
    StartAnalysisInput,
)
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


if TYPE_CHECKING:
    from app.module.analysis.application.dto.response import AnalysisMetricResponse, AnalysisResponse
    from app.module.analysis.application.use_case import (
        DeleteAnalysisUseCase,
        GetAnalysisMetricsUseCase,
        GetAnalysisUseCase,
        ListUserAnalysesUseCase,
        StartAnalysisUseCase,
    )


class AnalysisInternal(AnalysisInternalAPI):
    """Concrete implementation of the Analysis internal API."""

    def __init__(
        self,
        start_analysis_use_case: StartAnalysisUseCase,
        get_analysis_use_case: GetAnalysisUseCase,
        get_analysis_metrics_use_case: GetAnalysisMetricsUseCase,
        list_user_analyses_use_case: ListUserAnalysesUseCase,
        delete_analysis_use_case: DeleteAnalysisUseCase,
    ) -> None:
        self._start_analysis = start_analysis_use_case
        self._get_analysis = get_analysis_use_case
        self._get_analysis_metrics = get_analysis_metrics_use_case
        self._list_user_analyses = list_user_analyses_use_case
        self._delete_analysis = delete_analysis_use_case

    @override
    async def start_analysis(self, input_data: StartAnalysisInput) -> AnalysisResult:
        """See :meth:`AnalysisInternalAPI.start_analysis`."""
        result = await self._start_analysis(
            StartAnalysisCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
                name=input_data.name,
                analysis_type=input_data.analysis_type,
            )
        )
        return self._to_result(result)

    @override
    async def get_analysis(self, input_data: GetAnalysisInput) -> AnalysisResult:
        """See :meth:`AnalysisInternalAPI.get_analysis`."""
        result = await self._get_analysis(
            GetAnalysisCommand(
                analysis_id=input_data.analysis_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_analysis_metrics(self, input_data: GetAnalysisMetricsInput) -> list[AnalysisMetricResult]:
        """See :meth:`AnalysisInternalAPI.get_analysis_metrics`."""
        results = await self._get_analysis_metrics(
            GetAnalysisMetricsCommand(
                analysis_id=input_data.analysis_id,
                current_user_id=input_data.current_user_id,
                module=input_data.module,
            )
        )
        return [self._to_metric_result(result) for result in results]

    @override
    async def list_user_analyses(self, input_data: ListUserAnalysesInput) -> list[AnalysisResult]:
        """See :meth:`AnalysisInternalAPI.list_user_analyses`."""
        results = await self._list_user_analyses(ListUserAnalysesCommand(current_user_id=input_data.current_user_id))
        return [self._to_result(result) for result in results]

    @override
    async def delete_analysis(self, input_data: DeleteAnalysisInput) -> None:
        """See :meth:`AnalysisInternalAPI.delete_analysis`."""
        await self._delete_analysis(
            DeleteAnalysisCommand(
                analysis_id=input_data.analysis_id,
                current_user_id=input_data.current_user_id,
            )
        )

    @staticmethod
    def _to_metric_result(result: AnalysisMetricResponse) -> AnalysisMetricResult:
        """Map an application metric response DTO to an internal result DTO."""
        return AnalysisMetricResult(
            module=result.module,
            category=result.category,
            metrics_id=result.metrics_id,
        )

    @staticmethod
    def _to_result(result: AnalysisResponse) -> AnalysisResult:
        """Map an application response DTO to an internal result DTO."""
        return AnalysisResult(
            id=result.id,
            parcel_id=result.parcel_id,
            parcel_name=result.parcel_name,
            name=result.name,
            analysis_type=result.analysis_type,
            status=result.status,
            stage=result.stage,
            score=result.score,
            model_version=result.model_version,
            status_reason=result.status_reason,
            created_at=result.created_at,
            completed_at=result.completed_at,
        )


__all__ = ("AnalysisInternal",)
