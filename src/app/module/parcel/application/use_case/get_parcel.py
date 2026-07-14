"""Get parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.parcel.application.dto.command import GetParcelCommand
from app.module.parcel.application.dto.response import ParcelResponse
from app.module.parcel.application.error import ParcelNotFoundError
from app.module.parcel.domain.value_object import ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository, PolygonService


class GetParcelUseCase(BaseUseCase[GetParcelCommand, ParcelResponse]):
    """Retrieve a parcel by its ID."""

    def __init__(
        self,
        parcel_repository: ParcelRepository,
        polygon_service: PolygonService,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._polygon_service = polygon_service
        self._logger = get_logger("app.parcel.use_case.get_parcel")

    @override
    async def __call__(self, command: GetParcelCommand) -> ParcelResponse:
        self._logger.info("Getting parcel: id=%s", command.parcel_id)

        parcel_id = ParcelId(UUID(command.parcel_id))
        parcel = await self._parcel_repository.get_by_id(parcel_id)

        if parcel is None:
            self._logger.warning("Parcel not found: id=%s", command.parcel_id)
            raise ParcelNotFoundError(command.parcel_id)

        self._logger.info("Parcel found: id=%s name=%s", command.parcel_id, parcel.name.unwrap())

        return ParcelResponse(
            id=str(parcel.id.unwrap()),
            name=parcel.name.unwrap(),
            polygon=self._polygon_service.from_domain(parcel.polygon),
            owner_id=str(parcel.owner_id),
        )


__all__ = ("GetParcelUseCase",)
