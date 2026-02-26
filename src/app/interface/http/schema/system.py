import typing

from msgspec import Struct


class HealthResponse(Struct):
    """Health response schema."""

    status: typing.Literal["ok"] = "ok"
