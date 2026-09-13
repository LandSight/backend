"""Neutral metric contracts shared between modules.

``MetricValue`` is a single self-describing reading (a tagged union, so
heterogeneous sets can be transferred and parsed safely). ``MetricsResponse``
groups the values of one persisted snapshot and carries the module/category/id
metadata once, so it is not repeated on every value.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, cast

from app.module.shared.domain.value_object import MetricValueKind


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricValueBase:
    """Fields shared by every metric value variant."""

    key: str
    label: str
    unit: str


@dataclass(frozen=True, slots=True, kw_only=True)
class NumberMetricValue(MetricValueBase):
    """A floating-point metric value."""

    value_type: Literal["number"] = "number"
    value: float = 0.0


@dataclass(frozen=True, slots=True, kw_only=True)
class IntegerMetricValue(MetricValueBase):
    """An integer metric value."""

    value_type: Literal["integer"] = "integer"
    value: int = 0


@dataclass(frozen=True, slots=True, kw_only=True)
class TextMetricValue(MetricValueBase):
    """A textual (categorical) metric value."""

    value_type: Literal["text"] = "text"
    value: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class SeriesMetricValue(MetricValueBase):
    """A series metric value (e.g. a histogram or distribution)."""

    value_type: Literal["series"] = "series"
    value: list[float] = field(default_factory=list)


MetricValue = NumberMetricValue | IntegerMetricValue | TextMetricValue | SeriesMetricValue


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricsResponse:
    """Metrics calculated by one metric module for one snapshot.

    Attributes
    ----------
    module : str
        Metric module (``topography``, ``climate``, ``infrastructure``).
    category : str | None
        Infrastructure category; ``None`` for single-metric modules.
    id : UUID
        ID of the persisted metrics snapshot.
    metrics : list[MetricValue]
        Metric values belonging to this snapshot.
    """

    module: str
    category: str | None
    id: UUID
    metrics: list[MetricValue] = field(default_factory=list)


def build_metric_value(
    *,
    key: str,
    label: str,
    unit: str,
    value_type: MetricValueKind,
    raw: object,
) -> MetricValue:
    """Build the metric value variant matching ``value_type``.

    Parameters
    ----------
    key : str
        Machine metric key.
    label : str
        Human-readable metric name.
    unit : str
        Unit of the value.
    value_type : MetricValueKind
        Variant discriminator.
    raw : object
        Raw value read from the module result.

    Returns
    -------
    MetricValue
        The matching metric value variant.
    """
    match value_type:
        case MetricValueKind.NUMBER:
            return NumberMetricValue(key=key, label=label, unit=unit, value=float(cast("float", raw)))
        case MetricValueKind.INTEGER:
            return IntegerMetricValue(key=key, label=label, unit=unit, value=int(cast("int", raw)))
        case MetricValueKind.TEXT:
            return TextMetricValue(key=key, label=label, unit=unit, value=str(raw))
        case MetricValueKind.SERIES:
            return SeriesMetricValue(
                key=key,
                label=label,
                unit=unit,
                value=[float(item) for item in cast("list[float]", raw)],
            )


__all__ = (
    "IntegerMetricValue",
    "MetricValue",
    "MetricValueBase",
    "MetricsResponse",
    "NumberMetricValue",
    "SeriesMetricValue",
    "TextMetricValue",
    "build_metric_value",
)
