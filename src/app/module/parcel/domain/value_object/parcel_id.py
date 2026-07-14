from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class ParcelId(EntityIdUUID6ValueObject):
    """Parcel ID value object using UUID6."""


__all__ = ("ParcelId",)
