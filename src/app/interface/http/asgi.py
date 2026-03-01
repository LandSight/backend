from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app import __api_version__
from app.interface.http.controller.system import SystemController
from app.platform.config.loaders import load_logging_config
from app.platform.logging import configure_logging


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
        ],
        openapi_config=OpenAPIConfig(
            title="Land Sight API",
            version=__api_version__,
            render_plugins=[ScalarRenderPlugin()],
        ),
    )
    logging_config = load_logging_config()
    configure_logging(config=logging_config)

    return app
