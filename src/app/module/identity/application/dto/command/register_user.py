"""Register user command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    """Command for registering a new user.

    Attributes
    ----------
    username : str
        Desired username.
    password : str
        Plain-text password.
    """

    username: str
    password: str


__all__ = ("RegisterUserCommand",)
