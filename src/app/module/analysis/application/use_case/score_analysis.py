"""Score analysis use case."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import ScoreAnalysisCommand
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object.analysis import (
    AnalysisId,
    AnalysisStage,
    AnalysisStatus,
    AnalysisStatusReason,
)
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisRepository,
        AnalysisScorer,
        ConstraintEvaluator,
        InterpretationService,
        MetricsService,
        RestrictionService,
    )
    from app.module.shared.application.port import UnitOfWork


class ScoreAnalysisUseCase(BaseUseCase[ScoreAnalysisCommand, None]):
    """Score an analysis whose metrics are ready and persist the result.

    Runs as the final pipeline phase. On error it rolls back and records the
    failure in a separate transaction, then re-raises.

    The interpretation report is started in the same transaction through the
    ``InterpretationService`` port, so clients never see a completed analysis
    without its report row; If starting the interpretation
    fails, the analysis is still completed and committed (the report can be
    generated manually), so a transient failure does not roll back scoring.
    """

    _DEMO_STEP_DELAY_SECONDS = 5

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        metrics_service: MetricsService,
        scorer: AnalysisScorer,
        unit_of_work: UnitOfWork,
        interpretation_service: InterpretationService,
        restriction_service: RestrictionService,
        constraint_evaluator: ConstraintEvaluator,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._metrics_service = metrics_service
        self._restriction_service = restriction_service
        self._constraint_evaluator = constraint_evaluator
        self._scorer = scorer
        self._unit_of_work = unit_of_work
        self._interpretation_service = interpretation_service
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
            # Demo-only delay so the "running" state stays visible.
            await asyncio.sleep(self._DEMO_STEP_DELAY_SECONDS)
            analysis.mark_metrics_calculated()
            await self._analysis_repository.save(analysis)
            # Commit the stage transition so "scoring" is observable.
            await self._unit_of_work.commit()
            # Demo-only delay so the "scoring" state stays visible.
            await asyncio.sleep(self._DEMO_STEP_DELAY_SECONDS)

        refs = await self._analysis_repository.get_metrics(analysis.id)
        metrics = await self._metrics_service.get_metrics(analysis.parcel_id.unwrap(), refs, command.current_user_id)
        # Two independent levels: the scorer rates the parcel from its metrics,
        # then the constraints bar the scenario or lower that score.
        evaluation = self._scorer.evaluate(
            command.analysis_id,
            metrics,
            analysis.analysis_type,
            analysis.engine,
        )
        # Analyses started before restrictions existed have no check.
        restriction_check = await self._analysis_repository.get_restriction_check(analysis.id)
        if restriction_check is not None:
            check = await self._restriction_service.get(restriction_check, command.current_user_id)
            evaluation.apply_constraints(self._constraint_evaluator.evaluate(analysis.analysis_type, check.hits))
        analysis.complete(evaluation.total_score, evaluation.model_version)
        await self._analysis_repository.save(analysis)
        await self._analysis_repository.save_evaluation(evaluation)
        # Start the report in the same transaction: the ordered row and the
        # ``interpretation_started`` outbox event commit together with the
        # completed analysis, so there is no relay hop in between.
        try:
            await self._interpretation_service.start(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            )
        except Exception:
            # The analysis stays completed without the report row; the user can
            # start the report manually. This mirrors the pre-refactor behavior
            # where the relay could fail to order the report.
            self._logger.exception(
                "Failed to start interpretation, analysis stays completed: analysis_id=%s",
                command.analysis_id,
            )
        await self._unit_of_work.commit()

        self._logger.info(
            "Analysis scored: analysis_id=%s score=%s base_score=%s constraints=%s model_version=%s",
            command.analysis_id,
            evaluation.total_score.unwrap(),
            evaluation.base_score.unwrap(),
            [constraint.kind for constraint in evaluation.applied_constraints],
            evaluation.model_version,
        )

    async def _record_failure(self, analysis_id: UUID, error: Exception) -> None:
        """Log the error, roll back and persist a user-safe failure reason in a fresh transaction."""
        self._logger.error("Analysis scoring failed: analysis_id=%s", analysis_id, exc_info=error)
        await self._unit_of_work.rollback()
        analysis = await self._analysis_repository.get(AnalysisId(analysis_id))
        if analysis is not None and analysis.status in {AnalysisStatus.PENDING, AnalysisStatus.RUNNING}:
            analysis.fail(AnalysisStatusReason.scoring_failed())
            await self._analysis_repository.save(analysis)
            await self._unit_of_work.commit()


__all__ = ("ScoreAnalysisUseCase",)
