"""Declarative base for SQLAlchemy ORM models."""

import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


metadata = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class BaseModel(MappedAsDataclass, DeclarativeBase, kw_only=True):
    """Base class for all ORM models."""

    __abstract__ = True

    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid6,
        kw_only=True,
    )


class TimestampedModel(BaseModel):
    """Base model with created_at and updated_at timestamps."""

    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC),
        kw_only=True,
        repr=False,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.timezone("utc", sa.func.now()),
        server_onupdate=sa.func.timezone("utc", sa.func.now()),
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC),
        kw_only=True,
        repr=False,
    )


__all__ = (
    "BaseModel",
    "TimestampedModel",
)
