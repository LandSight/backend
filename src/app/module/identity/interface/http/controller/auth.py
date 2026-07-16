"""Auth endpoints."""

from typing import Annotated

from litestar import Response, post
from litestar.controller import Controller
from litestar.datastructures import Cookie
from litestar.di import NamedDependency
from litestar.params import CookieParameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.module.identity.application.dto.command import (
    AuthenticateUserCommand,
    RefreshTokenCommand,
    RegisterUserCommand,
)
from app.module.identity.application.error import AuthenticationError
from app.module.identity.application.use_case import (
    AuthenticateUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)
from app.module.identity.interface.http.schema.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)
from app.module.identity.interface.http.schema.user import UserResponse
from app.platform.config.loaders import load_auth_config


class AuthController(Controller):
    """Authentication and user management endpoints."""

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
        register_user_use_case: NamedDependency[RegisterUserUseCase],
    ) -> UserResponse:
        """Register a new user.

        Parameters
        ----------
        data : RegisterRequest
            Registration data.
        register_user_use_case : RegisterUserUseCase
            Injected use case.

        Returns
        -------
        UserResponse
            Created user data.
        """
        command = RegisterUserCommand(
            username=data.username,
            password=data.password,
        )
        result = await register_user_use_case(command)

        return UserResponse(
            id=result.id,
            username=result.username,
        )

    @post(
        "/login",
        status_code=HTTP_200_OK,
        description="Authenticate a user and return JWT tokens.",
    )
    async def login(
        self,
        data: LoginRequest,
        authenticate_user_use_case: NamedDependency[AuthenticateUserUseCase],
    ) -> Response[AuthResponse]:
        """Authenticate a user by username and password.

        Returns an access token in the response body and sets the
        refresh token as an http-only cookie.

        Parameters
        ----------
        data : LoginRequest
            Login credentials.
        authenticate_user_use_case : AuthenticateUserUseCase
            Injected use case.

        Returns
        -------
        AuthResponse
            Access token.
        """
        command = AuthenticateUserCommand(
            username=data.username,
            password=data.password,
        )
        result = await authenticate_user_use_case(command)

        auth_config = load_auth_config()
        refresh_max_age = auth_config.refresh_token_expire_days * 24 * 60 * 60

        response = Response(
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
                    secure=True,
                    samesite="lax",
                    path="/api/v1/auth/refresh",
                )
            ],
        )

        return response

    @post(
        "/refresh",
        status_code=HTTP_200_OK,
        description="Refresh access token using a refresh token.",
    )
    async def refresh(
        self,
        refresh_token_use_case: NamedDependency[RefreshTokenUseCase],
        refresh_token: Annotated[str, CookieParameter(name="refresh_token", required=True)],
    ) -> Response[AuthResponse]:
        """Refresh an access token.

        Reads the refresh token from the ``refresh_token`` http-only cookie.

        Parameters
        ----------
        refresh_token : str
            Refresh token from the ``refresh_token`` cookie.
        refresh_token_use_case : RefreshTokenUseCase
            Injected use case.

        Returns
        -------
        AuthResponse
            New access token.
        """
        if not refresh_token:
            message = "Refresh token not found"
            raise AuthenticationError(message)

        command = RefreshTokenCommand(refresh_token=refresh_token)
        result = await refresh_token_use_case(command)

        auth_config = load_auth_config()
        refresh_max_age = auth_config.refresh_token_expire_days * 24 * 60 * 60

        response = Response(
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
                    secure=True,
                    samesite="lax",
                    path="/api/v1/auth/refresh",
                )
            ],
        )

        return response


__all__ = ("AuthController",)
