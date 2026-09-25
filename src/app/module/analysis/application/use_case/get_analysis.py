"""Get analysis use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import GetAnalysisCommand
from app.module.analysis.application.dto.response import AnalysisResponse
from app.module.analysis.application.error import AnalysisNotFoundError
from app.module.analysis.domain.value_object import AnalysisId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from typing import NoReturn
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
        OwnedParcelsProvider,
    )
    from app.module.analysis.domain.entity import Analysis


class GetAnalysisUseCase(BaseUseCase[GetAnalysisCommand, AnalysisResponse]):
    """Retrieve an analysis by its ID.

    Access is granted only when the current user owns the underlying parcel.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
        owned_parcels_provider: OwnedParcelsProvider,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._owned_parcels_provider = owned_parcels_provider
        self._logger = get_logger("app.analysis.use_case.get_analysis")

    @override
    async def __call__(self, command: GetAnalysisCommand) -> AnalysisResponse:
        self._logger.info("Getting analysis: analysis_id=%s", command.analysis_id)

        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            self._raise_not_found(command.analysis_id)

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            analysis.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to view analysis %s",
                command.current_user_id,
                command.analysis_id,
            )
            self._raise_not_found(command.analysis_id)

        parcels = await self._owned_parcels_provider.list_owned_parcels(command.current_user_id)
        return self._to_response(analysis, parcels.get(analysis.parcel_id.unwrap()))

    @staticmethod
    def _raise_not_found(analysis_id: UUID) -> NoReturn:
        """Raise a not-found error for the given analysis ID."""
        raise AnalysisNotFoundError(str(analysis_id))

    @staticmethod
    def _to_response(analysis: Analysis, parcel_name: str | None) -> AnalysisResponse:
        """Map a domain entity to a response DTO."""
        return AnalysisResponse(
            id=analysis.id.unwrap(),
            parcel_id=analysis.parcel_id.unwrap(),
            parcel_name=parcel_name,
            name=analysis.name.unwrap(),
            analysis_type=analysis.analysis_type.value,
            status=analysis.status.value,
            stage=analysis.stage.value,
            score=analysis.score.unwrap() if analysis.score is not None else None,
            model_version=analysis.model_version,
            status_reason=analysis.status_reason,
            created_at=analysis.created_at,
            completed_at=analysis.completed_at,
        )


__all__ = ("GetAnalysisUseCase",)
