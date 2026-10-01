"""Interpreter port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.entity import Interpretation
    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class Interpreter(ABC):
    """Turns an evaluation breakdown into a generated report.

    Implementations own the whole generation strategy (LLM, templates, ...) and
    must degrade gracefully: a generation failure yields fallback text instead
    of an error, so a report is always produced.

    Implementations:
    - :class:`app.module.interpretation.infrastructure.llm.interpreter.LlmInterpreter`
    """

    @abstractmethod
    async def explain(self, analysis_id: UUID, breakdown: EvaluationBreakdown) -> Interpretation:
        """Generate the interpretation report of a breakdown."""
        raise NotImplementedError


__all__ = ("Interpreter",)
