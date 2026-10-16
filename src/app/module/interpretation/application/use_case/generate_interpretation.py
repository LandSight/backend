"""Generate interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.interpretation.application.dto.command import GenerateInterpretationCommand
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.value_object import InterpretationId, InterpretationStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.application.port import (
        AnalysisService,
        InterpretationRepository,
        Interpreter,
    )
    from app.module.shared.application.port import UnitOfWork


class GenerateInterpretationUseCase(BaseUseCase[GenerateInterpretationCommand, None]):
    """Generate the interpretation report of an analysis.

    The use case owns the report lifecycle, mirroring how the analysis pipeline
    phases work: the report is marked ``running`` and committed before the LLM
    work begins, then replaced by the completed report, and on error it is
    rolled back and persisted as ``failed``. Generation always produces a fresh
    report and replaces any stored one, but only when the stored report is
    ``ordered``: a report that is already running, completed or failed belongs
    to another attempt and is left untouched (the outbox relay and an explicit
    user order can enqueue the same analysis twice).
    """

    def __init__(
        self,
        interpretation_repository: InterpretationRepository,
        analysis_service: AnalysisService,
        interpreter: Interpreter,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = interpretation_repository
        self._analysis_service = analysis_service
        self._interpreter = interpreter
        self._unit_of_work = unit_of_work
        self._logger = get_logger("app.interpretation.use_case.generate")

    @override
    async def __call__(self, command: GenerateInterpretationCommand) -> None:
        try:
            await self._execute(command)
        except Exception as exc:
            await self._record_failure(command.analysis_id, exc)
            raise

    async def _execute(self, command: GenerateInterpretationCommand) -> None:
        """Run the happy path for the generation phase."""
        self._logger.info("Generating interpretation: analysis_id=%s", command.analysis_id)

        report = await self._repository.get(command.analysis_id)
        if report is None:
            # The report row may be missing when the relay raced ahead of the
            # ordered placeholder; create it, mirroring the outbox handler.
            report = Interpretation(
                id=InterpretationId(uuid6()),
                analysis_id=command.analysis_id,
                model="",
                summary="",
                status=InterpretationStatus.ORDERED,
            )
        elif report.status is not InterpretationStatus.ORDERED:
            # Idempotency guard: a report that is already running, completed or
            # failed belongs to another attempt, so this one must not clobber it.
            self._logger.warning(
                "Skipping interpretation generation: analysis_id=%s status=%s",
                command.analysis_id,
                report.status.value,
            )
            await self._unit_of_work.commit()
            return

        report.mark_running()
        await self._repository.save(report)
        # Commit the running status so clients see it while the LLM works.
        await self._unit_of_work.commit()

        breakdown = await self._analysis_service.read(command.analysis_id, command.current_user_id)
        generated = await self._interpreter.explain(command.analysis_id, breakdown)
        # The report row is created once (as ordered) and updated in place on
        # every regeneration, so the stored row keeps its identity.
        completed = Interpretation(
            id=report.id,
            analysis_id=command.analysis_id,
            model=generated.model,
            summary=generated.summary,
            explanations=generated.explanations,
            constraints_explanation=generated.constraints_explanation,
            status=InterpretationStatus.COMPLETED,
        )
        await self._repository.save(completed)
        await self._unit_of_work.commit()

    async def _record_failure(self, analysis_id: UUID, error: Exception) -> None:
        """Roll back and persist the failure in a fresh transaction."""
        self._logger.warning(
            "Interpretation generation failed: analysis_id=%s error=%s",
            analysis_id,
            error,
        )
        await self._unit_of_work.rollback()
        report = await self._repository.get(analysis_id)
        if report is not None and report.status in {
            InterpretationStatus.ORDERED,
            InterpretationStatus.RUNNING,
        }:
            report.fail()
            await self._repository.save(report)
            await self._unit_of_work.commit()


__all__ = ("GenerateInterpretationUseCase",)
