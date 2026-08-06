"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import (
        HospitalMetrics,
        SchoolMetrics,
        ShopMetrics,
        TransitStopMetrics,
        WaterBodyMetrics,
    )
    from app.module.infrastructure.domain.value_object import Buffer, ParcelId


class MetricsRepository(ABC):
    """Port for infrastructure metrics persistence.

    Each category has its own save and get methods dispatching to its dedicated
    table (e.g. ``parcel_school_metrics``).

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    # ----- Schools -----

    @abstractmethod
    async def save_schools(self, metrics: SchoolMetrics) -> None:
        """Persist school metrics.

        Parameters
        ----------
        metrics : SchoolMetrics
            School metrics entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_schools(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> SchoolMetrics | None:
        """Retrieve school metrics for a parcel.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        buffer : Buffer | None
            Buffer radius in meters. If provided, returns metrics for this
            exact buffer. If ``None``, returns the most recent metrics
            (ordered by ``computed_at DESC``).

        Returns
        -------
        SchoolMetrics | None
            School metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    # ----- Hospitals -----

    @abstractmethod
    async def save_hospitals(self, metrics: HospitalMetrics) -> None:
        """Persist hospital metrics.

        Parameters
        ----------
        metrics : HospitalMetrics
            Hospital metrics entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_hospitals(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> HospitalMetrics | None:
        """Retrieve hospital metrics for a parcel.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        buffer : Buffer | None
            Buffer radius in meters. If provided, returns metrics for this
            exact buffer. If ``None``, returns the most recent metrics
            (ordered by ``computed_at DESC``).

        Returns
        -------
        HospitalMetrics | None
            Hospital metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    # ----- Shops -----

    @abstractmethod
    async def save_shops(self, metrics: ShopMetrics) -> None:
        """Persist shop metrics.

        Parameters
        ----------
        metrics : ShopMetrics
            Shop metrics entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_shops(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> ShopMetrics | None:
        """Retrieve shop metrics for a parcel.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        buffer : Buffer | None
            Buffer radius in meters. If provided, returns metrics for this
            exact buffer. If ``None``, returns the most recent metrics
            (ordered by ``computed_at DESC``).

        Returns
        -------
        ShopMetrics | None
            Shop metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    # ----- Transit stops -----

    @abstractmethod
    async def save_transit_stops(self, metrics: TransitStopMetrics) -> None:
        """Persist transit stop metrics.

        Parameters
        ----------
        metrics : TransitStopMetrics
            Transit stop metrics entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_transit_stops(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> TransitStopMetrics | None:
        """Retrieve transit stop metrics for a parcel.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        buffer : Buffer | None
            Buffer radius in meters. If provided, returns metrics for this
            exact buffer. If ``None``, returns the most recent metrics
            (ordered by ``computed_at DESC``).

        Returns
        -------
        TransitStopMetrics | None
            Transit stop metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    # ----- Water bodies -----

    @abstractmethod
    async def save_water_bodies(self, metrics: WaterBodyMetrics) -> None:
        """Persist water body metrics.

        Parameters
        ----------
        metrics : WaterBodyMetrics
            Water body metrics entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_water_bodies(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> WaterBodyMetrics | None:
        """Retrieve water body metrics for a parcel.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        buffer : Buffer | None
            Buffer radius in meters. If provided, returns metrics for this
            exact buffer. If ``None``, returns the most recent metrics
            (ordered by ``computed_at DESC``).

        Returns
        -------
        WaterBodyMetrics | None
            Water body metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
