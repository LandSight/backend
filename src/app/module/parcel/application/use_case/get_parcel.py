"""Get parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.application.dto.command import GetParcelCommand
from app.module.parcel.application.dto.response import ParcelResponse
from app.module.parcel.application.error import NotParcelOwnerError, ParcelNotFoundError
from app.module.parcel.domain.value_object import OwnerId, ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository, PolygonService


class GetParcelUseCase(BaseUseCase[GetParcelCommand, ParcelResponse]):
    """Retrieve a parcel by its ID.

    Only the owner of the parcel can retrieve it.
    """

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

        parcel_id = ParcelId(command.parcel_id)
        parcel = await self._parcel_repository.get_by_id(parcel_id)

        if parcel is None:
            self._logger.warning("Parcel not found: id=%s", command.parcel_id)
            raise ParcelNotFoundError(str(command.parcel_id))

        current_user_id = OwnerId(command.current_user_id)
        if parcel.owner_id != current_user_id:
            self._logger.warning(
                "User %s is not the owner of parcel %s",
                command.current_user_id,
                command.parcel_id,
            )
            raise NotParcelOwnerError(str(command.parcel_id))

        self._logger.info("Parcel found: id=%s name=%s", command.parcel_id, parcel.name.unwrap())

        return ParcelResponse(
            id=parcel.id.unwrap(),
            name=parcel.name.unwrap(),
            polygon=self._polygon_service.from_domain(parcel.polygon),
            owner_id=parcel.owner_id.unwrap(),
        )


__all__ = ("GetParcelUseCase",)
