"""Delete parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.application.dto.command import DeleteParcelCommand
from app.module.parcel.domain.value_object import OwnerId, ParcelId
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.parcel.application.port import (
        ParcelPermissionService,
        ParcelRepository,
    )


class DeleteParcelUseCase(BaseUseCase[DeleteParcelCommand, None]):
    """Delete a parcel by its ID.

    Access is granted only when the current user is allowed to manage it.
    """

    def __init__(
        self,
        parcel_repository: ParcelRepository,
        parcel_permission_service: ParcelPermissionService,
    ) -> None:
        self._parcel_repository = parcel_repository
        self._parcel_permission_service = parcel_permission_service
        self._logger = get_logger("app.parcel.use_case.delete_parcel")

    @override
    async def __call__(self, command: DeleteParcelCommand) -> None:
        self._logger.info("Deleting parcel: id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)
        owner_id = OwnerId(command.current_user_id)

        if not await self._parcel_permission_service.user_can_manage_parcel(owner_id, parcel_id):
            self._logger.warning(
                "User %s is not allowed to manage parcel %s",
                command.current_user_id,
                command.parcel_id,
            )
            reason = f"User cannot manage parcel '{command.parcel_id}'."
            raise ForbiddenError(reason)

        await self._parcel_repository.delete(parcel_id)

        self._logger.info("Parcel deleted: id=%s", command.parcel_id)


__all__ = ("DeleteParcelUseCase",)
