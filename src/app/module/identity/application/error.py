"""Identity module application errors."""

from app.module.shared.application.error import ApplicationError


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid username or password.") -> None:
        super().__init__(message)


class UserNotFoundError(ApplicationError):
    """Raised when a user is not found."""

    def __init__(self, user_id: str) -> None:
        super().__init__(f"User with id '{user_id}' not found.")


class UserAlreadyExistsError(ApplicationError):
    """Raised when a user with the given username already exists."""

    def __init__(self, username: str) -> None:
        super().__init__(f"User with username '{username}' already exists.")


class RefreshTokenInvalidError(AuthenticationError):
    """Raised when refresh token is invalid or expired."""

    default_message = "Invalid or expired refresh token"


class RefreshTokenTypeError(AuthenticationError):
    """Raised when token is not a refresh token."""

    default_message = "Invalid token type"


class RefreshTokenPayloadError(AuthenticationError):
    """Raised when refresh token payload is invalid."""

    default_message = "Invalid token payload"


__all__ = (
    "AuthenticationError",
    "UserAlreadyExistsError",
    "UserNotFoundError",
)
