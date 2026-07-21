"""Delete parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.application.dto.command import DeleteParcelCommand
from app.module.parcel.application.error import NotParcelOwnerError, ParcelNotFoundError
from app.module.parcel.domain.value_object import OwnerId, ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import ParcelRepository


class DeleteParcelUseCase(BaseUseCase[DeleteParcelCommand, None]):
    """Delete a parcel by its ID.

    Only the owner of the parcel can delete it.
    """

    def __init__(
        self,
        parcel_repository: ParcelRepository,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._logger = get_logger("app.parcel.use_case.delete_parcel")

    @override
    async def __call__(self, command: DeleteParcelCommand) -> None:
        self._logger.info("Deleting parcel: id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)
        parcel = await self._parcel_repository.get_by_id(parcel_id)

        if parcel is None:
            self._logger.warning("Parcel not found for deletion: id=%s", command.parcel_id)
            raise ParcelNotFoundError(str(command.parcel_id))

        current_user_id = OwnerId(command.current_user_id)
        if parcel.owner_id != current_user_id:
            self._logger.warning(
                "User %s is not the owner of parcel %s",
                command.current_user_id,
                command.parcel_id,
            )
            raise NotParcelOwnerError(str(command.parcel_id))

        await self._parcel_repository.delete(parcel_id)

        self._logger.info("Parcel deleted: id=%s", command.parcel_id)


__all__ = ("DeleteParcelUseCase",)
