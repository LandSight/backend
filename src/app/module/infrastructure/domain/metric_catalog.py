"""Infrastructure metric catalog.

The catalog is the module's domain knowledge about its metrics: keys, labels,
units and value kinds.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.value_object import MetricValueKind


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    """Definition of a single infrastructure metric."""

    key: str
    label: str
    unit: str
    kind: MetricValueKind


CATEGORY_CATALOG: tuple[MetricDefinition, ...] = (
    MetricDefinition("buffer", "Buffer", "m", MetricValueKind.INTEGER),
    MetricDefinition("count", "Count", "", MetricValueKind.INTEGER),
    MetricDefinition("min_distance_to", "Min distance to", "m", MetricValueKind.NUMBER),
)

COVERAGE_RATIO: MetricDefinition = MetricDefinition(
    "coverage_ratio",
    "Coverage ratio",
    "ratio",
    MetricValueKind.NUMBER,
)

CATALOG: tuple[MetricDefinition, ...] = (*CATEGORY_CATALOG, COVERAGE_RATIO)


__all__ = ("CATALOG", "CATEGORY_CATALOG", "COVERAGE_RATIO", "MetricDefinition")
