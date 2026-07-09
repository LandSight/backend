"""Global error-to-HTTP-status mappings for shared errors."""

from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from app.module.shared.application.error import ApplicationError
from app.module.shared.domain.error import DomainError, InvariantViolationError, ValidationError


def get_shared_domain_error_mappings() -> dict[type[DomainError], int]:
    """Return domain error mappings for shared domain errors.

    Returns
    -------
    dict[type[DomainError], int]
    """
    return {
        ValidationError: HTTP_400_BAD_REQUEST,
        InvariantViolationError: HTTP_409_CONFLICT,
    }


def get_shared_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error mappings for shared application errors.

    Returns
    -------
    dict[type[ApplicationError], int]
    """
    return {
        ApplicationError: HTTP_500_INTERNAL_SERVER_ERROR,
    }


__all__ = (
    "get_shared_application_error_mappings",
    "get_shared_domain_error_mappings",
)
