"""Analysis task queue port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import AnalysisId


class AnalysisTaskQueue(ABC):
    """Port for scheduling analysis processing.

    Implementations:
    - :class:`app.module.analysis.infrastructure.queue.noop_analysis_task_queue.NoopAnalysisTaskQueue` (MVP)
    """

    @abstractmethod
    async def enqueue(self, analysis_id: AnalysisId) -> None:
        """Schedule processing for an analysis.

        Parameters
        ----------
        analysis_id : AnalysisId
            ID of the analysis to process.
        """
        raise NotImplementedError


__all__ = ("AnalysisTaskQueue",)
