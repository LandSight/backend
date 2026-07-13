"""Request logging middleware."""

import logging
import time
from typing import TYPE_CHECKING

from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR


if TYPE_CHECKING:
    from litestar.types import (
        ASGIApp,
        Message,
        Receive,
        Scope,
        Send,
    )


class RequestLoggingMiddleware:
    """Middleware for logging HTTP requests and responses."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize middleware with ASGI app."""
        self.app = app
        self._logger = logging.getLogger("app.http.access")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Handle HTTP request and log response status."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.monotonic()
        status_code: list[int] = [0]

        async def patched_send(message: Message) -> None:
            """Patch send to capture status code."""
            if message["type"] == "http.response.start":
                status_code[0] = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, patched_send)
        finally:
            elapsed = time.monotonic() - start
            level = logging.ERROR if status_code[0] >= HTTP_500_INTERNAL_SERVER_ERROR else logging.INFO
            self._logger.log(
                level,
                "%s %s %s %dms",
                scope.get("method", "UNKNOWN"),
                scope.get("path", "/"),
                status_code[0],
                int(elapsed * 1000),
            )


__all__ = ("RequestLoggingMiddleware",)
