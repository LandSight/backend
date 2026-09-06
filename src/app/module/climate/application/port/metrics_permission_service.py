"""Metrics permission service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class MetricsPermissionService(ABC):
    """Port for resolving whether a user may view a parcel's metrics.

    Implementations:
    - :class:`app.module.climate.infrastructure.permission.metrics_permission_service.MetricsPermissionServiceImpl`
    """

    @abstractmethod
    async def user_can_view_parcel_metrics(self, user_id: UUID, parcel_id: UUID) -> bool:
        """Return whether the user is allowed to view the parcel's metrics.

        Parameters
        ----------
        user_id : UUID
            ID of the user.
        parcel_id : UUID
            ID of the parcel.

        Returns
        -------
        bool
            True if the user owns the parcel, False otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsPermissionService",)
