"""Celery tasks for the analysis pipeline.

An analysis is processed end to end by a single task: it collects the metrics
for every module and then scores the analysis. This keeps the pipeline of one
analysis together, so with a single worker an earlier analysis finishes before
the next one starts.
"""

from __future__ import annotations

from uuid import UUID

from celery.signals import worker_process_init

from app.module.analysis.application.dto.command import CollectMetricsCommand, ScoreAnalysisCommand
from app.module.analysis.di import COLLECT_METRICS_USE_CASE_KEY, SCORE_ANALYSIS_USE_CASE_KEY
from app.module.analysis.domain.value_object import MetricType
from app.module.analysis.infrastructure.queue.celery_analysis_task_queue import (
    PROCESS_ANALYSIS_TASK_NAME,
)
from app.platform.config.loaders import load_logging_config
from app.platform.logging import configure_logging
from app.worker.celery_app import celery_app
from app.worker.container import WorkerContainer, get_session_factory, run_in_worker_loop


_METRIC_MODULES = (MetricType.TOPOGRAPHY, MetricType.CLIMATE, MetricType.INFRASTRUCTURE)


@worker_process_init.connect
def _configure_worker_logging(**_: object) -> None:
    """Configure logging in each forked worker process."""
    configure_logging(load_logging_config())


@celery_app.task(name=PROCESS_ANALYSIS_TASK_NAME)
def process_analysis(analysis_id: str, current_user_id: str) -> None:
    """Process one analysis end to end: collect metrics, then score."""
    run_in_worker_loop(_process(analysis_id, current_user_id))


async def _process(analysis_id: str, current_user_id: str) -> None:
    """Run the full analysis pipeline for one analysis."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        container = WorkerContainer(session)
        collect = container.resolve(COLLECT_METRICS_USE_CASE_KEY)
        score = container.resolve(SCORE_ANALYSIS_USE_CASE_KEY)

        analysis_id_value = UUID(analysis_id)
        user_id_value = UUID(current_user_id)

        for metric_type in _METRIC_MODULES:
            await collect(
                CollectMetricsCommand(
                    analysis_id=analysis_id_value,
                    current_user_id=user_id_value,
                    metric_type=metric_type,
                )
            )

        await score(
            ScoreAnalysisCommand(
                analysis_id=analysis_id_value,
                current_user_id=user_id_value,
            )
        )


__all__ = ("process_analysis",)
