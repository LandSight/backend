"""Get user use case."""

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.identity.application.dto.command import GetUserCommand
from app.module.identity.application.dto.response import UserResponse
from app.module.identity.application.error import UserNotFoundError
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.use_case import BaseUseCase


if TYPE_CHECKING:
    from app.module.identity.application.port import UserRepository


class GetUserUseCase(BaseUseCase[GetUserCommand, UserResponse]):
    """Retrieve a user by their ID."""

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    @override
    async def __call__(self, command: GetUserCommand) -> UserResponse:
        user_id = UserId(UUID(command.user_id))

        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(command.user_id)

        return UserResponse(
            id=str(user.id.unwrap()),
            username=user.username.unwrap(),
        )


__all__ = ("GetUserUseCase",)
