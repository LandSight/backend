"""Get analysis metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import GetAnalysisMetricsCommand
from app.module.analysis.application.dto.response import AnalysisMetricResponse
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object import AnalysisId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from typing import NoReturn
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
    )


class GetAnalysisMetricsUseCase(
    BaseUseCase[GetAnalysisMetricsCommand, list[AnalysisMetricResponse]],
):
    """Retrieve the metric references recorded for an analysis.

    The references describe which metrics snapshots the analysis used (module,
    category and snapshot ID). Access is granted only when the current user owns
    the underlying parcel.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._logger = get_logger("app.analysis.use_case.get_analysis_metrics")

    @override
    async def __call__(self, command: GetAnalysisMetricsCommand) -> list[AnalysisMetricResponse]:
        self._logger.info("Getting analysis metrics: analysis_id=%s", command.analysis_id)

        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            self._raise_not_found(command.analysis_id)

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            analysis.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to view analysis %s",
                command.current_user_id,
                command.analysis_id,
            )
            self._raise_not_found(command.analysis_id)

        refs = await self._analysis_repository.get_metrics(AnalysisId(command.analysis_id))
        if command.module is not None:
            refs = [ref for ref in refs if ref.metric_type.value == command.module]

        return [
            AnalysisMetricResponse(
                module=ref.metric_type.value,
                category=ref.category,
                metrics_id=ref.metric_id,
            )
            for ref in refs
        ]

    @staticmethod
    def _raise_not_found(analysis_id: UUID) -> NoReturn:
        """Raise a not-found error for the given analysis ID."""
        raise AnalysisNotFoundError(str(analysis_id))


__all__ = ("GetAnalysisMetricsUseCase",)
