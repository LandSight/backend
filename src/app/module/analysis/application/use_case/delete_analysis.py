"""Delete analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import DeleteAnalysisCommand
from app.module.analysis.application.error import (
    AnalysisNotDeletableError,
    AnalysisNotFoundError,
)
from app.module.analysis.domain.event import ANALYSIS_DELETED_EVENT, AnalysisDeletedEvent
from app.module.analysis.domain.value_object import AnalysisId, AnalysisStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
    )
    from app.module.shared.application.port import EventPublisher


class DeleteAnalysisUseCase(BaseUseCase[DeleteAnalysisCommand, None]):
    """Delete an analysis and schedule cleanup of its metric snapshots.

    Access is granted only when the current user owns the underlying parcel.
    Metric snapshots are parcel-owned, so they are not removed inline: an
    ``AnalysisDeleted`` event is written to the transactional outbox in the same
    transaction, and a relay removes the snapshots through the metric modules.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
        event_publisher: EventPublisher,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._event_publisher = event_publisher
        self._logger = get_logger("app.analysis.use_case.delete_analysis")

    @override
    async def __call__(self, command: DeleteAnalysisCommand) -> None:
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            raise AnalysisNotFoundError(str(command.analysis_id))

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            analysis.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to delete analysis %s",
                command.current_user_id,
                command.analysis_id,
            )
            raise AnalysisNotFoundError(str(command.analysis_id))

        if analysis.status not in {AnalysisStatus.COMPLETED, AnalysisStatus.FAILED}:
            raise AnalysisNotDeletableError(analysis.status.value)

        refs = await self._analysis_repository.get_metrics(analysis.id)
        if refs:
            await self._event_publisher.publish(
                ANALYSIS_DELETED_EVENT,
                AnalysisDeletedEvent(analysis_id=analysis.id, metrics=tuple(refs)).to_payload(),
            )

        await self._analysis_repository.delete(analysis.id)
        self._logger.info("Analysis deleted: analysis_id=%s", command.analysis_id)


__all__ = ("DeleteAnalysisUseCase",)
