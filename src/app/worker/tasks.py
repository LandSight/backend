"""Celery tasks for the analysis pipeline.

The pipeline is a chord: a group of per-module metrics tasks, followed by a
scoring task. Each task opens its own session; transaction boundaries are
managed by the use cases through the unit-of-work port.
"""

from __future__ import annotations

from uuid import UUID

from celery.signals import worker_process_init

from app.module.analysis.application.dto.command import CollectMetricsCommand, ScoreAnalysisCommand
from app.module.analysis.di import COLLECT_METRICS_USE_CASE_KEY, SCORE_ANALYSIS_USE_CASE_KEY
from app.module.analysis.domain.value_object import MetricType
from app.module.analysis.infrastructure.queue.celery_analysis_task_queue import (
    CALCULATE_CLIMATE_TASK_NAME,
    CALCULATE_INFRASTRUCTURE_TASK_NAME,
    CALCULATE_TOPOGRAPHY_TASK_NAME,
    SCORE_ANALYSIS_TASK_NAME,
)
from app.platform.config.loaders import load_logging_config
from app.platform.logging import configure_logging
from app.worker.celery_app import celery_app
from app.worker.container import WorkerContainer, get_session_factory, run_in_worker_loop


@worker_process_init.connect
def _configure_worker_logging(**_: object) -> None:
    """Configure logging in each forked worker process."""
    configure_logging(load_logging_config())


@celery_app.task(name=CALCULATE_TOPOGRAPHY_TASK_NAME)
def calculate_topography_metrics(analysis_id: str, current_user_id: str) -> None:
    """Calculate and record the analysis' topography metrics."""
    run_in_worker_loop(_collect(MetricType.TOPOGRAPHY, analysis_id, current_user_id))


@celery_app.task(name=CALCULATE_CLIMATE_TASK_NAME)
def calculate_climate_metrics(analysis_id: str, current_user_id: str) -> None:
    """Calculate and record the analysis' climate metrics."""
    run_in_worker_loop(_collect(MetricType.CLIMATE, analysis_id, current_user_id))


@celery_app.task(name=CALCULATE_INFRASTRUCTURE_TASK_NAME)
def calculate_infrastructure_metrics(analysis_id: str, current_user_id: str) -> None:
    """Calculate and record the analysis' infrastructure metrics."""
    run_in_worker_loop(_collect(MetricType.INFRASTRUCTURE, analysis_id, current_user_id))


@celery_app.task(name=SCORE_ANALYSIS_TASK_NAME)
def score_analysis(analysis_id: str, current_user_id: str) -> None:
    """Score the analysis after all metrics have been calculated."""
    run_in_worker_loop(_score(analysis_id, current_user_id))


async def _collect(metric_type: MetricType, analysis_id: str, current_user_id: str) -> None:
    """Run the metrics-collection use case for one module."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        use_case = WorkerContainer(session).resolve(COLLECT_METRICS_USE_CASE_KEY)
        await use_case(
            CollectMetricsCommand(
                analysis_id=UUID(analysis_id),
                current_user_id=UUID(current_user_id),
                metric_type=metric_type,
            ),
        )


async def _score(analysis_id: str, current_user_id: str) -> None:
    """Run the scoring use case."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        use_case = WorkerContainer(session).resolve(SCORE_ANALYSIS_USE_CASE_KEY)
        await use_case(
            ScoreAnalysisCommand(
                analysis_id=UUID(analysis_id),
                current_user_id=UUID(current_user_id),
            ),
        )


__all__ = (
    "calculate_climate_metrics",
    "calculate_infrastructure_metrics",
    "calculate_topography_metrics",
    "score_analysis",
)
