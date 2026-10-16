"""Port (abstract base) for the Interpretation module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.interpretation.interface.internal.dto import (
        CancelInterpretationInput,
        GenerateInterpretationInput,
        GetInterpretationInput,
        InterpretationResult,
    )


class InterpretationInternalAPI(ABC):
    """Abstract interface for the Interpretation module's internal API.

    Implementations:
    - :class:`app.module.interpretation.interface.internal.api.InterpretationInternal`
    """

    @abstractmethod
    async def get_interpretation(self, input_data: GetInterpretationInput) -> InterpretationResult:
        """Return the stored interpretation report of an analysis."""
        raise NotImplementedError

    @abstractmethod
    async def start_interpretation(self, input_data: GenerateInterpretationInput) -> InterpretationResult:
        """Start generation of an interpretation report of an analysis."""
        raise NotImplementedError

    @abstractmethod
    async def cancel_interpretation(self, input_data: CancelInterpretationInput) -> InterpretationResult:
        """Cancel the generation of an interpretation report of an analysis."""
        raise NotImplementedError


__all__ = ("InterpretationInternalAPI",)
