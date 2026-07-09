"""Token response DTO."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class TokenResponse:
    """DTO for authentication tokens returned from use cases.

    Attributes
    ----------
    access_token : str
        Access token.
    refresh_token : str
        Refresh token.
    token_type : str
        Token type (e.g. ``"Bearer"``).
    """

    access_token: str
    refresh_token: str
    token_type: ClassVar[str] = "Bearer"  # noqa: S105


__all__ = ("TokenResponse",)
