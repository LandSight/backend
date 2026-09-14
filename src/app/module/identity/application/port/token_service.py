"""Token service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.identity.domain.value_object import UserId


class TokenService(ABC):
    """Port for token creation and verification.

    Operates on domain :class:`~app.module.identity.domain.value_object.user_id.UserId`
    value object.

    Implementations:
    - :class:`app.module.identity.infrastructure.security.jwt_token_service.JWTTokenService`
    """

    @abstractmethod
    def create_access_token(self, user_id: UserId, claims: dict | None = None) -> str:
        """Create an access token.

        Parameters
        ----------
        user_id : UserId
            User identifier.
        claims : dict | None
            Additional claims to include.

        Returns
        -------
        str
            Encoded access token.
        """
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, user_id: UserId) -> str:
        """Create a refresh token.

        Parameters
        ----------
        user_id : UserId
            User identifier.

        Returns
        -------
        str
            Encoded refresh token.
        """
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """Verify and decode a token.

        Parameters
        ----------
        token : str
            Encoded token string.

        Returns
        -------
        dict
            Decoded token payload containing at least ``sub`` (user ID).

        Raises
        ------
        AuthenticationError
            If the token is expired or invalid.
        """
        raise NotImplementedError


__all__ = ("TokenService",)
