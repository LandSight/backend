import typing

from litestar import Litestar, status_codes


if typing.TYPE_CHECKING:
    from litestar.testing import AsyncTestClient


async def test_health_check_endpoint(test_client: AsyncTestClient[Litestar]) -> None:
    """Health check endpoint returns HTTP 200 and ok status."""
    response = await test_client.get("/system/health")
    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == {"status": "ok"}
