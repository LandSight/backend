from litestar import get
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK

from app.interface.http.schema.system import HealthResponse


class SystemController(Controller):
    """System management endpoints."""

    path = "api/v1/system"
    tags = ("system",)

    @get(
        "/health",
        sync_to_thread=False,
        status_code=HTTP_200_OK,
        description="Get service health status",
    )
    def health(self) -> HealthResponse:
        """Check service availability.

        Returns
        -------
        HealthResponse
            Object containing service health status.
            Always returns {"status": "ok"} when service is healthy.
        """
        return HealthResponse(status="ok")


__all__ = ("SystemController",)
