"""List user analyses use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import ListUserAnalysesCommand
from app.module.analysis.application.dto.response import AnalysisResponse
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import (
        AnalysisRepository,
        OwnedParcelsProvider,
    )
    from app.module.analysis.domain.entity import Analysis


class ListUserAnalysesUseCase(BaseUseCase[ListUserAnalysesCommand, list[AnalysisResponse]]):
    """List all analyses of the current user across all statuses.

    Ownership is resolved through the Parcel module: only analyses of parcels
    owned by the user are returned.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        owned_parcels_provider: OwnedParcelsProvider,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._owned_parcels_provider = owned_parcels_provider
        self._logger = get_logger("app.analysis.use_case.list_user_analyses")

    @override
    async def __call__(self, command: ListUserAnalysesCommand) -> list[AnalysisResponse]:
        self._logger.info("Listing analyses: user_id=%s", command.current_user_id)

        parcel_ids = await self._owned_parcels_provider.list_owned_parcel_ids(command.current_user_id)
        analyses = await self._analysis_repository.list_by_parcel_ids(parcel_ids)

        self._logger.info("Analyses listed: user_id=%s count=%s", command.current_user_id, len(analyses))

        return [self._to_response(analysis) for analysis in analyses]

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


__all__ = ("ListUserAnalysesUseCase",)
