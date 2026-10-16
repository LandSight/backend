"""Analysis evaluation entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.domain.value_object import (
    AnalysisEngine,
    AnalysisEvaluationId,
    AnalysisId,
    AnalysisScore,
    AnalysisType,
    AppliedConstraint,
    ClusterScore,
    ConstraintEffect,
)
from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError


if TYPE_CHECKING:
    import datetime


class AnalysisEvaluation(BaseEntity[AnalysisEvaluationId]):
    """Scoring result aggregate root.

    Owns the cluster/subcluster/metric breakdown produced by an evaluation. The
    breakdown entries are composite value objects; only the evaluation itself
    has identity.

    Attributes
    ----------
    id : AnalysisEvaluationId
        Unique identifier for the evaluation.
    analysis_id : AnalysisId
        Analysis the evaluation belongs to.
    analysis_type : AnalysisType
        Evaluation profile.
    engine : AnalysisEngine
        Scoring engine that produced the evaluation.
    model_version : str
        Version of the hierarchy and normalization configuration used.
    total_score : AnalysisScore
        Final score in ``[0, 10]``, after the constraints.
    clusters : tuple[ClusterScore, ...]
        Per-cluster breakdown.
    base_score : AnalysisScore
        Score of the multi-criteria breakdown before the constraints; equals
        ``total_score`` when none applied.
    applied_constraints : tuple[AppliedConstraint, ...]
        Restriction zones that barred the scenario or lowered the score.
    created_at : datetime | None
        When the evaluation was created (UTC); ``None`` if not yet persisted.
    """

    def __init__(
        self,
        id: AnalysisEvaluationId,
        analysis_id: AnalysisId,
        *,
        analysis_type: AnalysisType,
        engine: AnalysisEngine = AnalysisEngine.BASELINE,
        model_version: str,
        total_score: AnalysisScore,
        clusters: tuple[ClusterScore, ...],
        base_score: AnalysisScore | None = None,
        applied_constraints: tuple[AppliedConstraint, ...] = (),
        created_at: datetime.datetime | None = None,
    ) -> None:
        self._analysis_id: AnalysisId = analysis_id
        self._analysis_type: AnalysisType = analysis_type
        self._engine: AnalysisEngine = engine
        self._model_version: str = model_version
        self._total_score: AnalysisScore = total_score
        self._clusters: tuple[ClusterScore, ...] = clusters
        self._base_score: AnalysisScore = total_score if base_score is None else base_score
        self._applied_constraints: tuple[AppliedConstraint, ...] = applied_constraints
        self._created_at: datetime.datetime | None = created_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        if not self._model_version:
            message = "An evaluation must carry a model version."
            raise InvariantViolationError(message)
        if not self._clusters:
            message = "An evaluation must carry at least one cluster."
            raise InvariantViolationError(message)
        if self._total_score.unwrap() > self._base_score.unwrap():
            message = "Constraints can only lower the score, never raise it above the base score."
            raise InvariantViolationError(message)
        if self.prohibited and self._total_score.unwrap() != 0:
            message = "A prohibited evaluation must have a total score of 0."
            raise InvariantViolationError(message)

    @property
    def analysis_id(self) -> AnalysisId:
        """Analysis the evaluation belongs to."""
        return self._analysis_id

    @property
    def analysis_type(self) -> AnalysisType:
        """Evaluation profile."""
        return self._analysis_type

    @property
    def engine(self) -> AnalysisEngine:
        """Scoring engine that produced the evaluation."""
        return self._engine

    @property
    def model_version(self) -> str:
        """Version of the hierarchy and normalization configuration used."""
        return self._model_version

    @property
    def total_score(self) -> AnalysisScore:
        """Final score in the 0-10 range."""
        return self._total_score

    @property
    def clusters(self) -> tuple[ClusterScore, ...]:
        """Per-cluster breakdown."""
        return self._clusters

    @property
    def base_score(self) -> AnalysisScore:
        """Score of the multi-criteria breakdown before the constraints."""
        return self._base_score

    @property
    def applied_constraints(self) -> tuple[AppliedConstraint, ...]:
        """Restriction zones that barred the scenario or lowered the score."""
        return self._applied_constraints

    @property
    def prohibited(self) -> bool:
        """Whether a constraint bars the scenario on the parcel."""
        return any(constraint.effect is ConstraintEffect.PROHIBIT for constraint in self._applied_constraints)

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the evaluation was created (UTC)."""
        return self._created_at


__all__ = ("AnalysisEvaluation",)
