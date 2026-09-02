"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.topography.domain.entity.topography_metrics import TopographyMetrics
    from app.module.topography.domain.value_object.metric import ParcelId, TopographyMetricsId


class MetricsRepository(ABC):
    """Port for topography metrics persistence.

    Implementations:
    - :class:`app.module.topography.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def save(self, metrics: TopographyMetrics) -> TopographyMetrics:
        """Persist topography metrics and return the persisted entity.

        Parameters
        ----------
        metrics : TopographyMetrics
            Topography metrics entity to save.

        Returns
        -------
        TopographyMetrics
            The persisted entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, metrics_id: TopographyMetricsId) -> TopographyMetrics | None:
        """Retrieve topography metrics by their ID.

        Parameters
        ----------
        metrics_id : TopographyMetricsId
            Metrics identifier.

        Returns
        -------
        TopographyMetrics | None
            The metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_latest(self, parcel_id: ParcelId) -> TopographyMetrics | None:
        """Retrieve the most recent topography metrics for a parcel.

        Since a parcel can accumulate multiple snapshots over time, this returns
        the latest one (ordered by creation time).

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.

        Returns
        -------
        TopographyMetrics | None
            The latest metrics if any exist, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, parcel_id: ParcelId) -> list[TopographyMetrics]:
        """List all topography metrics snapshots for a parcel, newest first.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.

        Returns
        -------
        list[TopographyMetrics]
            All metrics snapshots for the parcel ordered by creation time
            descending.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
