"""Hierarchical MCDA structure as a single recursive value object.

Every level of the aggregation tree is the same node type: a node with
components is a group, a node without components is a leaf metric. Whether a
node lands in the cluster or subcluster table is derived from its depth when
the evaluation is persisted, so the domain does not need separate cluster and
subcluster types.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.analysis_key import AnalysisKey
    from app.module.analysis.domain.value_object.analysis_type import AnalysisType
    from app.module.analysis.domain.value_object.weight import Weight


_MAX_METRIC_DEPTH = 2


@dataclass(frozen=True, slots=True)
class HierarchyNode(BaseCompositeValueObject):
    """A node of the aggregation tree.

    Attributes
    ----------
    key : AnalysisKey
        Metric key for a leaf, group key otherwise.
    weight : Weight
        Relative weight among siblings.
    components : tuple[HierarchyNode, ...]
        Child nodes; empty for a leaf metric.
    """

    key: AnalysisKey
    weight: Weight
    components: tuple[HierarchyNode, ...] = ()

    def _validate(self) -> None:
        if self.components:
            kinds = {component.is_leaf for component in self.components}
            if len(kinds) > 1:
                message = f"Node '{self.key.unwrap()}' must contain either only metrics or only groups."
                raise ValidationError(message)

    @property
    def is_leaf(self) -> bool:
        """Whether the node is a leaf metric rather than a group."""
        return not self.components


@dataclass(frozen=True, slots=True)
class Hierarchy(BaseCompositeValueObject):
    """A complete aggregation hierarchy for one analysis type.

    The tree is at most three levels deep: cluster (root) -> optional
    subcluster -> metric leaf. A cluster may also hold metrics directly.
    """

    analysis_type: AnalysisType
    model_version: str
    roots: tuple[HierarchyNode, ...] = field(default_factory=tuple)

    def _validate(self) -> None:
        if not self.model_version:
            message = "Hierarchy model version must not be empty."
            raise ValidationError(message)
        if not self.roots:
            message = "Hierarchy must define at least one root cluster."
            raise ValidationError(message)
        for root in self.roots:
            if root.is_leaf:
                message = f"Root cluster '{root.key.unwrap()}' must not be a leaf metric."
                raise ValidationError(message)
            self._validate_depth(root, depth=0)

    @classmethod
    def _validate_depth(cls, node: HierarchyNode, depth: int) -> None:
        """Ensure the tree does not exceed the supported depth."""
        if depth >= _MAX_METRIC_DEPTH:
            if node.components:
                message = f"Node '{node.key.unwrap()}' exceeds the maximum hierarchy depth of {_MAX_METRIC_DEPTH}."
                raise ValidationError(message)
            return
        for component in node.components:
            cls._validate_depth(component, depth + 1)

    def leaf_keys(self) -> tuple[str, ...]:
        """Return every leaf metric key referenced by the hierarchy."""
        keys: list[str] = []
        for root in self.roots:
            self._collect_leaf_keys(root, keys)
        return tuple(dict.fromkeys(keys))

    @classmethod
    def _collect_leaf_keys(cls, node: HierarchyNode, keys: list[str]) -> None:
        """Append the leaf keys of ``node`` to ``keys``, preserving order."""
        if node.is_leaf:
            keys.append(node.key.unwrap())
            return
        for component in node.components:
            cls._collect_leaf_keys(component, keys)


__all__ = ("Hierarchy", "HierarchyNode")
