"""Analysis task queue port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import AnalysisId


class AnalysisTaskQueue(ABC):
    """Port for scheduling analysis processing.

    Implementations:
    - :class:`app.module.analysis.infrastructure.queue.celery_analysis_task_queue.CeleryAnalysisTaskQueue`
    """

    @abstractmethod
    async def enqueue(self, analysis_id: AnalysisId, current_user_id: UUID) -> None:
        """Schedule processing for an analysis.

        Parameters
        ----------
        analysis_id : AnalysisId
            ID of the analysis to process.
        current_user_id : UUID
            ID of the user who requested the analysis. Passed to metric modules
            by the worker, which has no HTTP request context of its own.
        """
        raise NotImplementedError


__all__ = ("AnalysisTaskQueue",)
