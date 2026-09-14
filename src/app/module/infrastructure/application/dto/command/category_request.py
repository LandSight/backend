"""Category request DTO for infrastructure metrics calculation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryRequest:
    """Requested infrastructure category with its own buffer radius.

    Attributes
    ----------
    category : str
        Category to compute metrics for.
    buffer : int
        Buffer radius in meters around the parcel boundary for this category.
    """

    category: str
    buffer: int


__all__ = ("CategoryRequest",)
