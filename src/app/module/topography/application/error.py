"""Topography module application errors."""

from app.module.shared.application.error import ApplicationError


class DemNotFoundError(ApplicationError):
    """Raised when DEM data is not available for the requested area."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"DEM data not available: {reason}.")


class RasterProcessingError(ApplicationError):
    """Raised when raster processing fails."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Raster processing failed: {reason}.")


class TopographyMetricsNotFoundError(ApplicationError):
    """Raised when topography metrics are not found."""

    def __init__(self, metrics_id: str) -> None:
        super().__init__(f"Topography metrics with id '{metrics_id}' not found.")


__all__ = (
    "DemNotFoundError",
    "RasterProcessingError",
    "TopographyMetricsNotFoundError",
)
