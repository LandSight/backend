"""Aspect explanation value object."""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


@dataclass(frozen=True, slots=True)
class AspectExplanation(BaseCompositeValueObject):
    """Generated explanation text of a single aspect.

    Attributes
    ----------
    key : str
        Aspect (cluster) key the text explains.
    text : str
        Generated explanation text.
    """

    key: str
    text: str

    def _validate(self) -> None:
        if not self.key:
            message = "Aspect explanation key must not be empty."
            raise ValidationError(message)


__all__ = ("AspectExplanation",)
