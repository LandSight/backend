"""Dependency injection for Identity module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.identity.application.port import TokenService, UserRepository
from app.module.identity.application.use_case import (
    AuthenticateUserUseCase,
    GetCurrentUserByTokenUseCase,
    GetUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)
from app.module.identity.infrastructure.repository import PostgresUserRepository
from app.module.identity.infrastructure.security import (
    BcryptPasswordHasher,
    JWTTokenService,
)
from app.module.identity.interface.internal.api import IdentityInternal
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


def provide_get_current_user_by_token_use_case(
    token_service: NamedDependency[TokenService],
    user_repository: NamedDependency[UserRepository],
) -> GetCurrentUserByTokenUseCase:
    return GetCurrentUserByTokenUseCase(token_service, user_repository)


# ----- Internal API -----
def provide_identity_internal(
    register_user_use_case: NamedDependency[RegisterUserUseCase],
    authenticate_user_use_case: NamedDependency[AuthenticateUserUseCase],
    refresh_token_use_case: NamedDependency[RefreshTokenUseCase],
    get_user_use_case: NamedDependency[GetUserUseCase],
    get_current_user_by_token_use_case: NamedDependency[GetCurrentUserByTokenUseCase],
) -> IdentityInternal:
    return IdentityInternal(
        register_use_case=register_user_use_case,
        authenticate_use_case=authenticate_user_use_case,
        refresh_token_use_case=refresh_token_use_case,
        get_user_use_case=get_user_use_case,
        get_current_user_by_token_use_case=get_current_user_by_token_use_case,
    )


identity_dependencies = {
    "user_repository": Provide(provide_postgres_user_repository, sync_to_thread=False),
    "password_hasher": Provide(provide_bcrypt_password_hasher, sync_to_thread=False),
    "token_service": Provide(provide_jwt_token_service, sync_to_thread=False),
    "register_user_use_case": Provide(provide_register_use_case, sync_to_thread=False),
    "authenticate_user_use_case": Provide(provide_authenticate_use_case, sync_to_thread=False),
    "get_user_use_case": Provide(provide_get_user_use_case, sync_to_thread=False),
    "refresh_token_use_case": Provide(provide_refresh_token_use_case, sync_to_thread=False),
    "get_current_user_by_token_use_case": Provide(provide_get_current_user_by_token_use_case, sync_to_thread=False),
    "identity_api": Provide(provide_identity_internal, sync_to_thread=False),
}

__all__ = ("identity_dependencies",)
