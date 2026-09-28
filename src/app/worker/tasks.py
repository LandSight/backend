"""Celery tasks for the analysis pipeline.

An analysis is processed end to end by a single task: it collects the metrics
for every module and then scores the analysis. This keeps the pipeline of one
analysis together, so with a single worker an earlier analysis finishes before
the next one starts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from celery.signals import worker_process_init

from app.module.analysis.application.dto.command import CollectMetricsCommand, ScoreAnalysisCommand
from app.module.analysis.di import COLLECT_METRICS_USE_CASE_KEY, SCORE_ANALYSIS_USE_CASE_KEY
from app.module.analysis.domain.event import ANALYSIS_DELETED_EVENT, metric_refs_from_payload
from app.module.analysis.domain.value_object import MetricType
from app.module.analysis.infrastructure.queue.celery_analysis_task_queue import (
    PROCESS_ANALYSIS_TASK_NAME,
)
from app.platform.config.loaders import load_logging_config
from app.platform.logging import configure_logging, get_logger
from app.platform.outbox import OutboxDrainer
from app.platform.outbox.constants import DRAIN_OUTBOX_TASK_NAME
from app.worker.celery_app import celery_app
from app.worker.container import WorkerContainer, get_session_factory, run_in_worker_loop


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.application.port import MetricsRemover
    from app.platform.outbox.repository import OutboxRepository


_METRIC_MODULES = (MetricType.TOPOGRAPHY, MetricType.CLIMATE, MetricType.INFRASTRUCTURE)

logger = get_logger("app.worker.tasks")


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


@celery_app.task(name=DRAIN_OUTBOX_TASK_NAME)
def drain_outbox() -> None:
    """Relay pending transactional-outbox events to their handlers."""
    run_in_worker_loop(_drain_outbox())


async def _drain_outbox() -> None:
    """Dispatch pending outbox events within a single transaction."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        container = WorkerContainer(session)
        repository: OutboxRepository = container.resolve("outbox_repository")
        metrics_remover: MetricsRemover = container.resolve("metrics_remover")

        async def handle_analysis_deleted(payload: Mapping[str, object]) -> None:
            await metrics_remover.delete(list(metric_refs_from_payload(payload)))

        drainer = OutboxDrainer(repository, {ANALYSIS_DELETED_EVENT: handle_analysis_deleted})
        processed = await drainer.drain()
        await session.commit()

        if processed:
            logger.info("Outbox drained: processed=%s", processed)


__all__ = ("drain_outbox", "process_analysis")
