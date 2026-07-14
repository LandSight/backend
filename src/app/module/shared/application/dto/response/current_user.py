"""Current user response DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrentUser:
    """Response DTO representing the currently authenticated user.

    This is a lightweight, framework-agnostic representation of the
    authenticated user that can be used across all modules without
    creating a dependency on the identity module.

    Attributes
    ----------
    id : str
        Unique identifier of the user.
    username : str
        Username of the user.
    """

    id: str
    username: str


__all__ = ("CurrentUser",)
