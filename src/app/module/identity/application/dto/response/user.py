"""User response DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserResponse:
    """DTO for user data returned from use cases.

    Attributes
    ----------
    id : str
        User identifier.
    username : str
        Username.
    """

    id: str
    username: str


__all__ = ("UserResponse",)
