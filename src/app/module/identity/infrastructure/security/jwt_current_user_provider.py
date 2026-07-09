"""Current user provider from jwt token implementation."""

from typing import TYPE_CHECKING, override

from app.module.identity.application.error import AuthenticationError, UserNotFoundError
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.port import CurrentUserProvider


if TYPE_CHECKING:
    from app.module.identity.application.port import TokenService, UserRepository


class JWTCurrentUserProvider(CurrentUserProvider):
    """Provides current user ID from a JWT token.

    Parameters
    ----------
    token_service : TokenService
        Port for encoding/decoding JWT tokens.
    user_repository : UserRepository
        Port for accessing user data.
    """

    def __init__(
        self,
        token_service: TokenService,
        user_repository: UserRepository,
    ) -> None:
        self._token_service = token_service
        self._user_repository = user_repository

    @override
    async def get_current_user_id(self, token: str) -> str:
        """Resolve a user ID from a JWT token.

        Parameters
        ----------
        token : str
            The raw JWT token string.

        Returns
        -------
        str
            The user ID string.

        Raises
        ------
        AuthenticationError
            If the token is invalid, expired, or malformed.
        UserNotFoundError
            If the user does not exist.
        """
        try:
            payload = self._token_service.verify_token(token)
        except Exception as e:
            message = f"Invalid token: {e!s}"
            raise AuthenticationError(message) from e
        user_id = payload.get("sub")
        if not user_id:
            message = "Token does not contain user ID"
            raise AuthenticationError(message)

        user = await self._user_repository.get_by_id(UserId(user_id))
        if not user:
            raise UserNotFoundError(user_id)

        return user_id


__all__ = ("JWTCurrentUserProvider",)
