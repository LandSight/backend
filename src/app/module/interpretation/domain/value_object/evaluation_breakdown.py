"""Evaluation breakdown value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    import datetime

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
    scale : str
        Score scale (e.g. ``0-10``).
    scenario : str
        Evaluation profile (e.g. ``izhs``).
    model_version : str
        Version of the scoring model that produced the evaluation.
    parcel_id : str
        ID of the evaluated parcel.
    evaluated_at : datetime.datetime | None
        When the evaluation was created.
    aspects : tuple[Aspect, ...]
        Top-level aspects with their flattened metrics.
    """

    total_score: float
    scale: str
    scenario: str
    model_version: str
    parcel_id: str
    evaluated_at: datetime.datetime | None
    aspects: tuple[Aspect, ...] = field(default_factory=tuple)

    def _validate(self) -> None:
        if self.total_score < 0:
            message = f"Evaluation breakdown total score must not be negative, got {self.total_score}."
            raise ValidationError(message)
        if not self.scenario:
            message = "Evaluation breakdown scenario must not be empty."
            raise ValidationError(message)


__all__ = ("EvaluationBreakdown",)
