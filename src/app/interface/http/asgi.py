from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app import __api_version__
from app.interface.http.controller.system import SystemController
from app.interface.http.dependencies import get_all_dependencies
from app.interface.http.error_mappings import (
    get_all_application_error_mappings,
    get_all_domain_error_mappings,
)
from app.interface.http.exception_handlers import create_exception_handlers
from app.module.identity.interface.http.controller.auth import AuthController
from app.module.identity.interface.http.controller.user import UserController
from app.platform.config.loaders import load_logging_config
from app.platform.database.engine import dispose_engine
from app.platform.logging import configure_logging


async def on_startup() -> None:
    """Initialize application resources on startup."""
    configure_logging(config=load_logging_config())


async def on_shutdown(app: Litestar) -> None:
    """Clean up application resources on shutdown."""
    engine = getattr(app.state, "database_engine", None)
    if engine is not None:
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
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    return app
