"""Get topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetTopographyMetricsCommand:
    """Command for retrieving a specific topography metrics snapshot by its ID.

    Attributes
    ----------
    metrics_id : UUID
        ID of the metrics snapshot to retrieve.
    current_user_id : UUID
        ID of the user performing the request.
    """

    metrics_id: UUID
    current_user_id: UUID


__all__ = ("GetTopographyMetricsCommand",)
