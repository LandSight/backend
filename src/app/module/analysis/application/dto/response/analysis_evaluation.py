"""Evaluation tree response DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
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
class AnalysisEvaluationResponse:
    """Response DTO for a full analysis evaluation tree."""

    analysis_id: str
    analysis_type: str
    model_version: str
    total_score: float
    scale: str
    clusters: tuple[ClusterScoreResponse, ...] = field(default_factory=tuple)


__all__ = (
    "AnalysisEvaluationResponse",
    "ClusterScoreResponse",
    "MetricContributionResponse",
)
