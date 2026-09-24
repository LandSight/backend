"""Static infrastructure metric policy.

Thresholds that define what counts as a *large* natural object per category.
These are base domain parameters, not environment-specific settings, so they
live in code as the single source of truth.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from app.module.infrastructure.domain.value_object import Category


if TYPE_CHECKING:
    from collections.abc import Mapping


LARGE_OBJECT_MIN_AREA_M2: Final[Mapping[Category, float]] = MappingProxyType(
    {
        Category.WATER_BODY: 1_000_000.0,
        Category.FOREST: 500_000.0,
        Category.PROTECTED_AREA: 1_000_000.0,
    },
)


__all__ = ("LARGE_OBJECT_MIN_AREA_M2",)
