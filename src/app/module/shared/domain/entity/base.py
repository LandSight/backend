from abc import ABC, abstractmethod


class BaseEntity[IdT](ABC):
    """Base class for all entities.

    Attributes
    ----------
    id : IdT
        The entity's ID.

    Notes
    -----
    When overriding ``__init__`` in a subclass, call ``super().__init__(id)``
    at the **end** of your custom ``__init__`` method. This ensures:

    1. All subclass attributes are set before ``_validate()`` runs
    2. The ``_id`` field is properly initialized
    3. The overridden ``_validate()`` method can access all attributes


    Example
    -------
    >>> class User(BaseEntity[int]):
    ...     def __init__(self, id: int, name: str) -> None:
    ...         self.name = name  # Set subclass attributes first
    ...         super().__init__(id)  # Then call parent __init__
    ...
    ...     def _validate(self) -> None:
    ...         if not self.name:  # Can safely access self.name here
    ...             raise ValidationError("Name is required")
    """

    def __init__(self, id: IdT) -> None:
        self._id: IdT = id
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """Validate the entity's state."""

    @property
    def id(self) -> IdT:
        """The entity ID."""
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
