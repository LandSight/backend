"""Hierarchical metrics aggregator."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object import (
    AnalysisKey,
    ClusterScore,
    Contribution,
    MetricContribution,
    NormalizedMetric,
    NormalizedScore,
    Weight,
)
from app.module.shared.domain.error import InvariantViolationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.infrastructure.scorer.hmcda.config.models import Hierarchy, HierarchyNode


class HierarchicalAggregator:
    """Aggregates normalized metrics through a hierarchy specification.

    Weights are renormalized at every level over the metrics that actually have
    a reading, so a missing input never drags a score down; when nothing in a
    node can be evaluated the node is dropped and its parent renormalizes.
    """

    def __init__(self, hierarchy: Hierarchy) -> None:
        self._hierarchy = hierarchy

    def aggregate(self, metrics: Mapping[str, NormalizedMetric]) -> tuple[ClusterScore, ...]:
        """Aggregate normalized metrics into cluster scores."""
        clusters = tuple(
            cluster for root in self._hierarchy.clusters if (cluster := self._cluster(root, metrics)) is not None
        )
        if not clusters:
            message = "No cluster could be evaluated from the supplied metrics."
            raise InvariantViolationError(message)
        return clusters

    def _cluster(self, node: HierarchyNode, metrics: Mapping[str, NormalizedMetric]) -> ClusterScore | None:
        """Aggregate one group node, or return ``None`` when it has no readings."""
        if not node.components:
            return None
        if node.components[0].is_leaf:
            contributions = tuple(self._metric(component, metrics) for component in node.components)
            score = self._weighted_average(
                [
                    (metric.normalized_value.unwrap(), metric.weight.unwrap())
                    for metric in contributions
                    if metric.normalized_value is not None
                ]
            )
            if score is None:
                return None
            return self._score(node, score, contributions=contributions)

        groups = tuple(
            group for component in node.components if (group := self._cluster(component, metrics)) is not None
        )
        score = self._weighted_average([(group.score.unwrap(), group.weight.unwrap()) for group in groups])
        if score is None:
            return None
        return self._score(node, score, groups, contributions=())

    @staticmethod
    def _score(
        node: HierarchyNode,
        score: NormalizedScore,
        groups: tuple[ClusterScore, ...] = (),
        contributions: tuple[MetricContribution, ...] = (),
    ) -> ClusterScore:
        """Build a cluster score from either nested groups or metric contributions."""
        return ClusterScore(
            key=AnalysisKey(node.key),
            score=score,
            weight=Weight(node.weight),
            contribution=Contribution(score.unwrap() * node.weight),
            subclusters=groups,
            metrics=contributions,
        )

    @staticmethod
    def _metric(node: HierarchyNode, metrics: Mapping[str, NormalizedMetric]) -> MetricContribution:
        """Build one metric contribution from its normalized reading."""
        normalized = metrics.get(node.key) or NormalizedMetric(
            key=AnalysisKey(node.key),
            raw_value=None,
            normalized_value=None,
        )
        return MetricContribution(
            key=AnalysisKey(node.key),
            raw_value=normalized.raw_value,
            normalized_value=normalized.normalized_value,
            weight=Weight(node.weight),
            contribution=(
                None
                if normalized.normalized_value is None
                else Contribution(normalized.normalized_value.unwrap() * node.weight)
            ),
            unit=normalized.unit,
            membership_function=normalized.function_name,
            membership_params=normalized.function_params,
        )

    @staticmethod
    def _weighted_average(pairs: list[tuple[float, float]]) -> NormalizedScore | None:
        """Return the weight-renormalized average of ``pairs``, or ``None``."""
        total_weight = sum(weight for _, weight in pairs)
        if total_weight <= 0:
            return None
        return NormalizedScore(sum(value * weight for value, weight in pairs) / total_weight)


__all__ = ("HierarchicalAggregator",)
