from litestar import get

from app.interface.http.schema.system import HealthResponse


@get("/health", sync_to_thread=False)
def health() -> HealthResponse:
    """Check service availability."""
    return HealthResponse(status="ok")
