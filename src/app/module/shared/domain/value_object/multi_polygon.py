"""MultiPolygon value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject
from app.module.shared.domain.value_object.polygon import Polygon


class MultiPolygon(BaseValueObject[tuple[tuple[Polygon, ...], ...]]):
    """MultiPolygon value object: one or more polygons that may have holes.

    Each part is a tuple whose first ring is the exterior boundary and whose
    remaining rings are holes (e.g. a forest relation with clearings or a
    village inside it).

    Invariants:
    - At least one part
    - Every part has an exterior ring
    """

    @override
    def _normalize(
        self,
        value: list[tuple[Polygon, ...]] | tuple[tuple[Polygon, ...], ...],
    ) -> tuple[tuple[Polygon, ...], ...]:
        return tuple(tuple(part) for part in value)

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "MultiPolygon must have at least one part."
            raise ValidationError(message)
        if any(not part for part in self._value):
            message = "Every MultiPolygon part must have an exterior ring."
            raise ValidationError(message)

    @property
    def parts(self) -> tuple[tuple[Polygon, ...], ...]:
        """Parts as ``(exterior, *holes)`` ring tuples."""
        return self._value


__all__ = ("MultiPolygon",)
