"""Current user provider port."""

from abc import ABC, abstractmethod


class CurrentUserProvider(ABC):
    """Port for resolving the current user ID from an authentication token.

    The token is extracted from the HTTP request by the controller layer
    and passed to this port. This keeps the port free of framework
    dependencies (e.g., Litestar's Request object).

    Implementations:
    - :class:`app.module.identity.infrastructure.security.jwt_current_user_provider.JWTCurrentUserProvider`
    """

    @abstractmethod
    async def get_current_user_id(self, token: str) -> str:
        """Resolve a user ID from an authentication token.

        Parameters
        ----------
        token : str
            The raw authentication token (e.g., JWT string).

        Returns
        -------
        str
            The user ID as a string.

        Raises
        ------
        AuthenticationError
            If the token is invalid, expired, or malformed.
        UserNotFoundError
            If the user associated with the token does not exist.
        """
        raise NotImplementedError


__all__ = ("CurrentUserProvider",)
