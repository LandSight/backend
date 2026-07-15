"""ASGI application factory."""

from __future__ import annotations

from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app import __api_version__
from app.interface.http.controller.system import SystemController
from app.interface.http.lifespan import lifespan
from app.interface.http.middleware import RequestLoggingMiddleware
from app.interface.http.util import (
    create_exception_handlers,
    get_all_application_error_mappings,
    get_all_dependencies,
    get_all_domain_error_mappings,
)
from app.module.identity.interface.http.controller.auth import AuthController
from app.module.identity.interface.http.controller.user import UserController
from app.module.parcel.interface.http.controller.parcel import ParcelController


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
