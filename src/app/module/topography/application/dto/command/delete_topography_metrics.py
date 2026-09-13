"""Delete topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class DeleteTopographyMetricsCommand:
    """Command for deleting topography metrics snapshots by their IDs."""

    metrics_ids: list[UUID] = field(default_factory=list)


__all__ = ("DeleteTopographyMetricsCommand",)
