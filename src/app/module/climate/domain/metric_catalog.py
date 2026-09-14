"""Climate metric catalog.

The catalog is the module's domain knowledge about its metrics: keys, labels,
units and value kinds.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.value_object import MetricValueKind


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    """Definition of a single climate metric."""

    key: str
    label: str
    unit: str
    kind: MetricValueKind


CATALOG: tuple[MetricDefinition, ...] = (
    MetricDefinition("mean_annual_temperature", "Mean annual temperature", "degC", MetricValueKind.NUMBER),
    MetricDefinition("annual_precipitation", "Annual precipitation", "mm", MetricValueKind.NUMBER),
    MetricDefinition("temperature_seasonality", "Temperature seasonality", "degC", MetricValueKind.NUMBER),
    MetricDefinition("precipitation_seasonality", "Precipitation seasonality", "%", MetricValueKind.NUMBER),
    MetricDefinition(
        "max_temperature_warmest_month",
        "Max temperature of the warmest month",
        "degC",
        MetricValueKind.NUMBER,
    ),
    MetricDefinition(
        "min_temperature_coldest_month",
        "Min temperature of the coldest month",
        "degC",
        MetricValueKind.NUMBER,
    ),
    MetricDefinition("precipitation_wettest_month", "Precipitation of the wettest month", "mm", MetricValueKind.NUMBER),
    MetricDefinition("precipitation_driest_month", "Precipitation of the driest month", "mm", MetricValueKind.NUMBER),
)


__all__ = ("CATALOG", "MetricDefinition")
