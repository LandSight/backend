"""Infrastructure metric catalog.

The catalog is the module's domain knowledge about its metrics: for each
category it declares the metric keys, labels, units and value kinds. The
internal API projects category responses into the neutral metric contract by
iterating these definitions, so adding a metric means extending the catalog and
the matching entity/DTO fields.

Metric keys are generic within a family (``count``, ``min_distance_to``,
``coverage_ratio``): the kind of object is already carried by the response
category, so no per-category key duplication is needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from app.module.shared.domain.value_object import MetricValueKind


if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    """Definition of a single infrastructure metric."""

    key: str
    label: str
    unit: str
    kind: MetricValueKind


_BUFFER = MetricDefinition("buffer", "Buffer", "m", MetricValueKind.INTEGER)
_COUNT = MetricDefinition("count", "Count", "", MetricValueKind.INTEGER)
_MIN_DISTANCE = MetricDefinition("min_distance_to", "Min distance to", "m", MetricValueKind.NUMBER)
_COVERAGE_RATIO = MetricDefinition("coverage_ratio", "Coverage ratio", "ratio", MetricValueKind.NUMBER)
_DISTANCE_TO_LARGE_OBJECT = MetricDefinition(
    "distance_to_large_object",
    "Distance to large object",
    "m",
    MetricValueKind.NUMBER,
)

_FACILITY_METRICS: Final[tuple[MetricDefinition, ...]] = (_BUFFER, _COUNT, _MIN_DISTANCE)
_ECOLOGY_METRICS: Final[tuple[MetricDefinition, ...]] = (
    _BUFFER,
    _COVERAGE_RATIO,
    _COUNT,
    _MIN_DISTANCE,
    _DISTANCE_TO_LARGE_OBJECT,
)
_UTILITY_METRICS: Final[tuple[MetricDefinition, ...]] = (_BUFFER, _MIN_DISTANCE)


CATEGORY_METRICS: Final[Mapping[str, tuple[MetricDefinition, ...]]] = MappingProxyType(
    {
        "school": _FACILITY_METRICS,
        "hospital": _FACILITY_METRICS,
        "grocery": _FACILITY_METRICS,
        "bus_stop": _FACILITY_METRICS,
        "railway_station": _FACILITY_METRICS,
        "water_body": _ECOLOGY_METRICS,
        "forest": _ECOLOGY_METRICS,
        "protected_area": _ECOLOGY_METRICS,
        "power_line": _UTILITY_METRICS,
        "gas_pipeline": _UTILITY_METRICS,
        "water_pipeline": _UTILITY_METRICS,
        "road_accessibility": (
            _BUFFER,
            MetricDefinition("distance_to_paved_road", "Distance to paved road", "m", MetricValueKind.NUMBER),
            MetricDefinition("road_density_1km", "Road density (1 km)", "km/km2", MetricValueKind.NUMBER),
        ),
        "geographic_position": (
            _BUFFER,
            MetricDefinition("distance_to_major_city", "Distance to major city", "m", MetricValueKind.NUMBER),
            MetricDefinition("city_tier", "City tier", "", MetricValueKind.TEXT),
        ),
    },
)


__all__ = ("CATEGORY_METRICS", "MetricDefinition")
