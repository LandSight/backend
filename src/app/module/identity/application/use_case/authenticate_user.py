"""Authenticate user use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.identity.application.dto.command import AuthenticateUserCommand
from app.module.identity.application.dto.response import TokenResponse
from app.module.identity.application.error import AuthenticationError
from app.module.identity.domain.value_object import (
    Password,
    Username,
)
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.identity.application.port import (
        PasswordHasher,
        TokenService,
        UserRepository,
    )


class AuthenticateUserUseCase(BaseUseCase[AuthenticateUserCommand, TokenResponse]):
    """Authenticate a user by username and password.

    Verifies credentials and returns JWT tokens.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._logger = get_logger("app.identity.use_case.authenticate_user")

    @override
    async def __call__(self, command: AuthenticateUserCommand) -> TokenResponse:
        username = Username(command.username)
        password = Password(command.password)

        self._logger.info("Authentication attempt: username=%s", command.username)

        user = await self._user_repository.get_by_username(username)
        if user is None:
            self._logger.warning("Authentication failed: user not found: %s", command.username)
            raise AuthenticationError

        if not self._password_hasher.verify(password, user.hashed_password):
            self._logger.warning("Authentication failed: invalid password: %s", command.username)
            raise AuthenticationError

        access_token = self._token_service.create_access_token(user.id)
        refresh_token = self._token_service.create_refresh_token(user.id)

        self._logger.info("Authentication successful: username=%s", command.username)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )


__all__ = ("AuthenticateUserUseCase",)
