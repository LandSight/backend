"""Interpretation report repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.application.dto.response import InterpretationResultResponse


class InterpretationRepository(ABC):
    """Stores generated interpretation reports, one per analysis."""

    @abstractmethod
    async def get(self, analysis_id: UUID) -> InterpretationResultResponse | None:
        """Return the stored report of an analysis, or ``None``."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, analysis_id: UUID, result: InterpretationResultResponse) -> None:
        """Persist (insert or replace) the report of an analysis."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, analysis_id: UUID) -> None:
        """Delete the stored report of an analysis, if any."""
        raise NotImplementedError


__all__ = ("InterpretationRepository",)
