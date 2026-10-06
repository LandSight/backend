"""Analysis evaluation reader port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class AnalysisEvaluationReader(ABC):
    """Reads an analysis evaluation and maps it to the interpretation domain.

    The reader hides the analysis module behind its internal API: it performs
    the request and converts the recursive evaluation response into the flat
    domain breakdown (anti-corruption layer).
    """

    @abstractmethod
    async def read(self, analysis_id: UUID, current_user_id: UUID) -> EvaluationBreakdown:
        """Read the evaluation of an analysis and return the domain breakdown."""
        raise NotImplementedError


__all__ = ("AnalysisEvaluationReader",)
