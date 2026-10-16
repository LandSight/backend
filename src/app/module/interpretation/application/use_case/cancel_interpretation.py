"""Cancel interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.interpretation.application.dto.command import CancelInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.application.error import InterpretationNotAvailableError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.interpretation.application.port import AnalysisService, InterpretationRepository


class CancelInterpretationUseCase(BaseUseCase[CancelInterpretationCommand, InterpretationResultResponse]):
    """Cancel the generation of an interpretation report.

    An ordered or running report is marked ``cancelled`` and loses its
    generation attempt. Nothing is sent to the worker: a queued task skips a
    report that is no longer ordered, and a running one stops at its next
    progress report, which finds the report no longer running under its
    attempt. A finished report is left as is, so cancelling is idempotent.
    """

    def __init__(
        self,
        interpretation_repository: InterpretationRepository,
        analysis_service: AnalysisService,
    ) -> None:
        self._repository = interpretation_repository
        self._analysis_service = analysis_service
        self._logger = get_logger("app.interpretation.use_case.cancel")

    @override
    async def __call__(self, command: CancelInterpretationCommand) -> InterpretationResultResponse:
        # Reading the evaluation enforces the access rights, like reading the report.
        await self._analysis_service.read(command.analysis_id, command.current_user_id)
        report = await self._repository.get(command.analysis_id)
        if report is None:
            raise InterpretationNotAvailableError(str(command.analysis_id))
        if report.cancel():
            await self._repository.save(report)
            self._logger.info("Interpretation cancelled: analysis_id=%s", command.analysis_id)
        return InterpretationResultResponse(status=report.status)


__all__ = ("CancelInterpretationUseCase",)
