"""Analysis evaluation reader port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class AnalysisService(ABC):
    """
    Gateway to the analysis modules' internal APIs.

    Implementations:
    - :class:`app.module.interpretation.infrastructure.gateway.analysis_service.AnalysisServiceImpl`
    """

    @abstractmethod
    async def read(self, analysis_id: UUID, current_user_id: UUID) -> EvaluationBreakdown:
        """Read the evaluation of an analysis and return the domain breakdown."""
        raise NotImplementedError


__all__ = ("AnalysisService",)
