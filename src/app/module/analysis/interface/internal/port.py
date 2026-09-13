"""Port (abstract base) for the Analysis module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.interface.internal.dto import (
        AnalysisResult,
        GetAnalysisInput,
        ListUserAnalysesInput,
        StartAnalysisInput,
    )


class AnalysisInternalAPI(ABC):
    """Abstract interface for the Analysis module's internal API.

    Implementations:
    - :class:`app.module.analysis.interface.internal.api.AnalysisInternal`
    """

    @abstractmethod
    async def start_analysis(self, input_data: StartAnalysisInput) -> AnalysisResult:
        """Start an analysis for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_analysis(self, input_data: GetAnalysisInput) -> AnalysisResult:
        """Retrieve an analysis by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def list_user_analyses(self, input_data: ListUserAnalysesInput) -> list[AnalysisResult]:
        """List all analyses of a user across all statuses."""
        raise NotImplementedError


__all__ = ("AnalysisInternalAPI",)
