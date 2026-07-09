from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class UserId(EntityIdUUID6ValueObject):
    """User ID value object using UUID6."""


__all__ = ("UserId",)
