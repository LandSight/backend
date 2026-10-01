"""Interpretation report repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.entity import Interpretation


class InterpretationRepository(ABC):
    """Stores generated interpretation reports, one per analysis."""

    @abstractmethod
    async def get(self, analysis_id: UUID) -> Interpretation | None:
        """Return the stored report of an analysis, or ``None``."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, interpretation: Interpretation) -> Interpretation:
        """Persist the report and return the flushed entity."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, analysis_id: UUID) -> None:
        """Delete the stored report of an analysis, if any."""
        raise NotImplementedError


__all__ = ("InterpretationRepository",)
