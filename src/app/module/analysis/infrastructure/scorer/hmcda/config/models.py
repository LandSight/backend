"""Pydantic models for the HMCDA engine configuration.

The document is keyed by analysis type, so each profile owns its hierarchy and
its fuzzy functions. These models are the typed schema of the packaged
``engine.yaml``; the loader validates the raw YAML into them and the scorer maps
them into engine inputs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.module.analysis.domain.value_object import AnalysisType  # noqa: TC001 - needed at runtime for pydantic
from app.module.analysis.infrastructure.fuzzy.s_shaped import SShaped
from app.module.analysis.infrastructure.fuzzy.trapezoidal import Trapezoidal
from app.module.analysis.infrastructure.fuzzy.z_shaped import ZShaped


if TYPE_CHECKING:
    from app.module.analysis.infrastructure.ports import FuzzyFunction


_MAX_METRIC_DEPTH = 2


class HierarchyNode(BaseModel):
    """A node of the aggregation tree.

    Attributes
    ----------
    key : str
        Metric key for a leaf, group key otherwise.
    weight : float
        Relative weight among siblings; must be positive.
    components : list[HierarchyNode]
        Child nodes; empty for a leaf metric.
    """

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_:.-]+$")
    weight: float = Field(gt=0)
    components: list[HierarchyNode] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_children(self) -> Self:
        if self.components:
            kinds = {component.is_leaf for component in self.components}
            if len(kinds) > 1:
                message = f"Node '{self.key}' must contain either only metrics or only groups."
                raise ValueError(message)
        return self

    @property
    def is_leaf(self) -> bool:
        """Whether the node is a leaf metric rather than a group."""
        return not self.components


class Hierarchy(BaseModel):
    """The aggregation hierarchy of a profile.

    The tree is at most three levels deep: cluster (root) -> optional
    subcluster -> metric leaf. A cluster may also hold metrics directly.
    """

    model_config = ConfigDict(extra="forbid")

    clusters: list[HierarchyNode] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_tree(self) -> Self:
        for root in self.clusters:
            # A root that is itself a metric leaf is intentionally rejected: an
            # evaluation must contain at least one group so that it can produce a
            # ClusterScore. Flat MCDA stays possible as a single root group that
            # holds all metrics directly, so this is a modelling policy rather
            # than a limitation of the data.
            if root.is_leaf:
                message = f"Root cluster '{root.key}' must not be a leaf metric."
                raise ValueError(message)
            self._validate_depth(root, depth=0)
        return self

    @classmethod
    def _validate_depth(cls, node: HierarchyNode, depth: int) -> None:
        """Ensure the tree does not exceed the supported depth."""
        if depth >= _MAX_METRIC_DEPTH:
            if node.components:
                message = f"Node '{node.key}' exceeds the maximum hierarchy depth of {_MAX_METRIC_DEPTH}."
                raise ValueError(message)
            return
        for component in node.components:
            cls._validate_depth(component, depth + 1)

    def leaf_keys(self) -> tuple[str, ...]:
        """Return every leaf metric key referenced by the hierarchy."""
        keys: list[str] = []
        for root in self.clusters:
            self._collect_leaf_keys(root, keys)
        return tuple(dict.fromkeys(keys))

    @classmethod
    def _collect_leaf_keys(cls, node: HierarchyNode, keys: list[str]) -> None:
        """Append the leaf keys of ``node`` to ``keys``, preserving order."""
        if node.is_leaf:
            keys.append(node.key)
            return
        for component in node.components:
            cls._collect_leaf_keys(component, keys)


class ZShapedParams(BaseModel):
    """Parameters of a Z-shaped fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    optimal_max: float
    acceptable_max: float


class SShapedParams(BaseModel):
    """Parameters of an S-shaped fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    min: float
    max: float


class TrapezoidalParams(BaseModel):
    """Parameters of a trapezoidal fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    low: float
    optimal_min: float
    optimal_max: float
    high: float


class ZShapedConfig(BaseModel):
    """Configuration of a Z-shaped fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["z_shaped"]
    params: ZShapedParams
    unit: str = ""

    def to_domain(self) -> FuzzyFunction:
        """Build the concrete fuzzy function."""
        return ZShaped(
            unit=self.unit,
            optimal_max=self.params.optimal_max,
            acceptable_max=self.params.acceptable_max,
        )


class SShapedConfig(BaseModel):
    """Configuration of an S-shaped fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["s_shaped"]
    params: SShapedParams
    unit: str = ""

    def to_domain(self) -> FuzzyFunction:
        """Build the concrete fuzzy function."""
        return SShaped(unit=self.unit, minimum=self.params.min, maximum=self.params.max)


class TrapezoidalConfig(BaseModel):
    """Configuration of a trapezoidal fuzzy function."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["trapezoidal"]
    params: TrapezoidalParams
    unit: str = ""

    def to_domain(self) -> FuzzyFunction:
        """Build the concrete fuzzy function."""
        return Trapezoidal(
            unit=self.unit,
            low=self.params.low,
            optimal_min=self.params.optimal_min,
            optimal_max=self.params.optimal_max,
            high=self.params.high,
        )


FuzzyFunctionConfig = Annotated[
    ZShapedConfig | SShapedConfig | TrapezoidalConfig,
    Field(discriminator="type"),
]


class ProfileConfig(BaseModel):
    """Configuration of a single analysis profile."""

    model_config = ConfigDict(extra="forbid")

    hierarchy: Hierarchy
    functions: dict[str, FuzzyFunctionConfig] = Field(min_length=1)

    def to_fuzzy_functions(self) -> dict[str, FuzzyFunction]:
        """Build concrete fuzzy functions keyed by metric key."""
        return {key: function.to_domain() for key, function in self.functions.items()}


class EngineConfig(BaseModel):
    """Root configuration of the HMCDA engine, keyed by analysis type."""

    model_config = ConfigDict(extra="forbid")

    engine: Literal["hmcda"]
    model_version: str = Field(min_length=1)
    profiles: dict[AnalysisType, ProfileConfig] = Field(min_length=1)


HierarchyNode.model_rebuild()
Hierarchy.model_rebuild()


__all__ = (
    "EngineConfig",
    "FuzzyFunctionConfig",
    "Hierarchy",
    "HierarchyNode",
    "ProfileConfig",
    "SShapedConfig",
    "SShapedParams",
    "TrapezoidalConfig",
    "TrapezoidalParams",
    "ZShapedConfig",
    "ZShapedParams",
)
