"""Shared internal DTOs for module-to-module communication."""

from __future__ import annotations

from .metric_value import (
    IntegerMetricValue,
    MetricsResponse,
    MetricValue,
    MetricValueBase,
    NumberMetricValue,
    TextMetricValue,
    build_metric_value,
)


__all__ = (
    "IntegerMetricValue",
    "MetricValue",
    "MetricValueBase",
    "MetricsResponse",
    "NumberMetricValue",
    "TextMetricValue",
    "build_metric_value",
)
