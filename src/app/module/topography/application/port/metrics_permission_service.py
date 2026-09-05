"""Metrics permission service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class MetricsPermissionService(ABC):
    """Port for checking access to topography metrics.

    Topography use cases consult this port before serving metrics so that a
    user cannot read another owner's data. Implementations MUST treat a
    missing parcel the same as a parcel the user does not own -- both return
    ``False``. Permission checks are predicates and therefore never raise.

    Implementations:
    - :class:`app.module.topography.infrastructure.permission.metrics_permission_service.MetricsPermissionServiceImpl`
    """

    @abstractmethod
    async def user_can_view_parcel_metrics(self, user_id: UUID, parcel_id: UUID) -> bool:
        """Check whether the user can view topography metrics for the parcel.

        Parameters
        ----------
        user_id : UUID
            ID of the user.
        parcel_id : UUID
            ID of the parcel.

        Returns
        -------
        bool
            ``True`` if the user can view the metrics, ``False`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsPermissionService",)
