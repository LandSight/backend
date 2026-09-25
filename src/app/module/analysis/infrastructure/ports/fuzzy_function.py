"""Fuzzy membership function abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar


if TYPE_CHECKING:
    from collections.abc import Mapping


class FuzzyFunction(ABC):
    """A fuzzy membership function mapping a raw value to ``mu`` in ``[0, 1]``.

    Concrete functions are interchangeable strategies: the fuzzy normalizer
    only relies on ``__call__`` and never on a specific shape.

    Attributes
    ----------
    name : ClassVar[str]
        Machine name of the function (matches the configuration ``type``).
    unit : str
        Unit of the raw metric the function normalizes.
    """

    name: ClassVar[str]

    def __init__(self, unit: str = "") -> None:
        self.unit: str = unit

    @abstractmethod
    def __call__(self, value: float) -> float:
        """Return the membership of ``value`` in ``[0, 1]``."""
        raise NotImplementedError

    def params(self) -> Mapping[str, float]:
        """Return the parameters that define this function."""
        return MappingProxyType({})

    @staticmethod
    def clamp(value: float) -> float:
        """Clamp a membership value to the closed ``[0, 1]`` range."""
        return max(0.0, min(1.0, value))


__all__ = ("FuzzyFunction",)
