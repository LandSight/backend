"""Refresh token command DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefreshTokenCommand:
    """Command to refresh an access token using a refresh token.

    Attributes
    ----------
    refresh_token : str
        The refresh token.
    """

    refresh_token: str


__all__ = ("RefreshTokenCommand",)
