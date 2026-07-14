"""Register user use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.identity.application.dto.command import RegisterUserCommand
from app.module.identity.application.dto.response import UserResponse
from app.module.identity.application.error import UserAlreadyExistsError
from app.module.identity.domain.entity import User
from app.module.identity.domain.value_object import (
    Password,
    UserId,
    Username,
)
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


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
        self._logger = get_logger("app.identity.use_case.register_user")

    @override
    async def __call__(self, command: RegisterUserCommand) -> UserResponse:
        username = Username(command.username)
        password = Password(command.password)

        self._logger.info("Registering user: username=%s", command.username)

        existing_username = await self._user_repository.get_by_username(username)
        if existing_username is not None:
            self._logger.warning("Registration failed: username already exists: %s", command.username)
            raise UserAlreadyExistsError(command.username)

        user_id = UserId(uuid6())
        hashed = self._password_hasher.hash(password)

        user = User(id=user_id, username=username, hashed_password=hashed)

        await self._user_repository.save(user)

        self._logger.info("User registered successfully: id=%s username=%s", user_id, command.username)

        return UserResponse(
            id=str(user.id.unwrap()),
            username=username.unwrap(),
        )


__all__ = ("RegisterUserUseCase",)
