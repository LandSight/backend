"""Get infrastructure objects command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetInfrastructureObjectsCommand:
    """Command for retrieving the objects behind a metrics snapshot.

    Attributes
    ----------
    category : str
        Infrastructure category of the snapshot.
    metrics_id : UUID
        ID of the metrics snapshot whose buffer and parcel are reused.
    current_user_id : UUID
        ID of the user performing the request.
    """

    category: str
    metrics_id: UUID
    current_user_id: UUID


__all__ = ("GetInfrastructureObjectsCommand",)
