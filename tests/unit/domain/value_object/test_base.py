from typing import override

import pytest

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject


class UpperStringValueObject(BaseValueObject[str]):
    """Test implementation of BaseValueObject for uppercase strings."""

    @override
    def _normalize(self, value: str) -> str:
        return value.strip().upper()

    @override
    def _validate(self) -> None:
        if len(self._value) < 3:
            message = "Value must be at least 3 characters"
            raise ValidationError(message)


class SimpleStringValueObject(BaseValueObject[str]):
    """Test implementation of BaseValueObject for strings."""

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()

    @override
    def _validate(self) -> None:
        pass


class ArrayValueObject(BaseValueObject[list]):
    """Test implementation of BaseValueObject for arrays."""

    def _normalize(self, value: list) -> list:
        return value

    def _validate(self) -> None:
        pass


class TestBaseValueObject:
    """Tests for BaseValueObject base class."""

    def test_create_with_valid_value(self) -> None:
        """Should create VO with valid value."""
        vo = SimpleStringValueObject("  Hello World  ")
        assert vo.unwrap() == "Hello World"

    def test_normalize_is_called_before_validate(self) -> None:
        """Should normalize value before validation."""
        with pytest.raises(ValidationError, match="at least 3 characters"):
            UpperStringValueObject("  AB  ")

    def test_equal_vos_with_same_value(self) -> None:
        """Should be equal when values are the same."""
        vo1 = UpperStringValueObject("TEST")
        vo2 = UpperStringValueObject("test")
        assert vo1 == vo2

    def test_not_equal_vos_with_different_values(self) -> None:
        """Should not be equal when values differ."""
        vo1 = UpperStringValueObject("test1")
        vo2 = UpperStringValueObject("test2")
        assert vo1 != vo2

    def test_not_equal_for_different_types(self) -> None:
        """Should not be equal when comparing with different VO type."""
        vo1 = UpperStringValueObject("test")
        vo2 = SimpleStringValueObject("TEST")
        assert vo1 != vo2

    def test_not_equal_for_non_vo(self) -> None:
        """Should not be equal when comparing with non-VO."""
        vo = UpperStringValueObject("test")
        assert vo != "TEST"

    def test_hash_based_on_value(self) -> None:
        """Should compute hash from underlying value."""
        vo1 = UpperStringValueObject("test")
        vo2 = UpperStringValueObject("test")
        assert hash(vo1) == hash(vo2)

    def test_hash_different_for_different_values(self) -> None:
        """Should have different hashes for different values."""
        vo1 = UpperStringValueObject("test1")
        vo2 = UpperStringValueObject("test2")
        assert hash(vo1) != hash(vo2)

    def test_hash_different_for_different_types(self) -> None:
        """Should have different hashes for different types."""
        vo1 = UpperStringValueObject("test")
        vo2 = SimpleStringValueObject("TEST")
        assert hash(vo1) != hash(vo2)

    def test_hash_different_for_non_vo(self) -> None:
        """Should have different hashes for different types."""
        vo = UpperStringValueObject("test")
        assert hash(vo) != hash("TEST")

    def test_repr_shows_class_name_and_value(self) -> None:
        """Should show class name and value in repr."""
        vo = UpperStringValueObject("test")
        assert repr(vo) == "UpperStringValueObject('TEST')"

    def test_unwrap_returns_normalized_value(self) -> None:
        """Should return the underlying value."""
        vo = UpperStringValueObject("test")
        assert vo.unwrap() == "TEST"

    def test_unwrap_returns_immutable_copy_for_mutable_types(self) -> None:
        """Should return value that can't modify original."""
        vo = ArrayValueObject([])
        value = vo.unwrap()

        value.append("test")
        assert vo.unwrap() != value

    def test_copy_incoming_value(self) -> None:
        """Should copy incoming value, not modify it."""
        value = []
        vo = ArrayValueObject(value)
        value.append("test")

        assert vo.unwrap() != value
