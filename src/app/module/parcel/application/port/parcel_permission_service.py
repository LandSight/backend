"""Parcel permission service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.parcel.domain.value_object import OwnerId, ParcelId


class ParcelPermissionService(ABC):
    """Port for checking parcel access permissions.

    Provides reusable, side-effect-free permission predicates expressed as
    *actions* (view, manage). Use cases consult this port before
    performing an action and raise a business-layer error when access is
    denied.

    Implementations MUST treat a missing parcel the same as a parcel the user
    does not own -- both return ``False``. Permission checks are predicates
    and therefore never raise; raising would both violate layer boundaries
    and reveal whether a specific parcel exists (information disclosure).

    Implementations:
    - :class:`app.module.parcel.infrastructure.permission.parcel_permission_service.ParcelPermissionServiceImpl`
    """

    @abstractmethod
    async def is_owner(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """Check whether the user owns the parcel (raw ownership predicate).

        Parameters
        ----------
        user_id : OwnerId
            ID of the user.
        parcel_id : ParcelId
            ID of the parcel.

        Returns
        -------
        bool
            ``True`` if the user owns the parcel, ``False`` otherwise
            (including when the parcel does not exist).
        """
        raise NotImplementedError

    @abstractmethod
    async def user_can_view_parcel(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """Check whether the user is allowed to view the parcel.

        Parameters
        ----------
        user_id : OwnerId
            ID of the user.
        parcel_id : ParcelId
            ID of the parcel.

        Returns
        -------
        bool
            ``True`` if the user can view the parcel, ``False`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def user_can_manage_parcel(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """Check whether the user is allowed to manage (modify/delete/use) the parcel.

        Parameters
        ----------
        user_id : OwnerId
            ID of the user.
        parcel_id : ParcelId
            ID of the parcel.

        Returns
        -------
        bool
            ``True`` if the user can manage the parcel, ``False`` otherwise.
        """
        raise NotImplementedError


__all__ = ("ParcelPermissionService",)
