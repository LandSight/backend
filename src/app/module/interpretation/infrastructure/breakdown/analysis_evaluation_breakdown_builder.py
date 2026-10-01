"""Builds the interpretation breakdown from an analysis evaluation response.

This is the anti-corruption layer between the analysis module's recursive
evaluation DTO and the interpretation domain's flat breakdown.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.response import HierarchicalExtensionResponse
from app.module.interpretation.application.port import EvaluationBreakdownBuilder
from app.module.interpretation.domain.value_object import Aspect, AspectMetric, EvaluationBreakdown, MetricRole


if TYPE_CHECKING:
    from collections.abc import Iterable

    from app.module.analysis.application.dto.response import (
        AnalysisEvaluationResponse,
        ClusterScoreResponse,
        MetricContributionResponse,
    )
    from app.module.interpretation.domain.service import MetricClassifier


class AnalysisEvaluationBreakdownBuilder(EvaluationBreakdownBuilder):
    """Flattens the recursive evaluation tree into a domain breakdown.

    Only the facts needed by the rule-based services are kept; the resulting
    breakdown is never persisted.
    """

    def __init__(self, classifier: MetricClassifier) -> None:
        self._classifier = classifier

    @override
    def build(self, response: AnalysisEvaluationResponse) -> EvaluationBreakdown:
        """Build the flat breakdown of an evaluation response."""
        extension = response.extensions.get("hierarchical")
        clusters = extension.clusters if isinstance(extension, HierarchicalExtensionResponse) else ()
        return EvaluationBreakdown(
            total_score=response.total_score,
            scale=response.scale,
            scenario=response.scenario,
            aspects=tuple(self._aspect(cluster) for cluster in clusters),
            scenario_description=response.scenario_description,
        )

    def _aspect(self, cluster: ClusterScoreResponse) -> Aspect:
        """Build an aspect with all leaf metrics collected recursively."""
        return Aspect(
            key=cluster.key,
            name=cluster.name or cluster.key,
            score=cluster.score,
            weight=cluster.weight,
            contribution=cluster.contribution,
            metrics=tuple(self._metric(metric) for metric in self._collect(cluster)),
        )

    def _collect(self, cluster: ClusterScoreResponse) -> Iterable[MetricContributionResponse]:
        """Yield the leaf metrics of a cluster, recursing into subclusters."""
        if cluster.metrics:
            yield from cluster.metrics
            return
        for subcluster in cluster.subclusters:
            yield from self._collect(subcluster)

    def _metric(self, metric: MetricContributionResponse) -> AspectMetric:
        """Build a metric and assign its rule-based role."""
        view = AspectMetric(
            key=metric.key,
            label=metric.label,
            raw_value=metric.raw_value,
            normalized_value=metric.normalized_value,
            weight=metric.weight,
            contribution=metric.contribution,
            unit=metric.unit,
            role=MetricRole.NEUTRAL,
        )
        return replace(view, role=self._classifier.classify(view))


__all__ = ("AnalysisEvaluationBreakdownBuilder",)
