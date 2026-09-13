"""Composition root for background tasks.

Reuses the same module dependency-provider dictionaries as the HTTP layer,
resolving them without Litestar. Platform-level dependencies that Litestar
would normally inject from application state (session, S3/AWS sessions,
configs) are seeded explicitly.

The worker only resolves module-owned providers by name; it does not import
application or infrastructure implementations directly.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import TYPE_CHECKING, cast

from app.module.analysis.di import analysis_dependencies, analysis_worker_dependencies
from app.module.climate.di import climate_dependencies
from app.module.infrastructure.di import infrastructure_dependencies
from app.module.parcel.di import parcel_dependencies
from app.module.topography.di import topography_dependencies
from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config
from app.platform.database.session import create_async_session_factory
from app.platform.storage.client import create_s3_boto_client
from app.platform.storage.session import create_aws_session, create_boto_session


if TYPE_CHECKING:
    from collections.abc import Awaitable

    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


_ALL_DEPENDENCIES = {
    **parcel_dependencies,
    **topography_dependencies,
    **infrastructure_dependencies,
    **climate_dependencies,
    **analysis_dependencies,
    **analysis_worker_dependencies,
}

_loop: asyncio.AbstractEventLoop | None = None
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def run_in_worker_loop[T](coro: Awaitable[T]) -> T:
    """Run a coroutine on the worker's persistent event loop.

    A single loop per worker process keeps the asyncpg connection pool bound to
    one loop across tasks.
    """
    return _get_loop().run_until_complete(coro)


def _get_loop() -> asyncio.AbstractEventLoop:
    """Return the worker's persistent event loop, creating it if needed."""
    global _loop  # noqa: PLW0603
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the worker's process-wide session factory."""
    global _engine, _session_factory  # noqa: PLW0603
    if _session_factory is None:
        config = load_app_config()
        _engine = create_async_engine_from_config(config.database)
        _session_factory = create_async_session_factory(_engine)
    return _session_factory


class WorkerContainer:
    """Resolves module dependencies outside of a Litestar request scope."""

    def __init__(self, session: AsyncSession) -> None:
        self._resolved: dict[str, object] = {}
        self._seed_platform_dependencies(session)

    def _seed_platform_dependencies(self, session: AsyncSession) -> None:
        """Seed dependencies normally injected by Litestar from app state."""
        config = load_app_config()
        boto_session = create_boto_session(config.s3)
        self._resolved["database_config"] = config.database
        self._resolved["auth_config"] = config.auth
        self._resolved["s3_config"] = config.s3
        self._resolved["session"] = session
        self._resolved["boto_session"] = boto_session
        self._resolved["s3_boto_client"] = create_s3_boto_client(boto_session, config.s3)
        self._resolved["aws_session"] = create_aws_session(boto_session)

    def resolve[T](self, name: str) -> T:
        """Resolve a dependency by name, constructing missing providers.

        Parameters
        ----------
        name : str
            Dependency name from a module's dependency dictionary.

        Returns
        -------
        T
            The resolved dependency.
        """
        if name in self._resolved:
            return cast("T", self._resolved[name])

        provide = _ALL_DEPENDENCIES[name]
        factory = provide.dependency
        parameters = inspect.signature(factory).parameters
        value = factory(**{parameter: self.resolve(parameter) for parameter in parameters})
        if provide.use_cache:
            self._resolved[name] = value
        return cast("T", value)


__all__ = (
    "WorkerContainer",
    "get_session_factory",
    "run_in_worker_loop",
)
