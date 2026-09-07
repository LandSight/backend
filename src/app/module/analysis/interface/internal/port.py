"""Port (abstract base) for the Analysis module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.interface.internal.dto import AnalyzeParcelInput, ParcelAnalysisResult


class AnalysisInternalAPI(ABC):
    """Abstract interface for the Analysis module's internal API.

    This is the framework-agnostic contract that the HTTP layer
    (``app/interface/http/controller/analysis/``) depends on.

    Implementations:
    - :class:`app.module.analysis.interface.internal.api.AnalysisInternal`
    """

    @abstractmethod
    async def analyze_parcel(self, input_data: AnalyzeParcelInput) -> ParcelAnalysisResult:
        """Aggregate all metrics of a parcel."""
        raise NotImplementedError


__all__ = ("AnalysisInternalAPI",)
