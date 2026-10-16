"""Restriction permission service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class RestrictionPermissionService(ABC):
    """Port for resolving whether a user may access a parcel's restriction checks.

    A user may read and delete the checks of the parcels they own.

    Implementations:
    - :class:`app.module.restriction.infrastructure.permission.restriction_permission_service.RestrictionPermissionServiceImpl`
    """

    @abstractmethod
    async def user_can_view_parcel(self, user_id: UUID, parcel_id: UUID) -> bool:
        """Return whether the user may access the restriction checks of the parcel.

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


__all__ = ("RestrictionPermissionService",)
