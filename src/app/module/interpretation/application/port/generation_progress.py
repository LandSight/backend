"""Generation progress port."""

from __future__ import annotations

from abc import ABC, abstractmethod


class GenerationProgress(ABC):
    """Receives the progress of a running generation attempt.

    Reporting doubles as the cancellation check: the interpreter reports before
    and after every text, and the implementation raises
    :class:`~app.module.interpretation.application.error.InterpretationCancelledError`
    once the attempt no longer owns the report (it was cancelled, regenerated
    or deleted together with its analysis), so the work stops at the next step.

    Implementations:
    - :class:`app.module.interpretation.application.service.attempt_progress.AttemptProgress`
    """

    @abstractmethod
    async def report(self, done: int, total: int) -> None:
        """Record that ``done`` of ``total`` texts are generated."""
        raise NotImplementedError


__all__ = ("GenerationProgress",)
