"""Litestar dependency providers for platform-level dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from boto3 import Session as BotoSession
from botocore.client import BaseClient
from litestar.datastructures import State
from litestar.di import NamedDependency, Provide
from rasterio.session import AWSSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


from app.platform.config.loaders import load_auth_config, load_database_config, load_s3_config
from app.platform.config.models import AuthConfig, DatabaseConfig, S3Config
from app.platform.database.session import create_async_session_factory
from app.platform.storage.session import create_aws_session


# ----- Config -----
def provide_database_config() -> DatabaseConfig:
    """Provide database configuration."""
    return load_database_config()


def provide_auth_config() -> AuthConfig:
    """Provide authentication configuration."""
    return load_auth_config()


def provide_s3_config() -> S3Config:
    """Provide S3 configuration."""
    return load_s3_config()


# ----- Database -----
def provide_async_session_factory(
    state: State,
) -> async_sessionmaker[AsyncSession]:
    """Provide a session factory bound to the app database engine."""
    return create_async_session_factory(state.engine)


async def provide_async_session(
    session_factory: NamedDependency[async_sessionmaker[AsyncSession]],
) -> AsyncGenerator[AsyncSession]:
    """Provide a new async session per request.

    The session is closed automatically after the request finishes.
    """
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ----- Storage -----
def provide_boto_session(
    state: State
) -> BotoSession:
    """Provide the boto session from application state."""
    return state.boto_session


def provide_s3_boto_client(
    state: State
) -> BaseClient:
    """Provide the s3 boto client from application state."""
    return state.s3_boto_client


def provide_aws_session(
    boto_session: NamedDependency[BotoSession]
) -> AWSSession:
    """Provide the aws session."""
    return create_aws_session(boto_session)


platform_dependencies = {
    "database_config": Provide(provide_database_config, use_cache=True, sync_to_thread=False),
    "auth_config": Provide(provide_auth_config, use_cache=True, sync_to_thread=False),
    "s3_config": Provide(provide_s3_config, use_cache=True, sync_to_thread=False),
    "session_factory": Provide(provide_async_session_factory, use_cache=True, sync_to_thread=False),
    "session": Provide(provide_async_session),
    "boto_session": Provide(provide_boto_session, use_cache=True, sync_to_thread=False),
    "s3_boto_client": Provide(provide_s3_boto_client, use_cache=True, sync_to_thread=False),
    "aws_session": Provide(provide_aws_session, use_cache=True, sync_to_thread=False),
}


__all__ = (
    "platform_dependencies",
    "provide_async_session",
    "provide_auth_config",
)
