"""Generate interpretation command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GenerateInterpretationCommand:
    """Command for generating an interpretation report.

    Generation always produces a fresh report: an existing report is replaced,
    so no ``force`` flag is needed.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("GenerateInterpretationCommand",)
