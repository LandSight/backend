"""Category info response DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryInfoResponse:
    """DTO for available infrastructure category information.

    Attributes
    ----------
    category : str
        Category identifier (e.g. "school", "water_body").
    label : str
        Human-readable category name for the UI (e.g. "Schools").
    """

    category: str
    label: str


__all__ = ("CategoryInfoResponse",)
