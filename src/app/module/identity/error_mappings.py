"""Error-to-HTTP-status mappings for the Identity module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.module.identity.application.error import (
    AuthenticationError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from app.module.shared.application.error import ApplicationError
    from app.module.shared.domain.error import DomainError


def get_identity_domain_error_mappings() -> dict[type[DomainError], int]:
    """Return domain error to HTTP status mappings for this module.

    Returns
    -------
    dict[type[DomainError], int]
    """
    return {
        ValidationError: HTTP_400_BAD_REQUEST,
    }


def get_identity_application_error_mappings() -> dict[type[ApplicationError], int]:
    """Return application error to HTTP status mappings for this module.

    Returns
    -------
    dict[type[ApplicationError], int]
    """
    return {
        AuthenticationError: HTTP_401_UNAUTHORIZED,
        UserNotFoundError: HTTP_404_NOT_FOUND,
        UserAlreadyExistsError: HTTP_409_CONFLICT,
    }


__all__ = (
    "get_identity_application_error_mappings",
    "get_identity_domain_error_mappings",
)
