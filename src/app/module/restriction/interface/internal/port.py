"""Port (abstract base) for the Restriction module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.restriction.interface.internal.dto import (
        CalculateCheckInput,
        DeleteChecksInput,
        GetCheckInput,
        RestrictionCheckResult,
    )


class RestrictionInternalAPI(ABC):
    """Abstract interface for the Restriction module's internal API.

    Implementations:
    - :class:`app.module.restriction.interface.internal.api.RestrictionInternal`
    """

    @abstractmethod
    async def calculate_check(self, input_data: CalculateCheckInput) -> RestrictionCheckResult:
        """Calculate the restriction check of a parcel and store the snapshot."""
        raise NotImplementedError

    @abstractmethod
    async def get_check(self, input_data: GetCheckInput) -> RestrictionCheckResult:
        """Retrieve a restriction check snapshot by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_checks(self, input_data: DeleteChecksInput) -> None:
        """Delete restriction check snapshots of the current user's parcels by their IDs."""
        raise NotImplementedError


__all__ = ("RestrictionInternalAPI",)
