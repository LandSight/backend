"""Interpretation service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class InterpretationService(ABC):
    """Gateway to the Interpretation module's internal API.

    The start is expected to run inside the caller's transaction, so the report
    row and the outbox event are committed atomically with the analysis
    completion.

    Implementations:
    - :class:`app.module.analysis.infrastructure.gateways.interpretation_service.InterpretationServiceImpl`
    """

    @abstractmethod
    async def start(self, analysis_id: UUID, current_user_id: UUID) -> None:
        """Start generation of the interpretation report of an analysis."""
        raise NotImplementedError


__all__ = ("InterpretationService",)
