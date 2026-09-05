"""Create parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.parcel.application.dto.command import CreateParcelCommand
from app.module.parcel.application.dto.response import ParcelResponse
from app.module.parcel.domain.entity import Parcel
from app.module.parcel.domain.value_object import OwnerId, ParcelId, ParcelName
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository, PolygonService


class CreateParcelUseCase(BaseUseCase[CreateParcelCommand, ParcelResponse]):
    """Create a new parcel.

    Validates the polygon geometry, creates a parcel entity, and persists it.
    """

    def __init__(
        self,
        parcel_repository: ParcelRepository,
        polygon_service: PolygonService,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._polygon_service = polygon_service
        self._logger = get_logger("app.parcel.use_case.create_parcel")

    @override
    async def __call__(self, command: CreateParcelCommand) -> ParcelResponse:
        self._logger.info("Creating parcel: name=%s", command.name)

        name = ParcelName(command.name)
        polygon = self._polygon_service.to_domain(command.polygon)

        self._polygon_service.validate(polygon)

        parcel_id = ParcelId(uuid6())
        owner_id = OwnerId(command.owner_id)
        parcel = Parcel(id=parcel_id, name=name, polygon=polygon, owner_id=owner_id)

        saved_parcel = await self._parcel_repository.save(parcel)
        saved_polygon = self._polygon_service.from_domain(saved_parcel.polygon)

        self._logger.info("Parcel created: id=%s name=%s", parcel_id, command.name)

        return ParcelResponse(
            id=saved_parcel.id.unwrap(),
            name=saved_parcel.name.unwrap(),
            polygon=saved_polygon,
            owner_id=saved_parcel.owner_id.unwrap(),
        )


__all__ = ("CreateParcelUseCase",)
