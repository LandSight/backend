"""Get user use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.identity.application.dto.command import GetUserCommand
from app.module.identity.application.dto.response import UserResponse
from app.module.identity.application.error import UserNotFoundError
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.identity.application.port import UserRepository


class GetUserUseCase(BaseUseCase[GetUserCommand, UserResponse]):
    """Retrieve a user by their ID."""

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository
        self._logger = get_logger("app.identity.use_case.get_user")

    @override
    async def __call__(self, command: GetUserCommand) -> UserResponse:
        self._logger.info("Getting user: user_id=%s", command.user_id)

        user_id = UserId(command.user_id)

        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            self._logger.warning("User not found: user_id=%s", command.user_id)
            raise UserNotFoundError(str(command.user_id))

        self._logger.info("User retrieved: user_id=%s username=%s", command.user_id, user.username.unwrap())

        return UserResponse(
            id=user.id.unwrap(),
            username=user.username.unwrap(),
        )


__all__ = ("GetUserUseCase",)
