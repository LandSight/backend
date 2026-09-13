"""Category metric request DTO for retrieving specific metrics by ID."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CategoryMetricRequest:
    """Reference to a specific infrastructure metrics record within a category.

    Attributes
    ----------
    category : str
        Category of the metrics record; selects the dedicated storage table.
    metrics_id : UUID
        ID of the metrics record.
    """

    category: str
    metrics_id: UUID


__all__ = ("CategoryMetricRequest",)
