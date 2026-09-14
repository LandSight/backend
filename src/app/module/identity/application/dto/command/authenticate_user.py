"""Authenticate user command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthenticateUserCommand:
    """Command for authenticating a user.

    Attributes
    ----------
    username : str
        Username.
    password : str
        Plain-text password.
    """

    username: str
    password: str


__all__ = ("AuthenticateUserCommand",)
