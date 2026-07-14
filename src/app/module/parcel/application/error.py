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

    def __init__(self, reason: str) -> None:
        super().__init__(f"Polygon is not valid: {reason}.")


class NotParcelOwnerError(ApplicationError):
    """Raised when a user tries to modify a parcel they do not own."""

    def __init__(self, parcel_id: str) -> None:
        super().__init__(f"User is not the owner of parcel '{parcel_id}'.")


__all__ = (
    "InvalidPolygonError",
    "NotParcelOwnerError",
    "ParcelAlreadyExistsError",
    "ParcelNotFoundError",
)
