"""No-op analysis task queue (MVP placeholder)."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import AnalysisTaskQueue
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import AnalysisId


class NoopAnalysisTaskQueue(AnalysisTaskQueue):
    """Task queue that only logs enqueued analyses.

    Temporary implementation used until the Celery + Redis queue is wired in.
    """

    def __init__(self) -> None:
        self._logger = get_logger("app.analysis.infrastructure.noop_task_queue")

    @override
    async def enqueue(self, analysis_id: AnalysisId) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisTaskQueue.enqueue`."""
        self._logger.info("Analysis enqueued (no-op queue): analysis_id=%s", analysis_id.unwrap())


__all__ = ("NoopAnalysisTaskQueue",)
