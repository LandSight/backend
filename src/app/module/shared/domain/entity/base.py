from abc import ABC, abstractmethod


class BaseEntity[IdT](ABC):
    """Base class for all entities."""

    def __init__(self, id: IdT) -> None:
        self._id: IdT = id

    @abstractmethod
    def _validate(self) -> None:
        """Validate the entity's state."""

    @property
    def id(self) -> IdT:
        """Returns the entity's ID."""
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._id))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"


__all__ = ("BaseEntity",)
