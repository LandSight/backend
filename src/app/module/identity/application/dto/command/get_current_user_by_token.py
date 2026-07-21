"""Get current user by token command DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetCurrentUserByTokenCommand:
    """Command to resolve the current user from an authentication token.

    Attributes
    ----------
    token : str
        Raw authentication token (e.g., JWT string).
    """

    token: str


__all__ = ("GetCurrentUserByTokenCommand",)
