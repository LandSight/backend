"""Evaluation tree response DTOs.

The evaluation response has a universal core shared by every scoring engine and
an ``extensions`` mapping whose keys depend on the engine. The baseline engine
populates the ``hierarchical`` extension; the planned hybrid engine adds the
``rule_based`` and ``constraint_based`` extensions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from collections.abc import Mapping


@dataclass(frozen=True, slots=True)
class MetricContributionResponse:
    """Response DTO for one metric contribution.

    Attributes
    ----------
    key : str
        Metric key.
    raw_value : float | None
        Raw reading; ``None`` when unavailable.
    normalized_value : float | None
        Normalized value in ``[0, 1]``; ``None`` when unavailable.
    weight : float
        Configured weight among siblings.
    contribution : float | None
        Weighted contribution; ``None`` when unavailable.
    unit : str
        Unit of the raw value.
    data_available : bool
        Whether a usable reading was available.
    membership_function : str | None
        Name of the applied membership function.
    membership_params : Mapping[str, float] | None
        Parameters of the applied membership function.
    """

    key: str
    raw_value: float | None
    normalized_value: float | None
    weight: float
    contribution: float | None
    unit: str
    data_available: bool
    membership_function: str | None
    membership_params: Mapping[str, float] | None


@dataclass(frozen=True, slots=True)
class ClusterScoreResponse:
    """Response DTO for a group score.

    The same shape represents a top-level cluster and a nested subcluster.
    """

    key: str
    score: float
    weight: float
    contribution: float
    subclusters: tuple[ClusterScoreResponse, ...] = field(default_factory=tuple)
    metrics: tuple[MetricContributionResponse, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class HierarchicalExtensionResponse:
    """Hierarchical MCDA extension of an evaluation.

    Attributes
    ----------
    clusters : tuple[ClusterScoreResponse, ...]
        Per-cluster breakdown produced by the hierarchical engine.
    """

    clusters: tuple[ClusterScoreResponse, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class RuleBasedExtensionResponse:
    """Rule-based extension of an evaluation.

    Attributes
    ----------
    base_score : float
        Score before rules were applied.
    applied_rules : tuple[Mapping[str, object], ...]
        Rules that fired, in application order.
    """

    base_score: float
    applied_rules: tuple[Mapping[str, object], ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ConstraintExtensionResponse:
    """Constraint-based extension of an evaluation.

    Attributes
    ----------
    applied_constraints : tuple[Mapping[str, object], ...]
        Constraints that were applied, in application order.
    """

    applied_constraints: tuple[Mapping[str, object], ...] = field(default_factory=tuple)


type EvaluationExtensionResponse = (
    HierarchicalExtensionResponse | RuleBasedExtensionResponse | ConstraintExtensionResponse
)


@dataclass(frozen=True, slots=True)
class EvaluationMetadataResponse:
    """Metadata of an evaluation.

    Attributes
    ----------
    evaluated_at : datetime.datetime | None
        When the evaluation was created (UTC).
    parcel_id : str
        ID of the parcel the evaluation belongs to.
    """

    evaluated_at: datetime.datetime | None
    parcel_id: str


@dataclass(frozen=True, slots=True)
class AnalysisEvaluationResponse:
    """Response DTO for a full analysis evaluation.

    Attributes
    ----------
    scenario : str
        Evaluation profile (e.g. izhs).
    engine : str
        Scoring engine that produced the evaluation (e.g. baseline).
    model_version : str
        Version of the scoring model.
    total_score : float
        Final score on the 0-10 scale.
    scale : str
        Score scale.
    metadata : EvaluationMetadataResponse
        Evaluation metadata.
    extensions : Mapping[str, EvaluationExtensionResponse]
        Engine-specific extensions keyed by extension name.
    """

    scenario: str
    engine: str
    model_version: str
    total_score: float
    scale: str
    metadata: EvaluationMetadataResponse
    extensions: Mapping[str, EvaluationExtensionResponse] = field(default_factory=dict)


__all__ = (
    "AnalysisEvaluationResponse",
    "ClusterScoreResponse",
    "ConstraintExtensionResponse",
    "EvaluationExtensionResponse",
    "EvaluationMetadataResponse",
    "HierarchicalExtensionResponse",
    "MetricContributionResponse",
    "RuleBasedExtensionResponse",
)
