"""Internal DTOs for the Analysis module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class StartAnalysisInput:
    """Input for starting an analysis of a parcel."""

    parcel_id: UUID
    current_user_id: UUID
    name: str


@dataclass(frozen=True, slots=True)
class GetAnalysisInput:
    """Input for retrieving an analysis by its ID."""

    analysis_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ListUserAnalysesInput:
    """Input for listing all analyses of a user."""

    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Result of an analysis operation."""

    id: UUID
    parcel_id: UUID
    name: str
    status: str
    stage: str
    score: float | None
    status_reason: str | None
    created_at: datetime.datetime | None


__all__ = (
    "AnalysisResult",
    "GetAnalysisInput",
    "ListUserAnalysesInput",
    "StartAnalysisInput",
)
