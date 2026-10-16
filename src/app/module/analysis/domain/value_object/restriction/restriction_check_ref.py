"""Reference to a restriction check used by an analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class RestrictionCheckRef:
    """Weak reference to a persisted restriction check snapshot.

    Restrictions are not metrics: they are facts with a legal effect that bar
    the scenario or lower the score after the multi-criteria breakdown, so the
    analysis keeps their snapshot apart from the metric references.

    Attributes
    ----------
    check_id : UUID
        ID of the restriction check snapshot.
    """

    check_id: UUID


__all__ = ("RestrictionCheckRef",)
