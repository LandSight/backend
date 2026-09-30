"""Hierarchical fuzzy MCDA scorer implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.analysis.application.port import AnalysisScorer
from app.module.analysis.domain.entity import AnalysisEvaluation
from app.module.analysis.domain.value_object import (
    AnalysisEngine,
    AnalysisEvaluationId,
    AnalysisId,
    AnalysisScore,
    AnalysisType,
)
from app.module.analysis.infrastructure.fuzzy import FuzzyNormalizer
from app.module.analysis.infrastructure.scorer.hmcda.hierarchical_aggregator import HierarchicalAggregator
from app.module.shared.domain.error import ValidationError
from app.module.shared.interface.internal import IntegerMetricValue, NumberMetricValue


if TYPE_CHECKING:
    from collections.abc import Mapping
    from uuid import UUID

    from app.module.analysis.application.port import MetricsResponse
    from app.module.analysis.domain.value_object import ClusterScore, NormalizedMetric
    from app.module.analysis.infrastructure.scorer.hmcda.config.models import EngineConfig, Hierarchy, ProfileConfig


@dataclass(frozen=True, slots=True)
class HmcdaProfile:
    """Concrete engine inputs for one analysis type."""

    hierarchy: Hierarchy
    normalizer: FuzzyNormalizer
    aggregator: HierarchicalAggregator


class HmcdaAnalysisScorer(AnalysisScorer):
    """Scores an analysis with the hierarchical fuzzy MCDA engine.

    The scorer owns its engine configuration: the ``EngineConfig`` passed in
    carries the profiles keyed by analysis type. Metrics responses are flattened
    into a single key space: topography and climate metrics keep their key,
    while infrastructure metrics are namespaced as ``<category>:<metric>`` to
    match the configured hierarchy.
    """

    def __init__(self, config: EngineConfig) -> None:
        self._model_version = config.model_version
        self._profiles: dict[AnalysisType, HmcdaProfile] = {
            analysis_type: self._build_profile(profile) for analysis_type, profile in config.profiles.items()
        }

    @override
    def evaluate(
        self,
        analysis_id: UUID,
        metrics: list[MetricsResponse],
        analysis_type: AnalysisType,
        engine: AnalysisEngine,
    ) -> AnalysisEvaluation:
        """See :class:`app.module.analysis.application.port.AnalysisScorer.evaluate`."""
        if engine is not AnalysisEngine.BASELINE:
            message = f"Engine '{engine}' is not supported by the HMCDA scorer."
            raise ValidationError(message)
        profile = self._profiles.get(analysis_type)
        if profile is None:
            message = f"No engine profile configured for analysis type '{analysis_type}'."
            raise ValidationError(message)
        normalized = self._normalize(profile, self._flatten(metrics))
        clusters = profile.aggregator.aggregate(normalized)
        return AnalysisEvaluation(
            id=AnalysisEvaluationId(uuid6()),
            analysis_id=AnalysisId(analysis_id),
            analysis_type=analysis_type,
            engine=engine,
            model_version=self._model_version,
            total_score=self._total_score(clusters),
            clusters=clusters,
        )

    @staticmethod
    def _build_profile(profile: ProfileConfig) -> HmcdaProfile:
        """Build the engine profile, ensuring every leaf has a fuzzy function."""
        functions = profile.to_fuzzy_functions()
        missing = sorted(key for key in profile.hierarchy.leaf_keys() if key not in functions)
        if missing:
            message = f"Missing fuzzy functions for metrics: {', '.join(missing)}."
            raise ValidationError(message)
        return HmcdaProfile(
            hierarchy=profile.hierarchy,
            normalizer=FuzzyNormalizer(functions),
            aggregator=HierarchicalAggregator(profile.hierarchy),
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
        weighted = sum(cluster.score.unwrap() * cluster.weight.unwrap() for cluster in clusters) / total_weight
        return AnalysisScore(weighted * 10)

    @staticmethod
    def _flatten(metrics_response: list[MetricsResponse]) -> dict[str, float | None]:
        """Flatten neutral metrics_response into a canonical key space."""
        values: dict[str, float | None] = {}
        for metric_response in metrics_response:
            prefix = f"{metric_response.category}:" if metric_response.category else ""
            for metric in metric_response.metrics:
                if isinstance(metric, (NumberMetricValue, IntegerMetricValue)):
                    values[f"{prefix}{metric.key}"] = None if metric.value is None else float(metric.value)
        return values


__all__ = ("HmcdaAnalysisScorer", "HmcdaProfile")
