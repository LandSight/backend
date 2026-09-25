"""Hierarchical fuzzy MCDA scorer implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.analysis.application.port import AnalysisScorer
from app.module.analysis.domain.entity import AnalysisEvaluation
from app.module.analysis.domain.value_object import (
    AnalysisEvaluationId,
    AnalysisId,
    AnalysisScore,
    AnalysisType,
)
from app.module.analysis.infrastructure.fuzzy import FuzzyNormalizer
from app.module.analysis.infrastructure.scorer.hierarchical_aggregator import HierarchicalAggregator
from app.module.shared.domain.error import ValidationError
from app.module.shared.interface.internal import IntegerMetricValue, NumberMetricValue


if TYPE_CHECKING:
    from collections.abc import Mapping
    from uuid import UUID

    from app.module.analysis.application.port import MetricsResponse
    from app.module.analysis.domain.value_object import ClusterScore, Hierarchy, NormalizedMetric
    from app.module.analysis.infrastructure.ports import FuzzyFunction


@dataclass(frozen=True, slots=True)
class HmcdaProfile:
    """Concrete engine inputs for one analysis type.

    Holds the configured hierarchy together with the concrete normalizer and
    aggregator built from it.
    """

    hierarchy: Hierarchy
    normalizer: FuzzyNormalizer
    aggregator: HierarchicalAggregator


def build_hmcda_profile(hierarchy: Hierarchy, functions: Mapping[str, FuzzyFunction]) -> HmcdaProfile:
    """Build an engine profile from a hierarchy and its fuzzy functions.

    Parameters
    ----------
    hierarchy : Hierarchy
        Aggregation hierarchy.
    functions : Mapping[str, FuzzyFunction]
        Fuzzy functions keyed by metric key.

    Returns
    -------
    HmcdaProfile
        The wired engine profile.

    Raises
    ------
    ValidationError
        If a hierarchy leaf metric has no fuzzy function configured.
    """
    missing = sorted(key for key in hierarchy.leaf_keys() if key not in functions)
    if missing:
        message = f"Missing fuzzy functions for metrics: {', '.join(missing)}."
        raise ValidationError(message)
    return HmcdaProfile(
        hierarchy=hierarchy,
        normalizer=FuzzyNormalizer(functions),
        aggregator=HierarchicalAggregator(hierarchy),
    )


class HmcdaAnalysisScorer(AnalysisScorer):
    """Scores an analysis with the hierarchical fuzzy MCDA engine.

    Metrics responses are flattened into a single key space: topography and
    climate metrics keep their key, while infrastructure metrics are namespaced
    as ``<category>:<metric>`` to match the configured hierarchy.
    """

    def __init__(self, profiles: Mapping[AnalysisType, HmcdaProfile]) -> None:
        self._profiles: dict[AnalysisType, HmcdaProfile] = dict(profiles)

    @override
    def evaluate(
        self,
        analysis_id: UUID,
        metrics: list[MetricsResponse],
        analysis_type: AnalysisType,
    ) -> AnalysisEvaluation:
        """See :class:`app.module.analysis.application.port.AnalysisScorer.evaluate`."""
        profile = self._profiles.get(analysis_type)
        if profile is None:
            message = f"No engine configured for analysis type '{analysis_type}'."
            raise ValidationError(message)
        normalized = self._normalize(profile, self._flatten(metrics))
        clusters = profile.aggregator.aggregate(normalized)
        return AnalysisEvaluation(
            id=AnalysisEvaluationId(uuid6()),
            analysis_id=AnalysisId(analysis_id),
            analysis_type=analysis_type,
            model_version=profile.hierarchy.model_version,
            total_score=self._total_score(clusters),
            clusters=clusters,
        )

    @staticmethod
    def _normalize(
        profile: HmcdaProfile,
        raw_values: Mapping[str, float | None],
    ) -> dict[str, NormalizedMetric]:
        """Normalize every hierarchy leaf, marking missing readings as unavailable."""
        return {key: profile.normalizer.normalize(key, raw_values.get(key)) for key in profile.hierarchy.leaf_keys()}

    @staticmethod
    def _total_score(clusters: tuple[ClusterScore, ...]) -> AnalysisScore:
        """Compute the total score on the 0-10 scale from the cluster scores."""
        total_weight = sum(cluster.weight.unwrap() for cluster in clusters)
        if total_weight <= 0:  # pragma: no cover - clusters always carry positive weights
            return AnalysisScore(0.0)
        weighted = sum(cluster.score.unwrap() * cluster.weight.unwrap() for cluster in clusters) / total_weight
        return AnalysisScore(weighted * 10)

    @staticmethod
    def _flatten(responses: list[MetricsResponse]) -> dict[str, float | None]:
        """Flatten neutral metrics responses into a canonical key space."""
        values: dict[str, float | None] = {}
        for response in responses:
            prefix = f"{response.category}:" if response.category else ""
            for metric in response.metrics:
                if isinstance(metric, (NumberMetricValue, IntegerMetricValue)):
                    values[f"{prefix}{metric.key}"] = None if metric.value is None else float(metric.value)
        return values


__all__ = ("HmcdaAnalysisScorer", "HmcdaProfile", "build_hmcda_profile")
