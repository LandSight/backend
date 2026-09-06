"""Error-to-HTTP-status mappings for all modules."""

from __future__ import annotations

from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.module.climate.application.error import (
    ClimateDataNotFoundError,
    ClimateMetricsNotFoundError,
)
from app.module.identity.application.error import (
    AuthenticationError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.module.parcel.application.error import (
    InvalidGeoJsonError,
    InvalidPolygonError,
    ParcelAlreadyExistsError,
    ParcelNotFoundError,
)
from app.module.shared.application.error import ApplicationError, ForbiddenError
from app.module.shared.domain.error import DomainError, InvariantViolationError, ValidationError
from app.module.topography.application.error import (
    DemNotFoundError,
    RasterProcessingError,
    TopographyMetricsNotFoundError,
)


#  Shared module


def _get_shared_domain_error_mappings() -> dict[type[DomainError], int]:
    """Return domain error mappings for shared domain errors."""
    return {
        ValidationError: HTTP_400_BAD_REQUEST,
        InvariantViolationError: HTTP_409_CONFLICT,
    }


def _get_shared_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error mappings for shared application errors."""
    return {
        ApplicationError: HTTP_500_INTERNAL_SERVER_ERROR,
        ForbiddenError: HTTP_403_FORBIDDEN,
    }


#  Identity module


def _get_identity_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for Identity module."""
    return {
        AuthenticationError: HTTP_401_UNAUTHORIZED,
        UserNotFoundError: HTTP_404_NOT_FOUND,
        UserAlreadyExistsError: HTTP_409_CONFLICT,
    }


#  Parcel module


def _get_parcel_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for Parcel module."""
    return {
        ParcelNotFoundError: HTTP_404_NOT_FOUND,
        ParcelAlreadyExistsError: HTTP_409_CONFLICT,
        InvalidGeoJsonError: HTTP_400_BAD_REQUEST,
        InvalidPolygonError: HTTP_400_BAD_REQUEST,
    }


# Topography module


def _get_topography_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for Topography module."""
    return {
        TopographyMetricsNotFoundError: HTTP_404_NOT_FOUND,
        DemNotFoundError: HTTP_404_NOT_FOUND,
        RasterProcessingError: HTTP_400_BAD_REQUEST,
    }


# Climate module


def _get_climate_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for Climate module."""
    return {
        ClimateMetricsNotFoundError: HTTP_404_NOT_FOUND,
        ClimateDataNotFoundError: HTTP_404_NOT_FOUND,
    }


#  Public API


def get_all_domain_error_mappings() -> dict[type[DomainError], int]:
    """Merge all domain error mappings.

    Returns
    -------
    dict[type[DomainError], int]
        Combined domain error mappings.
    """
    mappings: dict[type[DomainError], int] = {}
    mappings.update(_get_shared_domain_error_mappings())
    return mappings


def get_all_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Merge all application error mappings.

    Returns
    -------
    dict[type[ApplicationError], int]
        Combined application error mappings.
    """
    mappings: dict[type[ApplicationError], int] = {}
    mappings.update(_get_shared_application_error_mappings())
    mappings.update(_get_identity_application_error_mappings())
    mappings.update(_get_parcel_application_error_mappings())
    mappings.update(_get_topography_application_error_mappings())
    mappings.update(_get_climate_application_error_mappings())
    return mappings


__all__ = (
    "get_all_application_error_mappings",
    "get_all_domain_error_mappings",
)
