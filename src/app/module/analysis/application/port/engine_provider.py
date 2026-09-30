"""Engine catalog port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import Engine


class EngineProvider(ABC):
    """Port for listing the scoring engines available to analyses.

    Implementations:
    - :class:`app.module.analysis.infrastructure.provider.engine_provider.EngineProviderImpl`
    """

    @abstractmethod
    def list_engines(self) -> tuple[Engine, ...]:
        """Return every available scoring engine as a catalog descriptor.

        Returns
        -------
        tuple[Engine, ...]
            Engines in registration order.
        """
        raise NotImplementedError


__all__ = ("EngineProvider",)
