"""List user parcels use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.parcel.application.dto.command import ListUserParcelsCommand
from app.module.parcel.application.dto.response import ParcelResponse
from app.module.parcel.domain.value_object import OwnerId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository, PolygonService


class ListUserParcelsUseCase(BaseUseCase[ListUserParcelsCommand, list[ParcelResponse]]):
    """Retrieve all parcels owned by a specific user."""

    def __init__(
        self,
        parcel_repository: ParcelRepository,
        polygon_service: PolygonService,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._polygon_service = polygon_service
        self._logger = get_logger("app.parcel.use_case.list_user_parcels")

    @override
    async def __call__(self, command: ListUserParcelsCommand) -> list[ParcelResponse]:
        self._logger.info("Listing parcels for owner: id=%s", command.owner_id)

        owner_id = OwnerId(UUID(command.owner_id))
        parcels = await self._parcel_repository.get_by_owner_id(owner_id)

        self._logger.info("Found %d parcels for owner: id=%s", len(parcels), command.owner_id)

        return [
            ParcelResponse(
                id=str(parcel.id.unwrap()),
                name=parcel.name.unwrap(),
                polygon=self._polygon_service.from_domain(parcel.polygon),
                owner_id=str(parcel.owner_id.unwrap()),
            )
            for parcel in parcels
        ]


__all__ = ("ListUserParcelsUseCase",)
