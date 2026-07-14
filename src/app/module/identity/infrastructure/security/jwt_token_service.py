"""JWT token service implementation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, override

import jwt

from app.module.identity.application.port import TokenService


if TYPE_CHECKING:
    from app.module.identity.domain.value_object import UserId
    from app.platform.config.models import AuthConfig


class JWTTokenService(TokenService):
    """Create and verify JWT tokens using PyJWT."""

    def __init__(self, config: AuthConfig) -> None:
        self._config = config

    @override
    def create_access_token(self, user_id: UserId, claims: dict | None = None) -> str:
        """See :class:`app.module.identity.application.port.TokenService.create_access_token`."""
        payload = {
            "sub": str(user_id.unwrap()),
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=self._config.access_token_expire_minutes),
            "type": "access",
        }
        if claims:
            payload.update(claims)

        return jwt.encode(payload, self._config.secret_key.get_secret_value(), algorithm=self._config.algorithm)

    @override
    def create_refresh_token(self, user_id: UserId) -> str:
        """See :class:`app.module.identity.application.port.TokenService.create_refresh_token`."""
        payload = {
            "sub": str(user_id.unwrap()),
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(days=self._config.refresh_token_expire_days),
            "type": "refresh",
        }

        return jwt.encode(payload, self._config.secret_key.get_secret_value(), algorithm=self._config.algorithm)

    @override
    def verify_token(self, token: str) -> dict:
        """See :class:`app.module.identity.application.port.TokenService.verify_token`."""
        return jwt.decode(
            token,
            self._config.secret_key.get_secret_value(),
            algorithms=[self._config.algorithm],
        )


__all__ = ("JWTTokenService",)
