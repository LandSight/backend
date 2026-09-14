"""Infrastructure object ID value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class InfrastructureObjectId(BaseValueObject[str]):
    """Identifier of an infrastructure object from the data source.

    The identifier is source-agnostic (e.g. an OSM node id, a 2GIS id, or any
    other provider's id) and is represented as a string.

    Invariants:
    - Must be a non-empty string
    """

    @override
    def _normalize(self, value: str) -> str:
        return str(value).strip()

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Infrastructure object id must not be empty."
            raise ValidationError(message)


__all__ = ("InfrastructureObjectId",)
