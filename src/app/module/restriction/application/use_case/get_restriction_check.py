"""Get restriction check use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.restriction.application.dto.command import GetRestrictionCheckCommand
from app.module.restriction.application.dto.response import RestrictionCheckResponse
from app.module.restriction.application.error import RestrictionCheckNotFoundError
from app.module.restriction.application.use_case._mapping import to_check_response
from app.module.restriction.domain.value_object import RestrictionCheckId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.restriction.application.port import CheckRepository, RestrictionPermissionService


class GetRestrictionCheckUseCase(BaseUseCase[GetRestrictionCheckCommand, RestrictionCheckResponse]):
    """Retrieve a restriction check snapshot by its ID.

    Access is granted only when the current user owns the underlying parcel.
    """

    def __init__(
        self,
        check_repository: CheckRepository,
        permission_service: RestrictionPermissionService,
    ) -> None:
        self._check_repository = check_repository
        self._permission_service = permission_service
        self._logger = get_logger("app.restriction.use_case.get_restriction_check")

    @override
    async def __call__(self, command: GetRestrictionCheckCommand) -> RestrictionCheckResponse:
        check = await self._check_repository.get(RestrictionCheckId(command.check_id))
        if check is None:
            self._logger.warning("Restriction check not found: check_id=%s", command.check_id)
            raise RestrictionCheckNotFoundError(str(command.check_id))

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            check.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to view restriction check %s",
                command.current_user_id,
                command.check_id,
            )
            raise RestrictionCheckNotFoundError(str(command.check_id))

        return to_check_response(check)


__all__ = ("GetRestrictionCheckUseCase",)
