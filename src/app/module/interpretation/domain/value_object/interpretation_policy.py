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
        Contribution above which a metric is considered strong.
    weak_threshold : float
        Normalized value below which a metric may be considered weak.
    metric_limit : int
        Maximum number of metrics selected per aspect.
    aspect_limit : int
        Maximum number of aspects selected for the combined summary.
    """

    strong_threshold: float = 0.05
    weak_threshold: float = 0.3
    metric_limit: int = 5
    aspect_limit: int = 5

    def _validate(self) -> None:
        if self.strong_threshold < 0:
            message = f"Strong threshold must not be negative, got {self.strong_threshold}."
            raise ValidationError(message)
        if not 0 <= self.weak_threshold <= 1:
            message = f"Weak threshold must be within [0, 1], got {self.weak_threshold}."
            raise ValidationError(message)
        if self.metric_limit < 1:
            message = f"Metric limit must be positive, got {self.metric_limit}."
            raise ValidationError(message)
        if self.aspect_limit < 1:
            message = f"Aspect limit must be positive, got {self.aspect_limit}."
            raise ValidationError(message)


__all__ = ("InterpretationPolicy",)
