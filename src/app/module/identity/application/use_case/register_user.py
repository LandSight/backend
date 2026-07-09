"""Register user use case."""

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.identity.application.dto.command import RegisterUserCommand
from app.module.identity.application.dto.response import UserResponse
from app.module.identity.application.error import UserAlreadyExistsError
from app.module.identity.domain.entity import User
from app.module.identity.domain.value_object import (
    HashedPassword,
    Password,
    UserId,
    Username,
)
from app.module.shared.application.use_case import BaseUseCase


if TYPE_CHECKING:
    from app.module.identity.application.port import (
        PasswordHasher,
        UserRepository,
    )


class RegisterUserUseCase(BaseUseCase[RegisterUserCommand, UserResponse]):
    """Register a new user.

    Creates a user entity, hashes the password, and persists it.
    Validates that the username is unique and the password meets security requirements.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    @override
    async def __call__(self, command: RegisterUserCommand) -> UserResponse:
        username = Username(command.username)
        password = Password(command.password)

        existing_username = await self._user_repository.get_by_username(username)
        if existing_username is not None:
            raise UserAlreadyExistsError(command.username)

        user_id = UserId(uuid6())
        hashed = HashedPassword(self._password_hasher.hash(password.unwrap()))

        user = User(id=user_id, username=username, hashed_password=hashed)

        await self._user_repository.save(user)

        return UserResponse(
            id=str(user.id.unwrap()),
            username=username.unwrap(),
        )


__all__ = ("RegisterUserUseCase",)
