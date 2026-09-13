"""Collect analysis metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import (
    CollectMetricsCommand,
    FailAnalysisCommand,
)
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object import AnalysisId, AnalysisStatus, MetricType
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisRepository,
        MetricsCollector,
        UnitOfWork,
    )
    from app.module.analysis.application.use_case.fail_analysis import FailAnalysisUseCase
    from app.module.analysis.domain.value_object import AnalysisMetricRef


class CollectMetricsUseCase(BaseUseCase[CollectMetricsCommand, None]):
    """Calculate one metric module's data and record its references.

    Runs as part of the metrics phase. On error it rolls back and records the
    failure in a separate transaction, then re-raises so the pipeline stops.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        metrics_collector: MetricsCollector,
        fail_analysis_use_case: FailAnalysisUseCase,
        unit_of_work: UnitOfWork,
        infrastructure_buffers: dict[str, int],
    ) -> None:
        self._analysis_repository = analysis_repository
        self._metrics_collector = metrics_collector
        self._fail_analysis_use_case = fail_analysis_use_case
        self._unit_of_work = unit_of_work
        self._infrastructure_buffers = infrastructure_buffers
        self._logger = get_logger("app.analysis.use_case.collect_metrics")

    @override
    async def __call__(self, command: CollectMetricsCommand) -> None:
        try:
            await self._execute(command)
        except Exception as exc:
            await self._record_failure(command.analysis_id, exc)
            raise

    async def _execute(self, command: CollectMetricsCommand) -> None:
        """Run the happy path for one metrics module."""
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            raise AnalysisNotFoundError(str(command.analysis_id))

        if analysis.status not in {AnalysisStatus.PENDING, AnalysisStatus.RUNNING}:
            self._logger.warning(
                "Analysis is not in progress, skipping metrics: analysis_id=%s status=%s",
                command.analysis_id,
                analysis.status,
            )
            await self._unit_of_work.commit()
            return

        self._logger.info(
            "Collecting %s metrics: analysis_id=%s",
            command.metric_type,
            command.analysis_id,
        )

        refs = await self._collect(command.metric_type, analysis.parcel_id.unwrap(), command.current_user_id)
        await self._analysis_repository.save_metrics(analysis.id, refs)
        await self._unit_of_work.commit()

    async def _record_failure(self, analysis_id: UUID, error: Exception) -> None:
        """Roll back and persist the failure in a fresh transaction."""
        await self._unit_of_work.rollback()
        await self._fail_analysis_use_case(
            FailAnalysisCommand(analysis_id=analysis_id, reason=str(error)),
        )
        await self._unit_of_work.commit()

    async def _collect(
        self,
        metric_type: MetricType,
        parcel_id: UUID,
        user_id: UUID,
    ) -> list[AnalysisMetricRef]:
        """Dispatch to the collector method for the requested metric module."""
        match metric_type:
            case MetricType.TOPOGRAPHY:
                return [await self._metrics_collector.collect_topography(parcel_id, user_id)]
            case MetricType.CLIMATE:
                return [await self._metrics_collector.collect_climate(parcel_id, user_id)]
            case MetricType.INFRASTRUCTURE:
                return await self._metrics_collector.collect_infrastructure(
                    parcel_id,
                    user_id,
                    self._infrastructure_buffers,
                )


__all__ = ("CollectMetricsUseCase",)
