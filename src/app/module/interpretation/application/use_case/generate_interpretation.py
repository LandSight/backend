"""Generate interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.analysis.interface.internal.dto import GetAnalysisEvaluationInput
from app.module.interpretation.application.dto.command import GenerateInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.value_object import InterpretationId, InterpretationStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.interface.internal.port import AnalysisInternalAPI
    from app.module.interpretation.application.port import (
        EvaluationBreakdownBuilder,
        InterpretationRepository,
        Interpreter,
    )
    from app.module.interpretation.application.service import ReportAssembler
    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class GenerateInterpretationUseCase(
    BaseUseCase[GenerateInterpretationCommand, InterpretationResultResponse],
):
    """Generate the interpretation report of an analysis.

    Generation always produces a fresh report and replaces any stored one. The
    use case owns the business flow: reading the evaluation through the analysis
    internal API (which enforces access rights), building the breakdown,
    delegating generation to the interpreter and persisting the report. The
    generation strategy itself (LLM, templates, ...) lives behind the
    :class:`Interpreter` port.
    """

    def __init__(
        self,
        analysis_api: AnalysisInternalAPI,
        interpretation_repository: InterpretationRepository,
        breakdown_builder: EvaluationBreakdownBuilder,
        interpreter: Interpreter,
        report_assembler: ReportAssembler,
    ) -> None:
        self._analysis_api = analysis_api
        self._repository = interpretation_repository
        self._breakdown_builder = breakdown_builder
        self._interpreter = interpreter
        self._assembler = report_assembler
        self._logger = get_logger("app.interpretation.use_case.generate")

    @override
    async def __call__(self, command: GenerateInterpretationCommand) -> InterpretationResultResponse:
        self._logger.info("Generating interpretation: analysis_id=%s", command.analysis_id)

        breakdown = await self._load_breakdown(command)
        existing = await self._repository.get(command.analysis_id)
        generated = await self._interpreter.explain(command.analysis_id, breakdown)
        # The report row is created once (as ordered) and updated in place on
        # every regeneration, so the stored row keeps its identity.
        interpretation = Interpretation(
            id=existing.id if existing is not None else InterpretationId(uuid6()),
            analysis_id=command.analysis_id,
            model=generated.model,
            summary=generated.summary,
            explanations=generated.explanations,
            status=InterpretationStatus.COMPLETED,
        )
        saved = await self._repository.save(interpretation)
        return self._assembler.assemble(breakdown, saved)

    async def _load_breakdown(self, command: GenerateInterpretationCommand) -> EvaluationBreakdown:
        """Read the evaluation through the analysis API and flatten it."""
        evaluation = await self._analysis_api.get_analysis_evaluation(
            GetAnalysisEvaluationInput(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            ),
        )
        return self._breakdown_builder.build(evaluation)


__all__ = ("GenerateInterpretationUseCase",)
