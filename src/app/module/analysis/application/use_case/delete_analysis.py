"""Delete analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import DeleteAnalysisCommand
from app.module.analysis.application.error import (
    AnalysisNotDeletableError,
    AnalysisNotFoundError,
)
from app.module.analysis.domain.value_object import AnalysisId, AnalysisStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
        MetricsRemover,
    )


class DeleteAnalysisUseCase(BaseUseCase[DeleteAnalysisCommand, None]):
    """Delete an analysis together with its metric references.

    Access is granted only when the current user owns the underlying parcel.
    Metric snapshots owned by other modules are left untouched.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
        metrics_remover: MetricsRemover,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._metrics_remover = metrics_remover
        self._logger = get_logger("app.analysis.use_case.delete_analysis")

    @override
    async def __call__(self, command: DeleteAnalysisCommand) -> None:
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            raise AnalysisNotFoundError(str(command.analysis_id))

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            analysis.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to delete analysis %s",
                command.current_user_id,
                command.analysis_id,
            )
            raise AnalysisNotFoundError(str(command.analysis_id))

        if analysis.status not in {AnalysisStatus.COMPLETED, AnalysisStatus.FAILED}:
            raise AnalysisNotDeletableError(analysis.status.value)

        refs = await self._analysis_repository.get_metrics(analysis.id)
        if refs:
            await self._metrics_remover.delete(refs)

        await self._analysis_repository.delete(analysis.id)
        self._logger.info("Analysis deleted: analysis_id=%s", command.analysis_id)


__all__ = ("DeleteAnalysisUseCase",)
