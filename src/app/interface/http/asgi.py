from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app import __api_version__
from app.interface.http.controller.system import SystemController
from app.interface.http.exception_handlers import create_exception_handlers
from app.module.identity.di import identity_dependencies
from app.module.identity.error_mappings import (
    get_identity_application_error_mappings,
    get_identity_domain_error_mappings,
)
from app.module.identity.interface.http.controller.auth import AuthController
from app.module.identity.interface.http.controller.user import UserController
from app.module.shared.interface.http.error_mappings import (
    get_shared_application_error_mappings,
    get_shared_domain_error_mappings,
)
from app.platform.config.loaders import load_logging_config
from app.platform.di import platform_dependencies
from app.platform.logging import configure_logging


def create_asgi_application() -> Litestar:
    """Create and configure the ASGI application.

    Returns
    -------
    Litestar
        ASGI application.
    """
    dependencies = {**platform_dependencies, **identity_dependencies}

    domain_mappings: dict = {}
    application_mappings: dict = {}

    domain_mappings.update(get_shared_domain_error_mappings())
    application_mappings.update(get_shared_application_error_mappings())

    domain_mappings.update(get_identity_domain_error_mappings())
    application_mappings.update(get_identity_application_error_mappings())

    app = Litestar(
        route_handlers=[
            SystemController,
            AuthController,
            UserController,
        ],
        dependencies=dependencies,
        openapi_config=OpenAPIConfig(
            title="Land Sight API",
            version=__api_version__,
            render_plugins=[ScalarRenderPlugin()],
        ),
        exception_handlers=create_exception_handlers(
            domain_mappings=domain_mappings,
            application_mappings=application_mappings,
        ),
    )
    logging_config = load_logging_config()
    configure_logging(config=logging_config)

    return app
