"""SQLAlchemy ORM model for User."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.constants import COLLATION_CI_TEXT_NAME
from app.platform.database.base import TimestampedModel


class UserModel(TimestampedModel):
    """ORM model for the User entity.

    Maps to the ``identity.users`` table.
    """

    __tablename__ = "users"
    __table_args__ = {"schema": "identity"}  # noqa: RUF012

    username: Mapped[str] = mapped_column(
        String(16, collation=COLLATION_CI_TEXT_NAME),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        repr=False,
    )


__all__ = ("UserModel",)
