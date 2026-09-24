"""Celery-backed analysis task queue.

An analysis is processed by a single task that runs the whole pipeline
(collect every metric module, then score) sequentially. This keeps the work of
one analysis together, so with a single worker an earlier analysis finishes
completely before the next one starts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import AnalysisTaskQueue


if TYPE_CHECKING:
    from uuid import UUID

    from celery import Celery

    from app.module.analysis.domain.value_object import AnalysisId


PROCESS_ANALYSIS_TASK_NAME = "analysis.process_analysis"


class CeleryAnalysisTaskQueue(AnalysisTaskQueue):
    """Analysis task queue backed by Celery + Redis.

    Enqueues one task per analysis that processes it end to end.
    """

    def __init__(self, celery_app: Celery) -> None:
        self._celery_app = celery_app

    @override
    async def enqueue(self, analysis_id: AnalysisId, current_user_id: UUID) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisTaskQueue.enqueue`."""
        self._celery_app.send_task(
            PROCESS_ANALYSIS_TASK_NAME,
            args=[str(analysis_id.unwrap()), str(current_user_id)],
        )


__all__ = ("PROCESS_ANALYSIS_TASK_NAME", "CeleryAnalysisTaskQueue")
