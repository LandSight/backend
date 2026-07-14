from litestar import Response


def make_error_response(status_code: int, detail: str) -> Response[dict]:
    """Create a standardized error response.

    Parameters
    ----------
    status_code : int
        HTTP status code.
    detail : str
        Error message detail.

    Returns
    -------
    Response[dict]
        JSON response with error detail.
    """
    return Response(
        content={"detail": detail},
        status_code=status_code,
        media_type="application/json",
    )


__all__ = ("make_error_response",)
