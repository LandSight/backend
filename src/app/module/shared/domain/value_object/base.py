from abc import ABC, abstractmethod
from copy import deepcopy


class BaseValueObject[ValueT](ABC):
    """Base class for all value objects."""

    def __init__(self, value: ValueT) -> None:
        self._value = self._normalize(deepcopy(value))
        self._validate()

    @abstractmethod
    def _normalize(self, value: ValueT) -> ValueT:
        """Return the normalized value."""

    @abstractmethod
    def _validate(self) -> None:
        """Validate the value."""

    def unwrap(self) -> ValueT:
        """Return the underlying value."""
        return deepcopy(self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._value))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value!r})"


class BaseCompositeValueObject(ABC):
    """Base class for value objects composed of multiple fields.

    Unlike :class:`BaseValueObject`, which wraps a single value, a composite
    value object validates its own fields. Subclasses are frozen dataclasses:
    the dataclass-generated ``__init__`` calls the inherited ``__post_init__``,
    which in turn runs :meth:`_validate` on construction.
    """

    def __post_init__(self) -> None:
        """Validate the composite value after the dataclass initializes it."""
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """Validate the composite value's fields."""


__all__ = ("BaseCompositeValueObject", "BaseValueObject")
