"""Interpretation grader port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GradeVerdict:
    """Outcome of verifying a generated explanation against its source facts."""

    ok: bool
    issues: tuple[str, ...] = field(default_factory=tuple)
    corrected_text: str | None = None


class InterpretationGrader(ABC):
    """Verifies that a generated explanation is grounded in the source facts.

    The grader is a second LLM pass: it checks for hallucinated values, format
    violations and wrong language, and may propose a corrected text. It must not
    introduce new facts of its own.
    """

    @abstractmethod
    async def grade(self, facts: str, explanation: str) -> GradeVerdict:
        """Grade ``explanation`` against ``facts``."""
        raise NotImplementedError


__all__ = ("GradeVerdict", "InterpretationGrader")
