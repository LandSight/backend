"""Evaluation breakdown value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object.suitability_verdict import SuitabilityVerdict
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object.aspect import Aspect
    from app.module.interpretation.domain.value_object.constraint_finding import ConstraintFinding


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
        Final score on the configured scale, after the constraints.
    scale_max : float
        Upper bound of the score scale.
    scenario : str
        Evaluation profile (e.g. ``izhs``).
    scenario_description : str
        Human-readable description of the profile, fed to the prompt.
    aspects : tuple[Aspect, ...]
        Top-level aspects with their flattened metrics; their points add up
        to ``base_score``.
    base_score : float | None
        Score of the aspects before the constraints; ``None`` means equal to
        ``total_score``.
    constraints : tuple[ConstraintFinding, ...]
        Restriction zones that barred the scenario or lowered the score.
    """

    total_score: float
    scale_max: float
    scenario: str
    aspects: tuple[Aspect, ...] = field(default_factory=tuple)
    scenario_description: str = ""
    base_score: float | None = None
    constraints: tuple[ConstraintFinding, ...] = field(default_factory=tuple)

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
        if self.base_score is not None and self.base_score < self.total_score:
            message = (
                f"Evaluation breakdown base score {self.base_score} must not be below "
                f"the total score {self.total_score}: constraints only lower the score."
            )
            raise ValidationError(message)

    @property
    def aspects_score(self) -> float:
        """Score the aspects add up to, before the constraints."""
        return self.total_score if self.base_score is None else self.base_score

    @property
    def constraints_loss(self) -> float:
        """Points the constraints took away from the score of the aspects."""
        return max(self.aspects_score - self.total_score, 0.0)

    @property
    def prohibited(self) -> bool:
        """Whether a restriction zone bars the scenario on the parcel."""
        return any(constraint.prohibits for constraint in self.constraints)

    @property
    def verdict(self) -> SuitabilityVerdict:
        """Qualitative suitability verdict: prohibited, or derived from the total score."""
        if self.prohibited:
            return SuitabilityVerdict.PROHIBITED
        return SuitabilityVerdict.from_ratio(self.total_score / self.scale_max)


__all__ = ("EvaluationBreakdown",)
