"""Celery-backed analysis task queue.

The metrics phase runs as a ``group`` of independent module tasks; the scoring
phase is its ``chord`` callback. Chords require a result backend, which is why
Celery results are enabled.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from celery import chord, group

from app.module.analysis.application.port import AnalysisTaskQueue


if TYPE_CHECKING:
    from uuid import UUID

    from celery import Celery
    from celery.canvas import Signature

    from app.module.analysis.domain.value_object import AnalysisId


CALCULATE_TOPOGRAPHY_TASK_NAME = "analysis.calculate_topography_metrics"
CALCULATE_CLIMATE_TASK_NAME = "analysis.calculate_climate_metrics"
CALCULATE_INFRASTRUCTURE_TASK_NAME = "analysis.calculate_infrastructure_metrics"
SCORE_ANALYSIS_TASK_NAME = "analysis.score_analysis"


class CeleryAnalysisTaskQueue(AnalysisTaskQueue):
    """Analysis task queue backed by Celery + Redis.

    Enqueues a chord: a group of metrics tasks followed by the scoring task.
    """

    def __init__(self, celery_app: Celery) -> None:
        self._celery_app = celery_app

    @override
    async def enqueue(self, analysis_id: AnalysisId, current_user_id: UUID) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisTaskQueue.enqueue`."""
        analysis = str(analysis_id.unwrap())
        user = str(current_user_id)

        header = group(
            self._signature(CALCULATE_TOPOGRAPHY_TASK_NAME, analysis, user),
            self._signature(CALCULATE_CLIMATE_TASK_NAME, analysis, user),
            self._signature(CALCULATE_INFRASTRUCTURE_TASK_NAME, analysis, user),
        )
        callback = self._signature(SCORE_ANALYSIS_TASK_NAME, analysis, user)
        chord(header)(callback)

    def _signature(self, name: str, analysis_id: str, user_id: str) -> Signature:
        """Build an immutable signature for a task by name."""
        return self._celery_app.signature(name, args=[analysis_id, user_id], immutable=True)


__all__ = (
    "CALCULATE_CLIMATE_TASK_NAME",
    "CALCULATE_INFRASTRUCTURE_TASK_NAME",
    "CALCULATE_TOPOGRAPHY_TASK_NAME",
    "SCORE_ANALYSIS_TASK_NAME",
    "CeleryAnalysisTaskQueue",
)
