"""Cluster score value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.analysis_key import AnalysisKey
    from app.module.analysis.domain.value_object.contribution import Contribution
    from app.module.analysis.domain.value_object.metric_contribution import MetricContribution
    from app.module.analysis.domain.value_object.normalized_score import NormalizedScore
    from app.module.analysis.domain.value_object.weight import Weight


@dataclass(frozen=True, slots=True)
class ClusterScore(BaseCompositeValueObject):
    """Aggregated score of a group in the hierarchy.

    The same type represents a top-level cluster and a nested subcluster: a
    group either owns nested groups or metric contributions. Recursion is
    bounded by the hierarchy depth.

    Attributes
    ----------
    key : AnalysisKey
        Group key.
    score : NormalizedScore
        Aggregated score in ``[0, 1]``.
    weight : Weight
        Configured weight within the parent.
    contribution : Contribution
        ``score * weight``.
    subclusters : tuple[ClusterScore, ...]
        Nested groups; empty for a group of metrics.
    metrics : tuple[MetricContribution, ...]
        Metric contributions; empty for a group of subclusters.
    """

    key: AnalysisKey
    score: NormalizedScore
    weight: Weight
    contribution: Contribution
    subclusters: tuple[ClusterScore, ...] = field(default_factory=tuple)
    metrics: tuple[MetricContribution, ...] = field(default_factory=tuple)

    def _validate(self) -> None:
        if bool(self.subclusters) == bool(self.metrics):
            message = f"Cluster '{self.key.unwrap()}' must define exactly one of subclusters or metrics."
            raise ValidationError(message)
        if self.contribution.unwrap() > self.weight.unwrap() + 1e-9:
            message = (
                f"Cluster '{self.key.unwrap()}' contribution {self.contribution.unwrap()} "
                f"exceeds its weight {self.weight.unwrap()}."
            )
            raise ValidationError(message)


__all__ = ("ClusterScore",)
