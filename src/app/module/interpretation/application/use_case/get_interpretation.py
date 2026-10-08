"""Get interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.interpretation.application.dto.command import GetInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.application.error import InterpretationNotAvailableError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.interpretation.application.port import (
        AnalysisService,
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
        interpretation_repository: InterpretationRepository,
        analysis_service: AnalysisService,
        report_assembler: ReportAssembler,
    ) -> None:
        self._repository = interpretation_repository
        self._analysis_service = analysis_service
        self._assembler = report_assembler
        self._logger = get_logger("app.interpretation.use_case.get")

    @override
    async def __call__(self, command: GetInterpretationCommand) -> InterpretationResultResponse:
        breakdown = await self._analysis_service.read(command.analysis_id, command.current_user_id)
        interpretation = await self._repository.get(command.analysis_id)
        if interpretation is None:
            raise InterpretationNotAvailableError(str(command.analysis_id))
        return self._assembler.assemble(breakdown, interpretation)


__all__ = ("GetInterpretationUseCase",)
