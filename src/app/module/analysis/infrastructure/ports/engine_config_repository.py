"""Engine configuration repository abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object import AnalysisType, Hierarchy
    from app.module.analysis.infrastructure.ports.fuzzy_function import FuzzyFunction


class EngineConfigRepository(ABC):
    """Provides the configured engine inputs for an analysis type.

    Implementations own where the configuration comes from (packaged YAML,
    database, remote service), so the scoring pipeline stays source-agnostic.

    Implementations:
    - :class:`app.module.analysis.infrastructure.repository.yaml_engine_config_repository.YamlEngineConfigRepository`
    """

    @abstractmethod
    def get_hierarchy(self, analysis_type: AnalysisType) -> Hierarchy:
        """Return the aggregation hierarchy for ``analysis_type``."""
        raise NotImplementedError

    @abstractmethod
    def get_fuzzy_functions(self, analysis_type: AnalysisType) -> Mapping[str, FuzzyFunction]:
        """Return fuzzy functions keyed by metric key for ``analysis_type``."""
        raise NotImplementedError


__all__ = ("EngineConfigRepository",)
