class BaseEntity[IdT]:
    """Base class for entities."""

    def __init__(self, id: IdT) -> None:
        self._id = id

    @property
    def id(self) -> IdT:
        """Public getter for the entity's unique identifier."""
        return self._id

    def __hash__(self) -> int:
        """Hash based on the class name and unique identifier to ensure consistent hashing for entities."""
        return hash((self.__class__.__name__, self._id))

    def __eq__(self, other: object) -> bool:
        """Check equality based on the unique identifier."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._id == other._id

    def __repr__(self) -> str:
        """Return unambiguous string representation of the entity."""
        return f"{self.__class__.__name__}(id={self._id!r})"
