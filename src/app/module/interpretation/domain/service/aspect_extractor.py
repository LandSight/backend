"""Aspect top-metrics extractor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy, MetricRole


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object import Aspect, AspectMetric


class AspectExtractor:
    """Selects the metrics that best describe an aspect.

    The selection is balanced between the two sides of the explanation: the
    strengths that earned the most points and the weaknesses that lost the
    most points. The weaknesses get the larger half of the limit (they explain
    why the aspect fell short of its maximum); when one side has fewer metrics
    than its half, the other side fills the free slots. Strengths come first,
    then weaknesses. Metrics without a reading are never selected.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def limit(self) -> int:
        """Maximum number of metrics returned per aspect."""
        return self._policy.metric_limit

    def top_metrics(self, aspect: Aspect) -> tuple[AspectMetric, ...]:
        """Return up to the policy limit metrics describing the aspect."""
        strong = sorted(
            (metric for metric in aspect.metrics if metric.role is MetricRole.STRONG),
            key=lambda metric: metric.points,
            reverse=True,
        )
        weak = sorted(
            (metric for metric in aspect.metrics if metric.role is MetricRole.WEAK),
            key=lambda metric: metric.loss,
            reverse=True,
        )
        weak_count = min(len(weak), max(self.limit - len(strong), (self.limit + 1) // 2))
        strong_count = min(len(strong), self.limit - weak_count)
        return (*strong[:strong_count], *weak[:weak_count])


__all__ = ("AspectExtractor",)
