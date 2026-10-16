"""Interpretation task queue port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class InterpretationTaskQueue(ABC):
    """Port for scheduling interpretation report generation.

    Implementations:
    - :class:`app.module.interpretation.infrastructure.queue.celery_interpretation_task_queue.CeleryInterpretationTaskQueue`
    """

    @abstractmethod
    async def enqueue(self, analysis_id: UUID, current_user_id: UUID) -> None:
        """Schedule generation of the interpretation report for an analysis."""
        raise NotImplementedError


__all__ = ("InterpretationTaskQueue",)
