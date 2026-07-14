"""Parcel module application errors."""

from app.module.shared.application.error import ApplicationError


class ParcelNotFoundError(ApplicationError):
    """Raised when a parcel is not found."""

    def __init__(self, parcel_id: str) -> None:
        super().__init__(f"Parcel with id '{parcel_id}' not found.")


class ParcelAlreadyExistsError(ApplicationError):
    """Raised when a parcel with the given name already exists."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Parcel with name '{name}' already exists.")


class InvalidPolygonError(ApplicationError):
    """Raised when the polygon geometry is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


__all__ = (
    "InvalidPolygonError",
    "ParcelAlreadyExistsError",
    "ParcelNotFoundError",
)
