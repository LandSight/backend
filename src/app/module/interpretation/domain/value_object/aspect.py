"""Aspect value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object.aspect_metric import AspectMetric


@dataclass(frozen=True, slots=True)
class Aspect(BaseCompositeValueObject):
    """A top-level evaluation aspect with its flattened leaf metrics.

    An aspect is the interpretation domain view of a top-level cluster: the
    nested subclusters are flattened away and only the leaf metrics remain.

    Attributes
    ----------
    key : str
        Aspect (cluster) key.
    name : str
        Human-readable aspect name; falls back to the key when not configured.
    score : float
        Aspect score in ``[0, 1]``.
    weight : float
        Configured aspect weight.
    contribution : float
        ``score * weight``.
    metrics : tuple[AspectMetric, ...]
        Flattened leaf metrics.
    """

    key: str
    name: str
    score: float
    weight: float
    contribution: float
    metrics: tuple[AspectMetric, ...] = field(default_factory=tuple)

    def _validate(self) -> None:
        if not self.key:
            message = "Aspect key must not be empty."
            raise ValidationError(message)
        if not 0 <= self.score <= 1:
            message = f"Aspect '{self.key}' score must be within [0, 1], got {self.score}."
            raise ValidationError(message)
        if self.weight <= 0:
            message = f"Aspect '{self.key}' weight must be positive, got {self.weight}."
            raise ValidationError(message)
        if self.contribution < 0:
            message = f"Aspect '{self.key}' contribution must not be negative, got {self.contribution}."
            raise ValidationError(message)


__all__ = ("Aspect",)
