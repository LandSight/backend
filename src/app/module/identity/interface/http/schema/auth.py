"""Auth HTTP schemas."""

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
    refresh_token: str = Field(description="JWT refresh token.")
    token_type: str = Field(default="Bearer", description="Token type.")


__all__ = (
    "AuthResponse",
    "LoginRequest",
    "RegisterRequest",
)
