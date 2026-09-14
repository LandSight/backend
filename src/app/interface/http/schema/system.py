import typing

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health response schema."""

    status: typing.Literal["ok"] = "ok"


__all__ = ("HealthResponse",)
