"""Cancel interpretation command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CancelInterpretationCommand:
    """Command for cancelling the generation of an interpretation report."""

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("CancelInterpretationCommand",)
