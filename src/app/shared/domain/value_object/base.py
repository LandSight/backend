import copy
from typing import ReadOnly, Self, final


class BaseValueObject[ValueT]:
    """Base class for immutable value objects."""

    __slots__ = ("_value",)
    _value: ReadOnly[ValueT]

    def __init__(self, value: ValueT) -> None:
        """Initialize a validated value object."""
        normalized = self._normalize(value)
        object.__setattr__(self, "_value", normalized)
        self._validate()

    def _normalize(self, value: ValueT) -> ValueT:
        """Normalize the value object."""
        raise NotImplementedError

    def _validate(self) -> None:
        """Validate normalized value against domain constraints."""
        raise NotImplementedError

    @classmethod
    def default(cls) -> BaseValueObject[ValueT]:
        """Return a default value object."""
        raise NotImplementedError

    @final
    def to_python(self) -> ValueT:
        """Return the value as a Python object."""
        return self._value

    @final
    def __setattr__(self, name: str, value: object) -> None:
        """Prevent attribute modification after creation."""
        raise AttributeError

    @final
    def __delattr__(self, name: str) -> None:
        """Prevent attribute deletion."""
        raise AttributeError

    def __repr__(self) -> str:
        """Return unambiguous string representation of the value object."""
        return f"{self.__class__.__name__}({self._value!r})"

    def __str__(self) -> str:
        """Return readable string representation."""
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        """Compare two value objects for equality."""
        if not isinstance(other, self.__class__):
            message = f"Cannot compare {self.__class__.__name__} with {type(other).__name__}"
            raise TypeError(message)
        return self._value == other._value

    def __hash__(self) -> int:
        """Compute hash value for use in collections."""
        return hash((self.__class__.__name__, self._value))

    def __copy__(self) -> Self:
        """Create a shallow copy of the value object."""
        return self

    def __deepcopy__(self, memo: dict) -> Self:
        """Create a deep copy of the value object."""
        return self.__class__(copy.deepcopy(self._value, memo))

    def __reduce__(self) -> tuple:
        """Support for pickling value objects."""
        return (self.__class__, (self._value,))
