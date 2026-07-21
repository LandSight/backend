"""Identity HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """Request body for user registration."""

    username: str = Field(description="Username.")
    password: str = Field(description="Password.")


class LoginRequest(BaseModel):
    """Request body for user login."""

    username: str = Field(description="Username.")
    password: str = Field(description="Password.")


class AuthResponse(BaseModel):
    """Response body for authentication endpoints."""

    access_token: str = Field(description="JWT access token.")
    token_type: str = Field(default="Bearer", description="Token type.")


class UserResponse(BaseModel):
    """Response body for user data."""

    id: UUID = Field(description="User identifier.")
    username: str = Field(description="Username.")


__all__ = (
    "AuthResponse",
    "LoginRequest",
    "RegisterRequest",
    "UserResponse",
)
