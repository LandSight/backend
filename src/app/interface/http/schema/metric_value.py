"""Shared HTTP schemas for neutral metric values and metrics responses."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.module.shared.interface.internal import (
    IntegerMetricValue,
    MetricsResponse,
    MetricValue,
    NumberMetricValue,
    TextMetricValue,
)


class MetricValueSchemaBase(BaseModel):
    """Fields shared by every metric value schema variant."""

    key: str = Field(description="Machine metric key.")
    label: str = Field(description="Human-readable metric name.")
    unit: str = Field(description="Unit of the value; empty for unitless metrics.")


class NumberMetricValueSchema(MetricValueSchemaBase):
    """A floating-point metric value."""

    value_type: Literal["number"] = "number"
    value: float = Field(description="Floating-point metric value.")


class IntegerMetricValueSchema(MetricValueSchemaBase):
    """An integer metric value."""

    value_type: Literal["integer"] = "integer"
    value: int = Field(description="Integer metric value.")


class TextMetricValueSchema(MetricValueSchemaBase):
    """A textual metric value."""

    value_type: Literal["text"] = "text"
    value: str = Field(description="Textual (categorical) metric value.")


class SeriesMetricValueSchema(MetricValueSchemaBase):
    """A series metric value."""

    value_type: Literal["series"] = "series"
    value: list[float] = Field(default_factory=list, description="Series metric value.")


MetricValueSchema = Annotated[
    NumberMetricValueSchema | IntegerMetricValueSchema | TextMetricValueSchema | SeriesMetricValueSchema,
    Field(discriminator="value_type"),
]


class MetricsResponseSchema(BaseModel):
    """Metrics calculated by one module for one snapshot."""

    module: str = Field(description="Metric module (topography/climate/infrastructure).")
    category: str | None = Field(default=None, description="Infrastructure category; null for single-metric modules.")
    id: UUID = Field(description="ID of the persisted metrics snapshot.")
    metrics: list[MetricValueSchema] = Field(default_factory=list, description="Metric values of this snapshot.")


def _metric_value_to_schema(metric: MetricValue) -> MetricValueSchema:
    """Map a neutral metric value variant to its HTTP schema."""
    if isinstance(metric, NumberMetricValue):
        return NumberMetricValueSchema(key=metric.key, label=metric.label, unit=metric.unit, value=metric.value)
    if isinstance(metric, IntegerMetricValue):
        return IntegerMetricValueSchema(key=metric.key, label=metric.label, unit=metric.unit, value=metric.value)
    if isinstance(metric, TextMetricValue):
        return TextMetricValueSchema(key=metric.key, label=metric.label, unit=metric.unit, value=metric.value)
    return SeriesMetricValueSchema(key=metric.key, label=metric.label, unit=metric.unit, value=metric.value)


def metrics_response_to_schema(response: MetricsResponse) -> MetricsResponseSchema:
    """Map a neutral metrics response to its HTTP schema."""
    return MetricsResponseSchema(
        module=response.module,
        category=response.category,
        id=response.id,
        metrics=[_metric_value_to_schema(metric) for metric in response.metrics],
    )


__all__ = (
    "IntegerMetricValueSchema",
    "MetricValueSchema",
    "MetricValueSchemaBase",
    "MetricsResponseSchema",
    "NumberMetricValueSchema",
    "SeriesMetricValueSchema",
    "TextMetricValueSchema",
    "metrics_response_to_schema",
)
