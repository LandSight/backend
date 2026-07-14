"""PostgreSQL user repository implementation."""

from typing import TYPE_CHECKING, override

from sqlalchemy import select

from app.module.identity.application.port import UserRepository
from app.module.identity.domain.entity import User
from app.module.identity.domain.value_object import (
    HashedPassword,
    UserId,
    Username,
)
from app.module.identity.infrastructure.model import UserModel
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresUserRepository(BaseSQLAlchemyRepository, UserRepository):
    """User repository backed by PostgreSQL via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, user: User) -> None:
        """See :class:`app.module.identity.application.port.UserRepository.save`."""
        model = UserModel(
            id=user.id.unwrap(),
            username=user.username.unwrap(),
            hashed_password=user.hashed_password.unwrap(),
        )
        self._session.add(model)

    @override
    async def get_by_id(self, user_id: UserId) -> User | None:
        """See :class:`app.module.identity.application.port.UserRepository.get_by_id`."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id.unwrap()),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @override
    async def get_by_username(self, username: Username) -> User | None:
        """See :class:`app.module.identity.application.port.UserRepository.get_by_username`."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username.unwrap()),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @override
    async def delete(self, user_id: UserId) -> None:
        """See :class:`app.module.identity.application.port.UserRepository.delete`."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id.unwrap()),
        )
        model = result.scalar_one_or_none()
        if model is not None:
            await self._session.delete(model)

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        """Convert an ORM model to a domain entity.

        Parameters
        ----------
        model : UserModel
            ORM model instance.

        Returns
        -------
        User
            Domain entity.
        """
        return User(
            id=UserId(model.id),
            username=Username(model.username),
            hashed_password=HashedPassword(model.hashed_password),
        )


__all__ = ("PostgresUserRepository",)
