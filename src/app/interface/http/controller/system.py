from litestar import get
from src.app.interface.http.schema.system import HealthResponse


@get("/health")
def health() -> HealthResponse:
    """Check service availability."""
    return HealthResponse(status="ok")
