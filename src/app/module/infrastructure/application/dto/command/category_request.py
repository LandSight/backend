"""Category request DTO for infrastructure metrics calculation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import Category


@dataclass(frozen=True, slots=True)
class CategoryRequest:
    """Requested infrastructure category with its own buffer radius.

    Attributes
    ----------
    category : Category
        Infrastructure object category to compute metrics for.
    buffer : int
        Buffer radius in meters around the parcel boundary for this category.
    """

    category: Category
    buffer: int


__all__ = ("CategoryRequest",)
