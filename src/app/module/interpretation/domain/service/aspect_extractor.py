"""Aspect top-metrics extractor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.application.dto.response import MetricInfoResponse
from app.module.interpretation.domain.value_object import InterpretationPolicy, MetricRole


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object import Aspect, AspectMetric


class AspectExtractor:
    """Selects the metrics that best describe an aspect.

    Strong metrics come first, ordered by contribution descending, then weak
    metrics ordered by normalized value ascending. When this union has fewer
    than the policy limit, neutral metrics fill the remaining slots so a sparse
    aspect still gets an explanation.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def limit(self) -> int:
        """Maximum number of metrics returned per aspect."""
        return self._policy.metric_limit

    def top_metrics(self, aspect: Aspect) -> tuple[MetricInfoResponse, ...]:
        """Return up to the policy limit metrics describing the aspect."""
        available = [metric for metric in aspect.metrics if metric.data_available]
        strong = sorted(
            (metric for metric in available if metric.role is MetricRole.STRONG),
            key=lambda metric: metric.contribution or 0.0,
            reverse=True,
        )
        weak = sorted(
            (metric for metric in available if metric.role is MetricRole.WEAK),
            key=lambda metric: metric.normalized_value or 0.0,
        )
        selected = strong + weak
        if len(selected) < self.limit:
            neutral = sorted(
                (metric for metric in available if metric.role is MetricRole.NEUTRAL),
                key=lambda metric: metric.contribution or 0.0,
                reverse=True,
            )
            selected += neutral
        return tuple(self._to_info(metric) for metric in selected[: self.limit])

    @staticmethod
    def _to_info(metric: AspectMetric) -> MetricInfoResponse:
        """Map a metric view to its response DTO."""
        return MetricInfoResponse(
            key=metric.key,
            label=metric.label,
            raw_value=metric.raw_value,
            normalized_value=metric.normalized_value,
            contribution=metric.contribution,
            unit=metric.unit,
            role=metric.role,
        )


__all__ = ("AspectExtractor",)
