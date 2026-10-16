"""Analysis status value object."""

from __future__ import annotations

from enum import StrEnum


class AnalysisStatus(StrEnum):
    """Lifecycle status of an analysis."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


__all__ = ("AnalysisStatus",)
