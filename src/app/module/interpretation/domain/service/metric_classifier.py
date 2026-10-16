"""Rule-based metric classifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy, MetricRole


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object import AspectMetric


class MetricClassifier:
    """Splits aspect metrics into strengths, weaknesses and metrics without data.

    A metric is strong when its normalized value reaches the policy's strong
    threshold, i.e. the value lies in (or practically in) the optimal zone and
    the metric earned its full points. Every other metric with a reading lost
    points and is weak. Metrics without a usable reading are neutral and never
    selected.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def policy(self) -> InterpretationPolicy:
        """The interpretation policy driving the classification."""
        return self._policy

    def classify(self, metric: AspectMetric) -> MetricRole:
        """Return the rule-based role of a metric."""
        if metric.normalized_value is None:
            return MetricRole.NEUTRAL
        if metric.normalized_value >= self._policy.strong_threshold:
            return MetricRole.STRONG
        return MetricRole.WEAK


__all__ = ("MetricClassifier",)
