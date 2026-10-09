"""Metric role value object."""

from __future__ import annotations

from enum import StrEnum


class MetricRole(StrEnum):
    """Rule-based role of a metric inside its aspect.

    The role is decided before any LLM call and never by the model.

    ``STRONG``
        A strength: the metric earned (practically) its full points.
    ``WEAK``
        A weakness: the metric lost points, its value is outside the optimum.
    ``NEUTRAL``
        The metric has no usable reading.
    """

    STRONG = "strong"
    WEAK = "weak"
    NEUTRAL = "neutral"


__all__ = ("MetricRole",)
