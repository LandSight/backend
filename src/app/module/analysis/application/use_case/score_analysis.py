"""Score analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import FailAnalysisCommand, ScoreAnalysisCommand
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object import AnalysisId, AnalysisStage, AnalysisStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisRepository,
        AnalysisScorer,
        MetricsReader,
        UnitOfWork,
    )
    from app.module.analysis.application.use_case.fail_analysis import FailAnalysisUseCase


class ScoreAnalysisUseCase(BaseUseCase[ScoreAnalysisCommand, None]):
    """Score an analysis whose metrics are ready and persist the result.

    Runs as the final pipeline phase. On error it rolls back and records the
    failure in a separate transaction, then re-raises.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        metrics_reader: MetricsReader,
        scorer: AnalysisScorer,
        fail_analysis_use_case: FailAnalysisUseCase,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._metrics_reader = metrics_reader
        self._scorer = scorer
        self._fail_analysis_use_case = fail_analysis_use_case
        self._unit_of_work = unit_of_work
        self._logger = get_logger("app.analysis.use_case.score_analysis")

    @override
    async def __call__(self, command: ScoreAnalysisCommand) -> None:
        try:
            await self._execute(command)
        except Exception as exc:
            await self._record_failure(command.analysis_id, exc)
            raise

    async def _execute(self, command: ScoreAnalysisCommand) -> None:
        """Run the happy path for the scoring phase."""
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            raise AnalysisNotFoundError(str(command.analysis_id))

        if analysis.status is not AnalysisStatus.RUNNING:
            self._logger.warning(
                "Analysis is not running, skipping scoring: analysis_id=%s status=%s",
                command.analysis_id,
                analysis.status,
            )
            await self._unit_of_work.commit()
            return

        if analysis.stage is AnalysisStage.METRICS:
            analysis.mark_metrics_calculated()

        refs = await self._analysis_repository.get_metrics(analysis.id)
        values = await self._metrics_reader.read(analysis.parcel_id.unwrap(), refs, command.current_user_id)
        score = self._scorer.score(values)
        analysis.complete(score)
        await self._analysis_repository.save(analysis)
        await self._unit_of_work.commit()

        self._logger.info("Analysis scored: analysis_id=%s score=%s", command.analysis_id, score.unwrap())

    async def _record_failure(self, analysis_id: UUID, error: Exception) -> None:
        """Roll back and persist the failure in a fresh transaction."""
        await self._unit_of_work.rollback()
        await self._fail_analysis_use_case(
            FailAnalysisCommand(analysis_id=analysis_id, reason=str(error)),
        )
        await self._unit_of_work.commit()


__all__ = ("ScoreAnalysisUseCase",)
