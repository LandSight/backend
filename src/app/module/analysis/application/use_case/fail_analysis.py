"""Fail analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import FailAnalysisCommand
from app.module.analysis.domain.value_object import AnalysisId, AnalysisStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import AnalysisRepository


class FailAnalysisUseCase(BaseUseCase[FailAnalysisCommand, None]):
    """Mark a pending or running analysis as failed.

    Used by the worker to record failures in a transaction separate from the
    one that was rolled back.
    """

    _MAX_REASON_LENGTH = 512

    def __init__(self, analysis_repository: AnalysisRepository) -> None:
        self._analysis_repository = analysis_repository
        self._logger = get_logger("app.analysis.use_case.fail_analysis")

    @override
    async def __call__(self, command: FailAnalysisCommand) -> None:
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            self._logger.warning("Analysis not found for failure marking: analysis_id=%s", command.analysis_id)
            return

        if analysis.status not in {AnalysisStatus.PENDING, AnalysisStatus.RUNNING}:
            self._logger.warning(
                "Analysis already finished, not marking failed: analysis_id=%s status=%s",
                command.analysis_id,
                analysis.status,
            )
            return

        reason = command.reason.strip() or "Analysis failed."
        analysis.fail(reason[: self._MAX_REASON_LENGTH])
        await self._analysis_repository.save(analysis)
        self._logger.info("Analysis marked as failed: analysis_id=%s", command.analysis_id)


__all__ = ("FailAnalysisUseCase",)
