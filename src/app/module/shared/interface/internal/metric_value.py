"""Neutral metric value contract shared between modules.

A ``MetricValue`` is a single, self-describing metric reading. It is a tagged
union: every variant carries a ``value_type`` discriminator so heterogeneous
metric sets can be transferred and parsed safely.

Variants:
- :class:`NumberMetricValue` — ``float``
- :class:`IntegerMetricValue` — ``int``
- :class:`TextMetricValue` — ``str``
- :class:`SeriesMetricValue` — ``list[float]``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, cast


if TYPE_CHECKING:
    from uuid import UUID


MetricValueType = Literal["number", "integer", "text", "series"]


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricValueBase:
    """Fields shared by every metric value variant."""

    module: str
    category: str | None
    metrics_id: UUID
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


def build_metric_value(  # noqa: PLR0913
    *,
    module: str,
    category: str | None,
    metrics_id: UUID,
    key: str,
    label: str,
    unit: str,
    value_type: MetricValueType,
    raw: object,
) -> MetricValue:
    """Build the metric value variant matching ``value_type``.

    Parameters
    ----------
    module : str
        Metric module name.
    category : str | None
        Infrastructure category; ``None`` for single-metric modules.
    metrics_id : UUID
        ID of the persisted metrics snapshot.
    key : str
        Machine metric key.
    label : str
        Human-readable metric name.
    unit : str
        Unit of the value.
    value_type : MetricValueType
        Variant discriminator.
    raw : object
        Raw value read from the module result.

    Returns
    -------
    MetricValue
        The matching metric value variant.
    """
    match value_type:
        case "number":
            return NumberMetricValue(
                module=module,
                category=category,
                metrics_id=metrics_id,
                key=key,
                label=label,
                unit=unit,
                value=float(cast("float", raw)),
            )
        case "integer":
            return IntegerMetricValue(
                module=module,
                category=category,
                metrics_id=metrics_id,
                key=key,
                label=label,
                unit=unit,
                value=int(cast("int", raw)),
            )
        case "text":
            return TextMetricValue(
                module=module,
                category=category,
                metrics_id=metrics_id,
                key=key,
                label=label,
                unit=unit,
                value=str(raw),
            )
        case "series":
            return SeriesMetricValue(
                module=module,
                category=category,
                metrics_id=metrics_id,
                key=key,
                label=label,
                unit=unit,
                value=[float(item) for item in cast("list[float]", raw)],
            )


__all__ = (
    "IntegerMetricValue",
    "MetricValue",
    "MetricValueBase",
    "MetricValueType",
    "NumberMetricValue",
    "SeriesMetricValue",
    "TextMetricValue",
    "build_metric_value",
)
