"""Dependency injection for Identity module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.identity.application.port import TokenService, UserRepository
from app.module.identity.application.use_case import (
    AuthenticateUserUseCase,
    GetUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)
from app.module.identity.infrastructure.repository import PostgresUserRepository
from app.module.identity.infrastructure.security import (
    BcryptPasswordHasher,
    JWTCurrentUserProvider,
    JWTTokenService,
)
from app.platform.config.models import AuthConfig


# ----- Repositories -----
def provide_postgres_user_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresUserRepository:
    return PostgresUserRepository(session)


# ----- Security Services -----
def provide_bcrypt_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def provide_jwt_token_service(
    auth_config: NamedDependency[AuthConfig],
) -> JWTTokenService:
    return JWTTokenService(auth_config)


# ----- Current User Provider -----
def provide_jwt_current_user_provider(
    token_service: NamedDependency[TokenService],
    user_repository: NamedDependency[UserRepository],
) -> JWTCurrentUserProvider:
    return JWTCurrentUserProvider(token_service, user_repository)


# ----- Use Cases -----
def provide_register_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
    password_hasher: NamedDependency[BcryptPasswordHasher],
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository, password_hasher)


def provide_authenticate_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
    password_hasher: NamedDependency[BcryptPasswordHasher],
    token_service: NamedDependency[JWTTokenService],
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repository, password_hasher, token_service)


def provide_get_user_use_case(
    user_repository: NamedDependency[PostgresUserRepository],
) -> GetUserUseCase:
    return GetUserUseCase(user_repository)


def provide_refresh_token_use_case(
    token_service: NamedDependency[JWTTokenService],
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(token_service)


# Словарь зависимостей модуля
identity_dependencies = {
    "user_repository": Provide(provide_postgres_user_repository, sync_to_thread=False),
    "password_hasher": Provide(provide_bcrypt_password_hasher, sync_to_thread=False),
    "token_service": Provide(provide_jwt_token_service, sync_to_thread=False),
    "current_user_provider": Provide(provide_jwt_current_user_provider, sync_to_thread=False),
    "register_user_use_case": Provide(provide_register_use_case, sync_to_thread=False),
    "authenticate_user_use_case": Provide(provide_authenticate_use_case, sync_to_thread=False),
    "get_user_use_case": Provide(provide_get_user_use_case, sync_to_thread=False),
    "refresh_token_use_case": Provide(provide_refresh_token_use_case, sync_to_thread=False),
}

__all__ = ("identity_dependencies",)
