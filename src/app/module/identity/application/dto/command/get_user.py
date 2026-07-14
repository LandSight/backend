"""Get user command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetUserCommand:
    """Command for retrieving a user by ID.

    Attributes
    ----------
    user_id : str
        User identifier.
    """

    user_id: str


__all__ = ("GetUserCommand",)
