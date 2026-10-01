"""Get interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.interface.internal.dto import GetAnalysisEvaluationInput
from app.module.interpretation.application.dto.command import GetInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.application.error import InterpretationNotAvailableError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.interface.internal.port import AnalysisInternalAPI
    from app.module.interpretation.application.port import (
        EvaluationBreakdownBuilder,
        InterpretationRepository,
    )
    from app.module.interpretation.application.service import ReportAssembler


class GetInterpretationUseCase(BaseUseCase[GetInterpretationCommand, InterpretationResultResponse]):
    """Read the stored interpretation report of an analysis.

    The evaluation is fetched first so that access rights and the existence of
    a finished evaluation are enforced before reading the report. The report is
    then assembled from the current evaluation and the stored generated text.
    """

    def __init__(
        self,
        analysis_api: AnalysisInternalAPI,
        interpretation_repository: InterpretationRepository,
        breakdown_builder: EvaluationBreakdownBuilder,
        report_assembler: ReportAssembler,
    ) -> None:
        self._analysis_api = analysis_api
        self._repository = interpretation_repository
        self._breakdown_builder = breakdown_builder
        self._assembler = report_assembler
        self._logger = get_logger("app.interpretation.use_case.get")

    @override
    async def __call__(self, command: GetInterpretationCommand) -> InterpretationResultResponse:
        evaluation = await self._analysis_api.get_analysis_evaluation(
            GetAnalysisEvaluationInput(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            ),
        )
        interpretation = await self._repository.get(command.analysis_id)
        if interpretation is None:
            raise InterpretationNotAvailableError(str(command.analysis_id))
        return self._assembler.assemble(self._breakdown_builder.build(evaluation), interpretation)


__all__ = ("GetInterpretationUseCase",)
