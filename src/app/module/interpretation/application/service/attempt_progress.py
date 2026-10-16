"""Progress of one generation attempt, stored on the report."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.interpretation.application.error import InterpretationCancelledError
from app.module.interpretation.application.port import GenerationProgress


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.application.port import InterpretationRepository
    from app.module.shared.application.port import UnitOfWork


class AttemptProgress(GenerationProgress):
    """Writes the progress of an attempt to its report and detects cancellation.

    Every report is a conditional update committed at once, so clients polling
    the report see the progress while the worker runs. When the update finds
    no report running under the attempt, the attempt was cancelled, regenerated
    or deleted, and the generation stops.
    """

    def __init__(
        self,
        repository: InterpretationRepository,
        unit_of_work: UnitOfWork,
        analysis_id: UUID,
        attempt_id: UUID,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._analysis_id = analysis_id
        self._attempt_id = attempt_id

    @override
    async def report(self, done: int, total: int) -> None:
        """See :class:`app.module.interpretation.application.port.GenerationProgress.report`."""
        current = await self._repository.update_progress(self._analysis_id, self._attempt_id, done, total)
        await self._unit_of_work.commit()
        if not current:
            raise InterpretationCancelledError(str(self._analysis_id))


__all__ = ("AttemptProgress",)
