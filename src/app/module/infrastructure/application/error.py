"""Infrastructure module application errors."""

from app.module.shared.application.error import ApplicationError


class InfrastructureMetricsNotFoundError(ApplicationError):
    """Raised when infrastructure metrics are not found."""

    def __init__(self, parcel_id: str, category: str) -> None:
        super().__init__(f"Infrastructure metrics for parcel '{parcel_id}' and category '{category}' not found.")


__all__ = ("InfrastructureMetricsNotFoundError",)
