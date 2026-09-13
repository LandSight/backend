"""Analysis repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.entity import Analysis
    from app.module.analysis.domain.value_object import AnalysisId, AnalysisMetricRef


class AnalysisRepository(ABC):
    """Port for analysis persistence.

    Implementations:
    - :class:`app.module.analysis.infrastructure.repository.postgres_analysis_repository.PostgresAnalysisRepository`
    """

    @abstractmethod
    async def save(self, analysis: Analysis) -> Analysis:
        """Persist an analysis (insert or update) and return it.

        Parameters
        ----------
        analysis : Analysis
            The analysis aggregate to persist.

        Returns
        -------
        Analysis
            The persisted analysis.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, analysis_id: AnalysisId) -> Analysis | None:
        """Retrieve an analysis by its ID.

        Parameters
        ----------
        analysis_id : AnalysisId
            Analysis identifier.

        Returns
        -------
        Analysis | None
            The analysis if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, analysis_id: AnalysisId) -> None:
        """Delete an analysis and its metric references.

        Metric snapshots owned by other modules are left untouched.

        Parameters
        ----------
        analysis_id : AnalysisId
            Analysis identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_parcel_ids(self, parcel_ids: list[UUID]) -> list[Analysis]:
        """List analyses belonging to the given parcels.

        Results are ordered by creation time, newest first.

        Parameters
        ----------
        parcel_ids : list[UUID]
            Parcel identifiers to filter by.

        Returns
        -------
        list[Analysis]
            Matching analyses; empty if ``parcel_ids`` is empty.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_metrics(self, analysis_id: AnalysisId, metrics: list[AnalysisMetricRef]) -> None:
        """Replace the metric references for the metric types present in ``metrics``.

        Only rows whose ``metric_type`` appears in ``metrics`` are replaced, so
        independent metric modules can persist their references concurrently
        without clobbering each other.

        Parameters
        ----------
        analysis_id : AnalysisId
            Owning analysis identifier.
        metrics : list[AnalysisMetricRef]
            Metric references to store.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, analysis_id: AnalysisId) -> list[AnalysisMetricRef]:
        """Retrieve the metric references recorded for an analysis.

        Parameters
        ----------
        analysis_id : AnalysisId
            Owning analysis identifier.

        Returns
        -------
        list[AnalysisMetricRef]
            Metric references, empty if none were recorded.
        """
        raise NotImplementedError


__all__ = ("AnalysisRepository",)
