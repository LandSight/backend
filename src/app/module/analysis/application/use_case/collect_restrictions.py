"""Collect analysis restrictions use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import CollectRestrictionsCommand
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object.analysis import AnalysisId, AnalysisStatus, AnalysisStatusReason
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port import AnalysisRepository, RestrictionService
    from app.module.shared.application.port import UnitOfWork


class CollectRestrictionsUseCase(BaseUseCase[CollectRestrictionsCommand, None]):
    """Check the restrictions on the analysed parcel and record the snapshot.

    Runs after the metrics, before scoring. Restrictions are not metrics: they
    are applied to the multi-criteria score as prohibitions and penalties, so
    the snapshot is kept apart from the metric references. On error it rolls
    back and records the failure in a separate transaction, then re-raises so
    the pipeline stops.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        restriction_service: RestrictionService,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._restriction_service = restriction_service
        self._unit_of_work = unit_of_work
        self._logger = get_logger("app.analysis.use_case.collect_restrictions")

    @override
    async def __call__(self, command: CollectRestrictionsCommand) -> None:
        try:
            await self._execute(command)
        except Exception as exc:
            await self._record_failure(command.analysis_id, exc)
            raise

    async def _execute(self, command: CollectRestrictionsCommand) -> None:
        """Run the happy path for the restriction check."""
        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            raise AnalysisNotFoundError(str(command.analysis_id))

        if analysis.status is not AnalysisStatus.RUNNING:
            self._logger.warning(
                "Analysis is not running, skipping restrictions: analysis_id=%s status=%s",
                command.analysis_id,
                analysis.status,
            )
            await self._unit_of_work.commit()
            return

        self._logger.info("Checking restrictions: analysis_id=%s", command.analysis_id)
        ref = await self._restriction_service.calculate(analysis.parcel_id.unwrap(), command.current_user_id)
        await self._analysis_repository.save_restriction_check(analysis.id, ref)
        await self._unit_of_work.commit()

    async def _record_failure(self, analysis_id: UUID, error: Exception) -> None:
        """Log the error, roll back and persist a user-safe failure reason in a fresh transaction."""
        self._logger.error("Restriction check failed: analysis_id=%s", analysis_id, exc_info=error)
        await self._unit_of_work.rollback()
        analysis = await self._analysis_repository.get(AnalysisId(analysis_id))
        if analysis is not None and analysis.status in {AnalysisStatus.PENDING, AnalysisStatus.RUNNING}:
            analysis.fail(AnalysisStatusReason.restrictions_check_failed())
            await self._analysis_repository.save(analysis)
            await self._unit_of_work.commit()


__all__ = ("CollectRestrictionsUseCase",)
