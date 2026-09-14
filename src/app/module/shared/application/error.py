class ApplicationError(Exception):
    """Base class for application errors."""


class ForbiddenError(ApplicationError):
    """Raised when the user is not allowed to perform the requested action."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


__all__ = ("ApplicationError", "ForbiddenError")
