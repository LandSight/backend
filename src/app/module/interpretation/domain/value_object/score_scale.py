"""Score scale value object."""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


@dataclass(frozen=True, slots=True)
class ScoreScale(BaseCompositeValueObject):
    """Converts aspect fractions into points on the final score scale.

    The total score is the weight-renormalized average of the evaluated aspects
    (``sum(score * weight) / sum(weight) * scale_max``): aspects without data
    are dropped, so the configured weights do not have to sum to one. Dividing
    by the total weight keeps the aspect points summing up to the total score.

    Attributes
    ----------
    scale_max : float
        Upper bound of the score scale.
    total_weight : float
        Sum of the weights of the evaluated aspects.
    """

    scale_max: float
    total_weight: float

    def _validate(self) -> None:
        if self.scale_max <= 0:
            message = f"Score scale maximum must be positive, got {self.scale_max}."
            raise ValidationError(message)
        if self.total_weight <= 0:
            message = f"Score scale total weight must be positive, got {self.total_weight}."
            raise ValidationError(message)

    def points(self, contribution: float) -> float:
        """Return the points an aspect contributed to the total score."""
        return contribution / self.total_weight * self.scale_max

    def max_points(self, weight: float) -> float:
        """Return the points an aspect could contribute at its best."""
        return weight / self.total_weight * self.scale_max


__all__ = ("ScoreScale",)
