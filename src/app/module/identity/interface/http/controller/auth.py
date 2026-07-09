"""Auth endpoints."""

from litestar import post
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.module.identity.application.dto.command import (
    AuthenticateUserCommand,
    RegisterUserCommand,
)
from app.module.identity.application.use_case import (
    AuthenticateUserUseCase,
    RegisterUserUseCase,
)
from app.module.identity.interface.http.schema.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)
from app.module.identity.interface.http.schema.user import UserResponse


class AuthController(Controller):
    """Authentication and user management endpoints."""

    path = "/api/v1/auth"
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
    ) -> AuthResponse:
        """Authenticate a user by username and password.

        Parameters
        ----------
        data : LoginRequest
            Login credentials.
        authenticate_user_use_case : AuthenticateUserUseCase
            Injected use case.

        Returns
        -------
        AuthResponse
            JWT tokens.
        """
        command = AuthenticateUserCommand(
            username=data.username,
            password=data.password,
        )
        result = await authenticate_user_use_case(command)

        return AuthResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
        )


__all__ = ("AuthController",)
