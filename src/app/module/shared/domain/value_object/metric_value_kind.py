"""Kind of a metric value (its transport-independent shape)."""

from __future__ import annotations

from enum import StrEnum


class MetricValueKind(StrEnum):
    """Shape of a metric value used to interpret and render it."""

    NUMBER = "number"
    INTEGER = "integer"
    TEXT = "text"


__all__ = ("MetricValueKind",)
