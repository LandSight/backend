"""Token service port."""

from abc import ABC, abstractmethod


class TokenService(ABC):
    """Port for token creation and verification.

    Implementations:
    - :class:`app.module.identity.infrastructure.security.jwt_token_service.JWTTokenService`
    """

    @abstractmethod
    def create_access_token(self, user_id: str, claims: dict | None = None) -> str:
        """Create an access token.

        Parameters
        ----------
        user_id : str
            User identifier to embed in the token.
        claims : dict | None
            Additional claims to include.

        Returns
        -------
        str
            Encoded access token.
        """
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token.

        Parameters
        ----------
        user_id : str
            User identifier to embed in the token.

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
