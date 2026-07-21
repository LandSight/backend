"""Current user schema for HTTP layer.

This is a Pydantic model used as a Litestar dependency — it represents
the authenticated user resolved from the JWT token. It is intentionally
separate from the internal ``UserResult`` dataclass to keep the HTTP
layer decoupled from module-internal DTOs.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    """Current authenticated user resolved from token.

    Injected into controllers that need access to the authenticated
    user's identity (id, username).
    """

    id: UUID = Field(description="User identifier.")
    username: str = Field(description="Username.")


__all__ = ("CurrentUser",)
