"""Fail analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class FailAnalysisCommand:
    """Command for marking a queued analysis as failed.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis that failed.
    reason : str
        Human-readable failure reason.
    """

    analysis_id: UUID
    reason: str


__all__ = ("FailAnalysisCommand",)
