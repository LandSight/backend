from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from app import __api_version__
from app.interface.http.controller.system import health
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
            health,
        ],
        openapi_config=OpenAPIConfig(title="Land Sight API", version=__api_version__),
    )
    logging_config = load_logging_config()
    configure_logging(config=logging_config)

    return app
