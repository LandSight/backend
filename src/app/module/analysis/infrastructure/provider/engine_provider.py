"""Engine catalog provider backed by the packaged engine configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import EngineProvider
from app.module.analysis.domain.value_object import (
    AnalysisEngine,
    Engine,
    EngineDescription,
    EngineName,
)


if TYPE_CHECKING:
    from app.module.analysis.infrastructure.scorer.hmcda.config.models import EngineConfig


class EngineProviderImpl(EngineProvider):
    """Expose the engines described by the loaded engine configuration."""

    def __init__(self, config: EngineConfig) -> None:
        self._config = config

    @override
    def list_engines(self) -> tuple[Engine, ...]:
        """See :class:`app.module.analysis.application.port.EngineProvider.list_engines`."""
        return (
            Engine(
                key=AnalysisEngine(self._config.key),
                name=EngineName(self._config.name),
                description=EngineDescription(self._config.description),
                version=self._config.model_version,
            ),
        )


__all__ = ("EngineProviderImpl",)
