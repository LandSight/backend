"""Error-to-HTTP-status mappings for the Parcel module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.module.parcel.application.error import (
    InvalidPolygonError,
    NotParcelOwnerError,
    ParcelAlreadyExistsError,
    ParcelNotFoundError,
)


if TYPE_CHECKING:
    from app.module.shared.application.error import ApplicationError


def get_parcel_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for this module.

    Returns
    -------
    dict[type[ApplicationError], int]
    """
    return {
        ParcelNotFoundError: HTTP_404_NOT_FOUND,
        ParcelAlreadyExistsError: HTTP_409_CONFLICT,
        InvalidPolygonError: HTTP_400_BAD_REQUEST,
        NotParcelOwnerError: HTTP_403_FORBIDDEN,
    }


__all__ = ("get_parcel_application_error_mappings",)
