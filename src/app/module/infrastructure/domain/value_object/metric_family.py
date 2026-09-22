"""Metric family value object.

A family is the shape of metrics a category produces and maps directly to the
storage table that holds it. Several categories with the same metric shape share
one family: for example schools, hospitals and grocery shops are all
``facility`` metrics (count and minimum distance), while water bodies, forests
and protected areas are all ``ecology`` metrics.
"""

from __future__ import annotations

from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from app.module.infrastructure.domain.value_object.category import Category


if TYPE_CHECKING:
    from collections.abc import Mapping


class MetricFamily(StrEnum):
    """Shape of infrastructure metrics a category produces."""

    FACILITY = "facility"
    ECOLOGY = "ecology"
    UTILITY = "utility"
    ROAD_ACCESSIBILITY = "road_accessibility"
    GEOGRAPHIC_POSITION = "geographic_position"


CATEGORY_FAMILY: Final[Mapping[Category, MetricFamily]] = MappingProxyType(
    {
        Category.SCHOOL: MetricFamily.FACILITY,
        Category.HOSPITAL: MetricFamily.FACILITY,
        Category.GROCERY: MetricFamily.FACILITY,
        Category.BUS_STOP: MetricFamily.FACILITY,
        Category.RAILWAY_STATION: MetricFamily.FACILITY,
        Category.WATER_BODY: MetricFamily.ECOLOGY,
        Category.FOREST: MetricFamily.ECOLOGY,
        Category.PROTECTED_AREA: MetricFamily.ECOLOGY,
        Category.POWER_LINE: MetricFamily.UTILITY,
        Category.GAS_PIPELINE: MetricFamily.UTILITY,
        Category.WATER_PIPELINE: MetricFamily.UTILITY,
        Category.ROAD_ACCESSIBILITY: MetricFamily.ROAD_ACCESSIBILITY,
        Category.GEOGRAPHIC_POSITION: MetricFamily.GEOGRAPHIC_POSITION,
    },
)


def family_of(category: Category) -> MetricFamily:
    """Return the metric family a category belongs to."""
    return CATEGORY_FAMILY[category]


__all__ = ("CATEGORY_FAMILY", "MetricFamily", "family_of")
