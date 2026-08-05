"""Polygon value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject, GeoPoint


class Polygon(BaseValueObject[tuple[GeoPoint, ...]]):
    """Polygon value object representing a simple geographic polygon.

    Invariants:
    - Minimum 3 distinct points (triangle)
    - No consecutive duplicate points
    - Automatically closed (first == last)
    """

    _MIN_POINTS = 3

    @override
    def _normalize(self, value: list[GeoPoint] | tuple[GeoPoint, ...]) -> tuple[GeoPoint, ...]:
        points = tuple(value)

        if points and points[0] != points[-1]:
            points = (*points, points[0])

        return points

    @override
    def _validate(self) -> None:
        if len(self._value) < self._MIN_POINTS + 1:
            message = f"Polygon must have at least {self._MIN_POINTS} distinct points, got {len(self._value) - 1}."
            raise ValidationError(message)

        self._validate_no_consecutive_duplicates()

    def _validate_no_consecutive_duplicates(self) -> None:
        """Check that no two consecutive points are identical."""
        for i in range(len(self._value) - 1):
            if self._value[i] == self._value[i + 1]:
                message = (
                    f"Polygon has consecutive duplicate points at index {i} and {i + 1}. "
                    "This creates a zero-length edge."
                )
                raise ValidationError(message)

    @property
    def points(self) -> tuple[GeoPoint, ...]:
        """All points including closing point."""
        return self._value

    @property
    def distinct_points(self) -> tuple[GeoPoint, ...]:
        """Points without the closing duplicate."""
        return self._value[:-1] if len(self._value) > 1 else self._value


__all__ = ("Polygon",)
