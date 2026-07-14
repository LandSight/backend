"""User HTTP schemas."""

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """Response body for user data."""

    id: str = Field(description="User identifier.")
    username: str = Field(description="Username.")


__all__ = ("UserResponse",)
