"""Start analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.analysis.application.dto.command import StartAnalysisCommand
from app.module.analysis.application.dto.response import AnalysisResponse
from app.module.analysis.domain.entity import Analysis
from app.module.analysis.domain.value_object import AnalysisId, AnalysisName, ParcelId
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
        AnalysisTaskQueue,
    )


class StartAnalysisUseCase(BaseUseCase[StartAnalysisCommand, AnalysisResponse]):
    """Start an analysis for a parcel.

    Creates a ``PENDING`` analysis, persists it and enqueues it for processing.
    The actual metric aggregation and scoring run in a worker (see the queue
    port).
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
        task_queue: AnalysisTaskQueue,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._task_queue = task_queue
        self._logger = get_logger("app.analysis.use_case.start_analysis")

    @override
    async def __call__(self, command: StartAnalysisCommand) -> AnalysisResponse:
        self._logger.info("Starting analysis: parcel_id=%s", command.parcel_id)

        if not await self._permission_service.user_can_view_parcel(command.current_user_id, command.parcel_id):
            reason = f"User is not allowed to analyze parcel '{command.parcel_id}'"
            raise ForbiddenError(reason)

        analysis = Analysis(
            id=AnalysisId(uuid6()),
            parcel_id=ParcelId(command.parcel_id),
            name=AnalysisName(command.name),
        )
        saved = await self._analysis_repository.save(analysis)
        await self._task_queue.enqueue(saved.id)

        self._logger.info("Analysis started: analysis_id=%s parcel_id=%s", saved.id, saved.parcel_id)

        return self._to_response(saved)

    @staticmethod
    def _to_response(analysis: Analysis) -> AnalysisResponse:
        """Map a domain entity to a response DTO."""
        return AnalysisResponse(
            id=analysis.id.unwrap(),
            parcel_id=analysis.parcel_id.unwrap(),
            name=analysis.name.unwrap(),
            status=analysis.status.value,
            score=analysis.score.unwrap() if analysis.score is not None else None,
            status_reason=analysis.status_reason,
            created_at=analysis.created_at,
        )


__all__ = ("StartAnalysisUseCase",)
