"""Rule-based interpretation policy."""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


@dataclass(frozen=True, slots=True)
class InterpretationPolicy(BaseCompositeValueObject):
    """Domain policy of the rule-based interpretation.

    The thresholds and limits are properties of the interpretation model, not
    of a deployment, so they live in the domain with fixed defaults rather than
    in environment configuration.

    Attributes
    ----------
    strong_threshold : float
        Normalized value at or above which a metric earned (practically) its
        full points and is a strength; below it the metric lost points and is
        a weakness.
    metric_limit : int
        Maximum number of metrics selected per aspect, split between the
        strengths and the weaknesses.
    aspect_limit : int
        Maximum number of aspects selected for the combined summary.
    constraint_limit : int
        Maximum number of restriction zones selected for the restrictions
        explanation.
    """

    strong_threshold: float = 0.95
    metric_limit: int = 5
    aspect_limit: int = 5
    constraint_limit: int = 5

    def _validate(self) -> None:
        if not 0 < self.strong_threshold <= 1:
            message = f"Strong threshold must be within (0, 1], got {self.strong_threshold}."
            raise ValidationError(message)
        if self.metric_limit < 1:
            message = f"Metric limit must be positive, got {self.metric_limit}."
            raise ValidationError(message)
        if self.aspect_limit < 1:
            message = f"Aspect limit must be positive, got {self.aspect_limit}."
            raise ValidationError(message)
        if self.constraint_limit < 1:
            message = f"Constraint limit must be positive, got {self.constraint_limit}."
            raise ValidationError(message)


__all__ = ("InterpretationPolicy",)
