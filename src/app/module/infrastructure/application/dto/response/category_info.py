"""Category info response DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryInfoResponse:
    """DTO for available infrastructure category information.

    Attributes
    ----------
    category : str
        Category identifier (e.g., "schools", "hospitals").
    """

    category: str


__all__ = ("CategoryInfoResponse",)
