"""Reads the analysis evaluation through the analysis internal API.

This is the anti-corruption layer between the analysis module's recursive
evaluation DTO and the interpretation domain's flat breakdown: the reader calls
the analysis internal API and flattens the response into the domain model.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.response import HierarchicalExtensionResponse
from app.module.analysis.interface.internal.dto import GetAnalysisEvaluationInput
from app.module.interpretation.application.port import AnalysisService
from app.module.interpretation.domain.value_object import (
    Aspect,
    AspectMetric,
    EvaluationBreakdown,
    Membership,
    MetricRole,
    ScoreScale,
)


if TYPE_CHECKING:
    from collections.abc import Iterable
    from uuid import UUID

    from app.module.analysis.application.dto.response import (
        AnalysisEvaluationResponse,
        ClusterScoreResponse,
        MetricContributionResponse,
    )
    from app.module.analysis.interface.internal.port import AnalysisInternalAPI
    from app.module.interpretation.domain.service import MetricClassifier


class AnalysisServiceImpl(AnalysisService):
    """Flattens the recursive evaluation tree into a domain breakdown.

    Only the facts needed by the rule-based services are kept; the resulting
    breakdown is never persisted.
    """

    def __init__(self, analysis_api: AnalysisInternalAPI, classifier: MetricClassifier) -> None:
        self._analysis_api = analysis_api
        self._classifier = classifier

    @override
    async def read(self, analysis_id: UUID, current_user_id: UUID) -> EvaluationBreakdown:
        """See :class:`app.module.interpretation.application.port.AnalysisService.read`."""
        response = await self._analysis_api.get_analysis_evaluation(
            GetAnalysisEvaluationInput(
                analysis_id=analysis_id,
                current_user_id=current_user_id,
            ),
        )
        return self._build(response)

    def _build(self, response: AnalysisEvaluationResponse) -> EvaluationBreakdown:
        """Build the flat breakdown of an evaluation response."""
        extension = response.extensions.get("hierarchical")
        clusters = extension.clusters if isinstance(extension, HierarchicalExtensionResponse) else ()
        aspects: tuple[Aspect, ...] = ()
        if clusters:
            scale = ScoreScale(response.scale_max, sum(cluster.weight for cluster in clusters))
            aspects = tuple(self._aspect(cluster, scale) for cluster in clusters)
        return EvaluationBreakdown(
            total_score=response.total_score,
            scale_max=response.scale_max,
            scenario=response.scenario,
            aspects=aspects,
            scenario_description=response.scenario_description,
        )

    def _aspect(self, cluster: ClusterScoreResponse, scale: ScoreScale) -> Aspect:
        """Build an aspect with its points and all leaf metrics collected recursively."""
        return Aspect(
            key=cluster.key,
            name=cluster.name or cluster.key,
            score=cluster.score,
            weight=cluster.weight,
            contribution=cluster.contribution,
            points=scale.points(cluster.contribution),
            max_points=scale.max_points(cluster.weight),
            metrics=tuple(
                self._metric(metric, share * scale.max_points(cluster.weight))
                for metric, share in self._collect(cluster, 1.0)
            ),
        )

    def _collect(
        self,
        cluster: ClusterScoreResponse,
        share: float,
    ) -> Iterable[tuple[MetricContributionResponse, float]]:
        """Yield the leaf metrics of a cluster with their weight share inside the aspect.

        The share mirrors the aggregator: at every level the weights are
        renormalized over the entries that have a reading (subclusters without
        any reading are already dropped from the tree), so the shares of the
        metrics with data sum up to ``share``.
        """
        if cluster.metrics:
            total = sum(metric.weight for metric in cluster.metrics if metric.normalized_value is not None)
            for metric in cluster.metrics:
                available = metric.normalized_value is not None and total > 0
                yield metric, share * metric.weight / total if available else 0.0
            return
        total = sum(subcluster.weight for subcluster in cluster.subclusters)
        for subcluster in cluster.subclusters:
            yield from self._collect(subcluster, share * subcluster.weight / total if total > 0 else 0.0)

    def _metric(self, metric: MetricContributionResponse, max_points: float) -> AspectMetric:
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
            membership=self._membership(metric),
            max_points=max_points,
        )
        return replace(view, role=self._classifier.classify(view))

    @staticmethod
    def _membership(metric: MetricContributionResponse) -> Membership | None:
        """Build the membership function of a metric when it is known."""
        if not metric.membership_function or metric.membership_params is None:
            return None
        return Membership(function=metric.membership_function, params=dict(metric.membership_params))


__all__ = ("AnalysisServiceImpl",)
