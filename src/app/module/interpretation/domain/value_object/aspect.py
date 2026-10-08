"""Aspect value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

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
    points : float
        Points the aspect contributed to the total score.
    max_points : float
        Points the aspect could contribute at its best.
    metrics : tuple[AspectMetric, ...]
        Flattened leaf metrics.
    """

    _TOLERANCE: ClassVar[float] = 1e-9

    key: str
    name: str
    score: float
    weight: float
    contribution: float
    points: float
    max_points: float
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
        if self.max_points <= 0:
            message = f"Aspect '{self.key}' max points must be positive, got {self.max_points}."
            raise ValidationError(message)
        if not 0 <= self.points <= self.max_points + self._TOLERANCE:
            message = f"Aspect '{self.key}' points must be within [0, {self.max_points}], got {self.points}."
            raise ValidationError(message)

    @property
    def loss(self) -> float:
        """Points the aspect fell short of its maximum."""
        return max(self.max_points - self.points, 0.0)

    @property
    def loss_share(self) -> float:
        """Share of the maximum points the aspect lost, in ``[0, 1]``."""
        return self.loss / self.max_points


__all__ = ("Aspect",)
