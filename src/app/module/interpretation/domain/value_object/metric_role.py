"""Metric role value object."""

from __future__ import annotations

from enum import StrEnum


class MetricRole(StrEnum):
    """Rule-based role of a metric inside its aspect.

    The role is decided before any LLM call and never by the model.

    ``STRONG``
        The metric contributed above the strong threshold.
    ``WEAK``
        The metric normalized below the weak threshold and barely contributed.
    ``NEUTRAL``
        Neither clearly strong nor weak, or has no usable reading.
    """

    STRONG = "strong"
    WEAK = "weak"
    NEUTRAL = "neutral"


__all__ = ("MetricRole",)
