"""Restriction check repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.restriction.domain.entity import RestrictionCheck
    from app.module.restriction.domain.value_object import RestrictionCheckId


class CheckRepository(ABC):
    """Port for restriction check persistence.

    Implementations:
    - :class:`app.module.restriction.infrastructure.repository.postgres_check_repository.PostgresCheckRepository`
    """

    @abstractmethod
    async def save(self, check: RestrictionCheck) -> RestrictionCheck:
        """Persist a restriction check and return the persisted entity."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, check_id: RestrictionCheckId) -> RestrictionCheck | None:
        """Retrieve a restriction check by its ID, or ``None`` if not found."""
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_ids(self, check_ids: list[UUID]) -> dict[UUID, UUID]:
        """Return the parcel ID of each existing check, keyed by check ID; missing checks are left out."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, check_ids: list[UUID]) -> None:
        """Delete restriction check snapshots by their IDs."""
        raise NotImplementedError


__all__ = ("CheckRepository",)
