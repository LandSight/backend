"""Auth HTTP endpoints."""

from __future__ import annotations

from typing import Annotated

from litestar import Response, post
from litestar.controller import Controller
from litestar.datastructures import Cookie
from litestar.params import CookieParameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.identity import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.module.identity.interface.internal.dto import (
    LoginInput,
    RefreshTokenInput,
    RegisterUserInput,
)
from app.module.identity.interface.internal.port import IdentityInternalAPI
from app.platform.config.loaders import load_auth_config


class AuthController(Controller):
    """Authentication endpoints."""

    path = "/auth"
    tags = ("auth",)

    @post(
        "/register",
        status_code=HTTP_201_CREATED,
        description="Register a new user.",
    )
    async def register(
        self,
        data: RegisterRequest,
        identity_api: IdentityInternalAPI,
    ) -> UserResponse:
        """Register a new user."""
        result = await identity_api.register(
            RegisterUserInput(
                username=data.username,
                password=data.password,
            )
        )
        return UserResponse(id=result.id, username=result.username)

    @post(
        "/login",
        status_code=HTTP_200_OK,
        description="Authenticate a user and return JWT tokens.",
    )
    async def login(
        self,
        data: LoginRequest,
        identity_api: IdentityInternalAPI,
    ) -> Response[AuthResponse]:
        """Authenticate a user by username and password."""
        result = await identity_api.login(
            LoginInput(
                username=data.username,
                password=data.password,
            )
        )

        auth_config = load_auth_config()
        refresh_max_age = auth_config.refresh_token_expire_days * 24 * 60 * 60

        return Response(
            status_code=HTTP_200_OK,
            media_type="application/json",
            content=AuthResponse(
                access_token=result.access_token,
                token_type=result.token_type,
            ),
            cookies=[
                Cookie(
                    key="refresh_token",
                    value=result.refresh_token,
                    max_age=refresh_max_age,
                    httponly=True,
                    secure=auth_config.cookie_secure,
                    samesite="lax",
                    path="/api/v1/identity/auth/refresh",
                )
            ],
        )

    @post(
        "/refresh",
        status_code=HTTP_200_OK,
        description="Refresh access token using a refresh token.",
    )
    async def refresh(
        self,
        identity_api: IdentityInternalAPI,
        refresh_token: Annotated[str, CookieParameter(name="refresh_token", required=True)],
    ) -> Response[AuthResponse]:
        """Refresh an access token."""
        result = await identity_api.refresh_token(RefreshTokenInput(refresh_token=refresh_token))

        auth_config = load_auth_config()
        refresh_max_age = auth_config.refresh_token_expire_days * 24 * 60 * 60

        return Response(
            status_code=HTTP_200_OK,
            media_type="application/json",
            content=AuthResponse(
                access_token=result.access_token,
                token_type=result.token_type,
            ),
            cookies=[
                Cookie(
                    key="refresh_token",
                    value=result.refresh_token,
                    max_age=refresh_max_age,
                    httponly=True,
                    secure=auth_config.cookie_secure,
                    samesite="lax",
                    path="/api/v1/identity/auth/refresh",
                )
            ],
        )


__all__ = ("AuthController",)
