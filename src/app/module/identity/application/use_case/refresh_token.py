"""Refresh token use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.identity.application.dto.command import RefreshTokenCommand
from app.module.identity.application.dto.response import TokenResponse
from app.module.identity.application.error import (
    RefreshTokenInvalidError,
    RefreshTokenPayloadError,
    RefreshTokenTypeError,
)
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.identity.application.port import TokenService


class RefreshTokenUseCase(BaseUseCase[RefreshTokenCommand, TokenResponse]):
    """Refresh an access token using a refresh token.

    Verifies the refresh token, extracts the user ID, and issues
    a new access token and a new refresh token (token rotation).
    """

    def __init__(
        self,
        token_service: TokenService,
    ) -> None:
        self._token_service = token_service
        self._logger = get_logger("app.identity.use_case.refresh_token")

    @override
    async def __call__(self, command: RefreshTokenCommand) -> TokenResponse:
        self._logger.info("Refreshing token")

        try:
            payload = self._token_service.verify_token(command.refresh_token)
        except Exception as e:
            self._logger.warning("Refresh token verification failed: %s", e)
            raise RefreshTokenInvalidError from e

        if payload.get("type") != "refresh":
            self._logger.warning("Token is not a refresh token")
            raise RefreshTokenTypeError

        user_id_str = payload.get("sub")
        if not user_id_str:
            self._logger.warning("Refresh token does not contain user ID")
            raise RefreshTokenPayloadError

        user_id = UserId(UUID(user_id_str))

        access_token = self._token_service.create_access_token(user_id)
        refresh_token = self._token_service.create_refresh_token(user_id)

        self._logger.info("Token refreshed successfully: user_id=%s", user_id_str)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )


__all__ = ("RefreshTokenUseCase",)
