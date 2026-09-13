"""Topography metric catalog.

The catalog is the module's domain knowledge about its metrics: keys, labels,
units and value kinds.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.value_object import MetricValueKind


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    """Definition of a single topography metric."""

    key: str
    label: str
    unit: str
    kind: MetricValueKind


CATALOG: tuple[MetricDefinition, ...] = (
    MetricDefinition("mean_elevation", "Mean elevation", "m", MetricValueKind.NUMBER),
    MetricDefinition("max_elevation", "Max elevation", "m", MetricValueKind.NUMBER),
    MetricDefinition("min_elevation", "Min elevation", "m", MetricValueKind.NUMBER),
    MetricDefinition("elevation_range", "Elevation range", "m", MetricValueKind.NUMBER),
    MetricDefinition("elevation_std", "Elevation std", "m", MetricValueKind.NUMBER),
    MetricDefinition("mean_slope", "Mean slope", "deg", MetricValueKind.NUMBER),
    MetricDefinition("max_slope", "Max slope", "deg", MetricValueKind.NUMBER),
    MetricDefinition("aspect", "Aspect", "", MetricValueKind.TEXT),
    MetricDefinition("south_aspect_percentage", "South aspect percentage", "%", MetricValueKind.NUMBER),
    MetricDefinition("area", "Area", "m2", MetricValueKind.NUMBER),
    MetricDefinition("perimeter", "Perimeter", "m", MetricValueKind.NUMBER),
    MetricDefinition("compactness_index", "Compactness index", "", MetricValueKind.NUMBER),
    MetricDefinition("elongation_index", "Elongation index", "", MetricValueKind.NUMBER),
)


__all__ = ("CATALOG", "MetricDefinition")
