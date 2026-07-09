"""Extensible exception handlers for the HTTP layer.

Each module provides its own error-to-status mappings via a function
that returns ``dict[type[Exception], int]``. The mappings are merged
in :func:`create_exception_handlers` and passed to Litestar.

If a mapping is not provided for an error type, it falls through to
the ``Exception`` handler and returns 500. This ensures all error
mappings are explicitly registered — no hidden defaults.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from litestar import Request, Response, status_codes

from app.interface.http.util.response import make_error_response
from app.module.shared.application.error import ApplicationError
from app.module.shared.domain.error import DomainError


if TYPE_CHECKING:
    from litestar.types import ExceptionHandler, ExceptionHandlersMap


def _create_domain_error_handler(
    mapping: dict[type[DomainError], int],
) -> ExceptionHandler:
    """Create a domain error handler for the given mapping."""

    def handler(request: Request, exc: DomainError) -> Response:
        status_code = mapping.get(type(exc))
        if status_code is None:
            return _internal_server_error_handler(request, exc)
        return make_error_response(status_code, str(exc))

    return cast("ExceptionHandler", handler)


def _create_application_error_handler(
    mapping: dict[type[ApplicationError], int],
) -> ExceptionHandler:
    """Create an application error handler for the given mapping."""

    def handler(request: Request, exc: ApplicationError) -> Response:
        status_code = mapping.get(type(exc))
        if status_code is None:
            return _internal_server_error_handler(request, exc)
        return make_error_response(status_code, str(exc))

    return cast("ExceptionHandler", handler)


def _internal_server_error_handler(_request: Request, _exc: Exception) -> Response:
    """Handle unexpected errors."""
    return make_error_response(status_codes.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")


def create_exception_handlers(
    domain_mappings: dict[type[DomainError], int] | None = None,
    application_mappings: dict[type[ApplicationError], int] | None = None,
) -> ExceptionHandlersMap:
    """Create the exception handlers map for Litestar.

    Parameters
    ----------
    domain_mappings : dict[type[DomainError], int] | None
        Mapping of domain error types to HTTP status codes.
    application_mappings : dict[type[ApplicationError], int] | None
        Mapping of application error types to HTTP status codes.

    Returns
    -------
    ExceptionHandlersMap
        Mapping of exception types to handler functions.
    """
    handlers: ExceptionHandlersMap = {}

    if domain_mappings:
        handlers[DomainError] = _create_domain_error_handler(domain_mappings)

    if application_mappings:
        handlers[ApplicationError] = _create_application_error_handler(application_mappings)

    handlers[Exception] = _internal_server_error_handler
    return handlers


__all__ = ("create_exception_handlers",)
