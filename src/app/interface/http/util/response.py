from __future__ import annotations

from typing import Any

from litestar import Response


def make_error_response(
    status_code: int,
    detail: str,
    errors: list[dict[str, Any]] | None = None,
) -> Response[dict]:
    """Create a standardized error response.

    Parameters
    ----------
    status_code : int
        HTTP status code.
    detail : str
        Human-readable error message.
    errors : list[dict[str, Any]] | None
        Optional field-level errors (e.g. validation failures).

    Returns
    -------
    Response[dict]
        JSON response with error detail and, when present, field errors.
    """
    content: dict[str, Any] = {"detail": detail}
    if errors:
        content["errors"] = errors
    return Response(
        content=content,
        status_code=status_code,
        media_type="application/json",
    )


__all__ = ("make_error_response",)
