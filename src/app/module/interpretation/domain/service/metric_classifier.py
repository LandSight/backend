"""Rule-based metric classifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy, MetricRole


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object import AspectMetric


class MetricClassifier:
    """Splits aspect metrics into strong, weak and neutral roles.

    A metric is strong when its contribution is above the policy's strong
    threshold; it is weak when its normalized value is below the weak threshold
    and it did not contribute enough to be strong. Everything else is neutral.
    Metrics without a usable reading are neutral and never selected.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def policy(self) -> InterpretationPolicy:
        """The interpretation policy driving the classification."""
        return self._policy

    def classify(self, metric: AspectMetric) -> MetricRole:
        """Return the rule-based role of a metric."""
        if metric.normalized_value is None or metric.contribution is None:
            return MetricRole.NEUTRAL
        if metric.contribution > self._policy.strong_threshold:
            return MetricRole.STRONG
        if metric.normalized_value < self._policy.weak_threshold:
            return MetricRole.WEAK
        return MetricRole.NEUTRAL


__all__ = ("MetricClassifier",)
