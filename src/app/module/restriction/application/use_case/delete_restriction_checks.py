"""Delete restriction checks use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.restriction.application.dto.command import DeleteRestrictionChecksCommand
from app.module.restriction.application.error import RestrictionCheckNotFoundError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.restriction.application.port import CheckRepository, RestrictionPermissionService


class DeleteRestrictionChecksUseCase(BaseUseCase[DeleteRestrictionChecksCommand, None]):
    """Delete restriction check snapshots by their IDs.

    Used by owning modules (e.g. Analysis) to clean up snapshots they no longer
    reference. Every check must belong to a parcel of the current user;
    otherwise nothing is deleted and the foreign check is reported as not
    found, so its existence is not revealed. Checks that are already gone (for
    example, removed with their parcel) are skipped.
    """

    def __init__(
        self,
        check_repository: CheckRepository,
        permission_service: RestrictionPermissionService,
    ) -> None:
        self._check_repository = check_repository
        self._permission_service = permission_service
        self._logger = get_logger("app.restriction.use_case.delete_restriction_checks")

    @override
    async def __call__(self, command: DeleteRestrictionChecksCommand) -> None:
        parcel_ids = await self._check_repository.get_parcel_ids(command.check_ids)

        for parcel_id in set(parcel_ids.values()):
            if not await self._permission_service.user_can_view_parcel(command.current_user_id, parcel_id):
                denied = next(check_id for check_id, owner in parcel_ids.items() if owner == parcel_id)
                self._logger.warning(
                    "User %s is not allowed to delete restriction check %s",
                    command.current_user_id,
                    denied,
                )
                raise RestrictionCheckNotFoundError(str(denied))

        await self._check_repository.delete(list(parcel_ids))


__all__ = ("DeleteRestrictionChecksUseCase",)
