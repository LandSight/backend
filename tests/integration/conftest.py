import typing

import pytest
from litestar.testing import AsyncTestClient

from app.interface.http.asgi import create_asgi_application


if typing.TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from litestar import Litestar


@pytest.fixture(scope="session")
def app() -> Litestar:
    """Provide Litestar application instance for tests."""
    app = create_asgi_application()
    app.debug = True
    return app


@pytest.fixture(scope="function")
async def test_client(app: Litestar) -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Provide async test client bound to the Litestar app."""
    async with AsyncTestClient(app=app) as client:
        yield client
