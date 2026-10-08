"""Aspect metric value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object.value_position import ValuePosition
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object.membership import Membership
    from app.module.interpretation.domain.value_object.metric_role import MetricRole


@dataclass(frozen=True, slots=True)
class AspectMetric(BaseCompositeValueObject):
    """One leaf metric of an aspect, with its rule-based role.

    This is the interpretation domain view of a metric: flattened out of the
    recursive evaluation tree and enriched with a human-readable label and the
    role computed from the interpretation policy.

    Attributes
    ----------
    key : str
        Canonical metric key.
    label : str
        Human-readable metric name; empty when not available.
    raw_value : float | None
        Raw reading; ``None`` when unavailable.
    normalized_value : float | None
        Normalized value in ``[0, 1]``; ``None`` when unavailable.
    weight : float
        Configured weight among siblings.
    contribution : float | None
        ``normalized_value * weight``; ``None`` when unavailable.
    unit : str
        Unit of the raw value.
    role : MetricRole
        Rule-based role inside the aspect.
    membership : Membership | None
        Fuzzy function the metric was normalized with; ``None`` when unknown.
    """

    key: str
    label: str
    raw_value: float | None
    normalized_value: float | None
    weight: float
    contribution: float | None
    unit: str
    role: MetricRole
    membership: Membership | None = None

    def _validate(self) -> None:
        if not self.key:
            message = "Aspect metric key must not be empty."
            raise ValidationError(message)
        if self.weight <= 0:
            message = f"Aspect metric '{self.key}' weight must be positive, got {self.weight}."
            raise ValidationError(message)
        if self.normalized_value is not None and not 0 <= self.normalized_value <= 1:
            message = f"Aspect metric '{self.key}' normalized value must be within [0, 1], got {self.normalized_value}."
            raise ValidationError(message)
        if self.contribution is not None and self.contribution < 0:
            message = f"Aspect metric '{self.key}' contribution must not be negative, got {self.contribution}."
            raise ValidationError(message)

    @property
    def data_available(self) -> bool:
        """Whether a usable normalized reading is available."""
        return self.normalized_value is not None

    @property
    def position(self) -> ValuePosition:
        """Where the raw value lies relative to the membership function zones."""
        if self.membership is None or self.raw_value is None:
            return ValuePosition.UNKNOWN
        return self.membership.position(self.raw_value)


__all__ = ("AspectMetric",)
