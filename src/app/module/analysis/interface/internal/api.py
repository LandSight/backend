"""Concrete implementation of the Analysis module's internal API.

See :class:`app.module.analysis.interface.internal.port.AnalysisInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import (
    GetAnalysisCommand,
    ListUserAnalysesCommand,
    StartAnalysisCommand,
)
from app.module.analysis.interface.internal.dto import (
    AnalysisResult,
    GetAnalysisInput,
    ListUserAnalysesInput,
    StartAnalysisInput,
)
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


if TYPE_CHECKING:
    from app.module.analysis.application.dto.response import AnalysisResponse
    from app.module.analysis.application.use_case import (
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
        list_user_analyses_use_case: ListUserAnalysesUseCase,
    ) -> None:
        self._start_analysis = start_analysis_use_case
        self._get_analysis = get_analysis_use_case
        self._list_user_analyses = list_user_analyses_use_case

    @override
    async def start_analysis(self, input_data: StartAnalysisInput) -> AnalysisResult:
        """See :meth:`AnalysisInternalAPI.start_analysis`."""
        result = await self._start_analysis(
            StartAnalysisCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
                name=input_data.name,
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
    async def list_user_analyses(self, input_data: ListUserAnalysesInput) -> list[AnalysisResult]:
        """See :meth:`AnalysisInternalAPI.list_user_analyses`."""
        results = await self._list_user_analyses(ListUserAnalysesCommand(current_user_id=input_data.current_user_id))
        return [self._to_result(result) for result in results]

    @staticmethod
    def _to_result(result: AnalysisResponse) -> AnalysisResult:
        """Map an application response DTO to an internal result DTO."""
        return AnalysisResult(
            id=result.id,
            parcel_id=result.parcel_id,
            name=result.name,
            status=result.status,
            score=result.score,
            status_reason=result.status_reason,
            created_at=result.created_at,
        )


__all__ = ("AnalysisInternal",)
