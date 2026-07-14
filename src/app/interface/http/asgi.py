"""ASGI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app import __api_version__
from app.interface.http.controller.system import SystemController
from app.interface.http.util import (
    RequestLoggingMiddleware,
    create_exception_handlers,
    get_all_application_error_mappings,
    get_all_dependencies,
    get_all_domain_error_mappings,
)
from app.module.identity.interface.http.controller.auth import AuthController
from app.module.identity.interface.http.controller.user import UserController
from app.module.parcel.interface.http.controller.parcel import ParcelController
from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine
from app.platform.logging import configure_logging


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None]:
    """Application lifespan: create engine on startup, dispose on shutdown."""
    # ── Startup ──────────────────────────────────────────────────────
    config = load_app_config()
    configure_logging(config.logging)

    engine = create_async_engine_from_config(config.database)
    app.state.engine = engine

    try:
        yield
    finally:
        # ── Shutdown ─────────────────────────────────────────────────
        await dispose_engine(engine)


def create_asgi_application() -> Litestar:
    """Create and configure the ASGI application.

    Returns
    -------
    Litestar
        ASGI application.
    """
    app = Litestar(
        route_handlers=[
            SystemController,
            AuthController,
            UserController,
            ParcelController,
        ],
        dependencies=get_all_dependencies(),
        openapi_config=OpenAPIConfig(
            title="Land Sight API",
            version=__api_version__,
            render_plugins=[ScalarRenderPlugin()],
        ),
        exception_handlers=create_exception_handlers(
            domain_mappings=get_all_domain_error_mappings(),
            application_mappings=get_all_application_error_mappings(),
        ),
        lifespan=[lifespan],
        middleware=[RequestLoggingMiddleware],
    )

    return app
