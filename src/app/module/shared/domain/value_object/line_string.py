"""LineString value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject
from app.module.shared.domain.value_object.geo_point import GeoPoint


class LineString(BaseValueObject[tuple[GeoPoint, ...]]):
    """LineString value object representing a simple geographic polyline.

    Invariants:
    - Minimum 2 points (a segment)
    - No consecutive duplicate points
    """

    _MIN_POINTS = 2

    @override
    def _normalize(self, value: list[GeoPoint] | tuple[GeoPoint, ...]) -> tuple[GeoPoint, ...]:
        return tuple(value)

    @override
    def _validate(self) -> None:
        if len(self._value) < self._MIN_POINTS:
            message = f"LineString must have at least {self._MIN_POINTS} points, got {len(self._value)}."
            raise ValidationError(message)

        for i in range(len(self._value) - 1):
            if self._value[i] == self._value[i + 1]:
                message = (
                    f"LineString has consecutive duplicate points at index {i} and {i + 1}. "
                    "This creates a zero-length segment."
                )
                raise ValidationError(message)

    @property
    def points(self) -> tuple[GeoPoint, ...]:
        """All points of the line."""
        return self._value


__all__ = ("LineString",)
