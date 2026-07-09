"""Dependency injection for Identity module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.di import NamedDependency, Provide

from app.module.identity.application.use_case import (
    AuthenticateUserUseCase,
    GetUserUseCase,
    RegisterUserUseCase,
)
from app.module.identity.infrastructure.repository import PostgresUserRepository
from app.module.identity.infrastructure.security import (
    BcryptPasswordHasher,
    JWTCurrentUserProvider,
    JWTTokenService,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.module.identity.application.port import TokenService, UserRepository
    from app.platform.config.models import AuthConfig


# ----- Repositories -----
async def provide_postgres_user_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresUserRepository:
    return PostgresUserRepository(session)


# ----- Security Services -----
async def provide_bcrypt_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


async def provide_jwt_token_service(
    auth_config: NamedDependency[AuthConfig],
) -> JWTTokenService:
    return JWTTokenService(auth_config)


# ----- Current User Provider -----
async def provide_jwt_current_user_provider(
    token_service: NamedDependency[TokenService],
    user_repository: NamedDependency[UserRepository],
) -> JWTCurrentUserProvider:
    return JWTCurrentUserProvider(token_service, user_repository)


# ----- Use Cases -----
async def provide_register_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
    password_hasher: NamedDependency[BcryptPasswordHasher],
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository, password_hasher)


async def provide_authenticate_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
    password_hasher: NamedDependency[BcryptPasswordHasher],
    token_service: NamedDependency[JWTTokenService],
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repository, password_hasher, token_service)


async def provide_get_user_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
) -> GetUserUseCase:
    return GetUserUseCase(user_repository)


# Словарь зависимостей модуля
identity_dependencies = {
    "user_repository": Provide(provide_postgres_user_repository),
    "password_hasher": Provide(provide_bcrypt_password_hasher),
    "token_service": Provide(provide_jwt_token_service),
    "current_user_provider": Provide(provide_jwt_current_user_provider),
    "register_user_use_case": Provide(provide_register_use_case),
    "authenticate_user_use_case": Provide(provide_authenticate_use_case),
    "get_user_use_case": Provide(provide_get_user_use_case),
}

__all__ = ("identity_dependencies",)
