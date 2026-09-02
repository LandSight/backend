from typing import override

import pytest

from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError


class DummyEntity(BaseEntity[int]):
    """Dummy entity for testing."""

    @override
    def _validate(self) -> None:
        pass


class DummyWithExtraEntity(BaseEntity[int]):
    """Dummy entity with extra validation for testing."""

    def __init__(self, id: int, extra: str) -> None:
        self._extra = extra
        super().__init__(id)

    @override
    def _validate(self) -> None:
        if self.extra == str(self.id):
            message = "Extra must not be equal to id"
            raise InvariantViolationError(message)

    @property
    def extra(self) -> str:
        """Extra value of the entity."""
        return self._extra


class TestBaseEntity:
    """Tests for BaseEntity class."""

    def test_create_with_valid_value(self) -> None:
        """Should create entity with valid value."""
        _ = DummyEntity(42)

    def test_create_with_invalid_value(self) -> None:
        """Should raise ValueError with invalid value."""
        with pytest.raises(InvariantViolationError, match="Extra must not be equal to id"):
            _ = DummyWithExtraEntity(1, "1")

    def test_equal_entity_with_same_id(self) -> None:
        """Should be equal when id are the same."""
        entity1 = DummyWithExtraEntity(42, "test1")
        entity2 = DummyWithExtraEntity(42, "test2")
        assert entity1 == entity2

    def test_not_equal_entity_with_different_id(self) -> None:
        """Should not be equal when id are different."""
        entity1 = DummyEntity(42)
        entity2 = DummyEntity(43)
        assert entity1 != entity2

    def test_not_equal_entity_with_different_type(self) -> None:
        """Should not be equal when type are different."""
        entity1 = DummyEntity(42)
        entity2 = DummyWithExtraEntity(42, "test")
        assert entity1 != entity2

    def test_hash_based_on_id(self) -> None:
        """Should compute hash from underlying value."""
        entity1 = DummyWithExtraEntity(1, "test")
        entity2 = DummyWithExtraEntity(1, "TEST")
        assert hash(entity1) == hash(entity2)

    def test_hash_different_for_different_id(self) -> None:
        """Should have different hashes for different values."""
        entity1 = DummyWithExtraEntity(1, "test")
        entity2 = DummyWithExtraEntity(2, "test")
        assert hash(entity1) != hash(entity2)

    def test_hash_different_for_different_types(self) -> None:
        """Should have different hashes for different types."""
        entity1 = DummyEntity(1)
        entity2 = DummyWithExtraEntity(1, "TEST")
        assert hash(entity1) != hash(entity2)

    def test_hash_different_for_non_entity(self) -> None:
        """Should have different hashes for different types."""
        entity = DummyEntity(1)
        assert hash(entity) != hash(1)

    def test_repr_shows_class_name_and_id(self) -> None:
        """Should show class name and value in repr."""
        entity = DummyWithExtraEntity(1, "test")
        assert repr(entity) == "DummyWithExtraEntity(id=1)"
