"""Restriction service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import RestrictionCheck, RestrictionCheckRef


class RestrictionService(ABC):
    """Gateway to the restriction module's internal API.

    Implementations:
    - :class:`app.module.analysis.infrastructure.gateway.restriction_service.RestrictionServiceImpl`
    """

    @abstractmethod
    async def calculate(self, parcel_id: UUID, user_id: UUID) -> RestrictionCheckRef:
        """Calculate and persist the restriction check of a parcel; return a reference to it."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, ref: RestrictionCheckRef, user_id: UUID) -> RestrictionCheck:
        """Get the restriction check behind a reference, with all its hits."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, refs: list[RestrictionCheckRef], user_id: UUID) -> None:
        """Delete restriction check snapshots on behalf of the user."""
        raise NotImplementedError


__all__ = ("RestrictionService",)
