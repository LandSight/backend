"""Delete parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.parcel.application.dto.command import DeleteParcelCommand
from app.module.parcel.application.error import ParcelNotFoundError
from app.module.parcel.domain.value_object import ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository


class DeleteParcelUseCase(BaseUseCase[DeleteParcelCommand, None]):
    """Delete a parcel by its ID."""

    def __init__(
        self,
        parcel_repository: ParcelRepository,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._logger = get_logger("app.parcel.use_case.delete_parcel")

    @override
    async def __call__(self, command: DeleteParcelCommand) -> None:
        self._logger.info("Deleting parcel: id=%s", command.parcel_id)

        parcel_id = ParcelId(UUID(command.parcel_id))
        parcel = await self._parcel_repository.get_by_id(parcel_id)

        if parcel is None:
            self._logger.warning("Parcel not found for deletion: id=%s", command.parcel_id)
            raise ParcelNotFoundError(command.parcel_id)

        await self._parcel_repository.delete(parcel_id)

        self._logger.info("Parcel deleted: id=%s", command.parcel_id)


__all__ = ("DeleteParcelUseCase",)
