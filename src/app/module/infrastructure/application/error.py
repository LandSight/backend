"""Infrastructure module application errors."""

from app.module.shared.application.error import ApplicationError


class InfrastructureMetricsNotFoundError(ApplicationError):
    """Raised when infrastructure metrics are not found."""

    def __init__(self, parcel_id: str, category: str) -> None:
        super().__init__(f"Infrastructure metrics for parcel '{parcel_id}' and category '{category}' not found.")


class InfrastructureMetricsByIdNotFoundError(ApplicationError):
    """Raised when an infrastructure metrics record is not found by its ID.

    Also raised when the current user is not allowed to view the record, so that
    the API does not leak the existence of other users' metrics.
    """

    def __init__(self, metrics_id: str) -> None:
        super().__init__(f"Infrastructure metrics '{metrics_id}' not found.")


class UnknownCategoryError(ApplicationError):
    """Raised when an unsupported infrastructure category is requested."""

    def __init__(self, category: str) -> None:
        super().__init__(f"Unknown infrastructure category: '{category}'.")


__all__ = (
    "InfrastructureMetricsByIdNotFoundError",
    "InfrastructureMetricsNotFoundError",
    "UnknownCategoryError",
)
