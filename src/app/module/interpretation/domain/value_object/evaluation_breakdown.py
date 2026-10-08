"""Evaluation breakdown value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object.suitability_verdict import SuitabilityVerdict
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object.aspect import Aspect


@dataclass(frozen=True, slots=True)
class EvaluationBreakdown(BaseCompositeValueObject):
    """A finished evaluation broken down into interpretable aspects.

    This is the interpretation domain representation of an evaluation: unlike
    the hierarchical ``AnalysisEvaluation`` of the analysis module, it is flat
    and carries human-readable names, labels and metric roles, ready for the
    rule-based services and the LLM prompts. It is never persisted.

    Attributes
    ----------
    total_score : float
        Final score on the configured scale.
    scale_max : float
        Upper bound of the score scale.
    scenario : str
        Evaluation profile (e.g. ``izhs``).
    scenario_description : str
        Human-readable description of the profile, fed to the prompt.
    aspects : tuple[Aspect, ...]
        Top-level aspects with their flattened metrics.
    """

    total_score: float
    scale_max: float
    scenario: str
    aspects: tuple[Aspect, ...] = field(default_factory=tuple)
    scenario_description: str = ""

    def _validate(self) -> None:
        if self.total_score < 0:
            message = f"Evaluation breakdown total score must not be negative, got {self.total_score}."
            raise ValidationError(message)
        if self.scale_max <= 0:
            message = f"Evaluation breakdown scale maximum must be positive, got {self.scale_max}."
            raise ValidationError(message)
        if not self.scenario:
            message = "Evaluation breakdown scenario must not be empty."
            raise ValidationError(message)

    @property
    def verdict(self) -> SuitabilityVerdict:
        """Qualitative suitability verdict derived from the total score."""
        return SuitabilityVerdict.from_ratio(self.total_score / self.scale_max)


__all__ = ("EvaluationBreakdown",)
