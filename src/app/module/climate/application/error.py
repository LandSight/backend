"""Climate module application errors."""

from __future__ import annotations

from app.module.shared.application.error import ApplicationError


class ClimateDataNotFoundError(ApplicationError):
    """Raised when climate data is not available for the requested area."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Climate data not available: {reason}.")


class RasterProcessingError(ApplicationError):
    """Raised when raster processing fails."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Raster processing failed: {reason}.")


class ClimateMetricsNotFoundError(ApplicationError):
    """Raised when climate metrics are not found."""

    def __init__(self, metrics_id: str) -> None:
        super().__init__(f"Climate metrics with id '{metrics_id}' not found.")


__all__ = (
    "ClimateDataNotFoundError",
    "ClimateMetricsNotFoundError",
    "RasterProcessingError",
)
