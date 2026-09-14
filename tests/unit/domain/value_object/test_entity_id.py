from uuid import uuid4, uuid6

import pytest

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.entity_id import EntityIdUUID6ValueObject


class TestEntityIdUUID6ValueObject:
    """Tests for s class."""

    def test_create_with_valid_value(self) -> None:
        """Should create VO with valid value."""
        value = uuid6()
        _ = EntityIdUUID6ValueObject(value)

    def test_create_with_invalid_uuid_version(self) -> None:
        """Should raise error for invalid UUID version."""
        value = uuid4()
        with pytest.raises(ValidationError, match="Invalid UUID version: 4"):
            _ = EntityIdUUID6ValueObject(value)
