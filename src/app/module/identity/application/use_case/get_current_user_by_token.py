"""Get current user by token use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.identity.application.dto.command import GetCurrentUserByTokenCommand
from app.module.identity.application.dto.response import UserResponse
from app.module.identity.application.error import AuthenticationError, UserNotFoundError
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.identity.application.port import TokenService, UserRepository


class GetCurrentUserByTokenUseCase(BaseUseCase[GetCurrentUserByTokenCommand, UserResponse]):
    """Resolve the current user from an authentication token."""

    def __init__(
        self,
        token_service: TokenService,
        user_repository: UserRepository,
    ) -> None:
        self._token_service = token_service
        self._user_repository = user_repository
        self._logger = get_logger("app.identity.use_case.get_current_user_by_token")

    @override
    async def __call__(self, command: GetCurrentUserByTokenCommand) -> UserResponse:
        try:
            payload = self._token_service.verify_token(command.token)
        except Exception as e:
            self._logger.warning("Token verification failed: %s", e)
            message = f"Invalid token: {e!s}"
            raise AuthenticationError(message) from e

        user_id_str = payload.get("sub")
        if not user_id_str:
            self._logger.warning("Token does not contain user ID")
            message = "Token does not contain user ID"
            raise AuthenticationError(message)

        user_id = UUID(user_id_str)
        user = await self._user_repository.get_by_id(UserId(user_id))
        if not user:
            self._logger.warning("User from token not found: user_id=%s", user_id_str)
            raise UserNotFoundError(user_id_str)

        self._logger.info("Token verified successfully: user_id=%s", user_id_str)

        return UserResponse(id=user_id, username=user.username.unwrap())


__all__ = ("GetCurrentUserByTokenUseCase",)
