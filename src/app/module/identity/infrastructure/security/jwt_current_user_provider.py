"""Current user provider from jwt token implementation."""

from typing import TYPE_CHECKING, override
from uuid import UUID

from app.module.identity.application.error import AuthenticationError, UserNotFoundError
from app.module.identity.domain.value_object import UserId
from app.module.shared.application.dto.response import CurrentUser
from app.module.shared.application.port import CurrentUserProvider
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.identity.application.port import TokenService, UserRepository


class JWTCurrentUserProvider(CurrentUserProvider):
    """Provides current user from a JWT token.

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
        self._logger = get_logger("app.identity.infrastructure.jwt_current_user_provider")

    @override
    async def get_current_user(self, token: str) -> CurrentUser:
        """Resolve a current user from a JWT token.

        Parameters
        ----------
        token : str
            The raw JWT token string.

        Returns
        -------
        CurrentUser
            The authenticated user's id and username.

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
            self._logger.warning("Token verification failed: %s", e)
            message = f"Invalid token: {e!s}"
            raise AuthenticationError(message) from e

        user_id = payload.get("sub")
        if not user_id:
            self._logger.warning("Token does not contain user ID")
            message = "Token does not contain user ID"
            raise AuthenticationError(message)

        user = await self._user_repository.get_by_id(UserId(UUID(user_id)))
        if not user:
            self._logger.warning("User from token not found: user_id=%s", user_id)
            raise UserNotFoundError(user_id)

        self._logger.info("Token verified successfully: user_id=%s", user_id)
        return CurrentUser(id=user_id, username=user.username.unwrap())


__all__ = ("JWTCurrentUserProvider",)
