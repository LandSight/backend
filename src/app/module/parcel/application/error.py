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


class InvalidGeoJsonError(ApplicationError):
    """Raised when the provided GeoJSON is malformed or not a valid Polygon."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Invalid GeoJSON: {reason}.")


class InvalidPolygonError(ApplicationError):
    """Raised when the polygon geometry is invalid."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Polygon is not valid: {reason}.")


__all__ = (
    "InvalidGeoJsonError",
    "InvalidPolygonError",
    "ParcelAlreadyExistsError",
    "ParcelNotFoundError",
)
