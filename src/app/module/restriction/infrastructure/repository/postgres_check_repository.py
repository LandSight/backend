"""PostgreSQL restriction check repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from sqlalchemy import delete, select

from app.module.restriction.application.port import CheckRepository
from app.module.restriction.domain.entity import RestrictionCheck
from app.module.restriction.domain.value_object import (
    LegalBasis,
    ParcelId,
    RestrictionCheckId,
    RestrictionHit,
    RestrictionKind,
    ZoneNames,
)
from app.module.restriction.infrastructure.model import RestrictionCheckHitModel, RestrictionCheckModel
from app.module.shared.domain.value_object import Area, SemanticVersion, Share
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresCheckRepository(BaseSQLAlchemyRepository, CheckRepository):
    """Restriction check repository backed by PostgreSQL.

    Stores checks in ``restriction.checks`` and their hits in
    ``restriction.check_hits``.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, check: RestrictionCheck) -> RestrictionCheck:
        """See :class:`app.module.restriction.application.port.CheckRepository.save`."""
        model = RestrictionCheckModel(
            id=check.id.unwrap(),
            parcel_id=check.parcel_id.unwrap(),
            rules_version=check.rules_version.unwrap(),
        )
        self._session.add(model)
        await self._session.flush()

        hit_models = [
            RestrictionCheckHitModel(
                check_id=model.id,
                position=position,
                kind=hit.kind.value,
                overlap_area_m2=hit.overlap_area.unwrap(),
                overlap_share=hit.overlap_share.unwrap(),
                zone_names=list(hit.zone_names.unwrap()),
                legal_basis=hit.legal_basis.unwrap(),
            )
            for position, hit in enumerate(check.hits)
        ]
        self._session.add_all(hit_models)
        await self._session.flush()

        return self._to_domain(model, hit_models)

    @override
    async def get(self, check_id: RestrictionCheckId) -> RestrictionCheck | None:
        """See :class:`app.module.restriction.application.port.CheckRepository.get`."""
        result = await self._session.execute(
            select(RestrictionCheckModel).where(RestrictionCheckModel.id == check_id.unwrap()),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None

        hits = await self._session.execute(
            select(RestrictionCheckHitModel)
            .where(RestrictionCheckHitModel.check_id == model.id)
            .order_by(RestrictionCheckHitModel.position),
        )
        return self._to_domain(model, list(hits.scalars().all()))

    @override
    async def get_parcel_ids(self, check_ids: list[UUID]) -> dict[UUID, UUID]:
        """See :class:`app.module.restriction.application.port.CheckRepository.get_parcel_ids`."""
        if not check_ids:
            return {}
        result = await self._session.execute(
            select(RestrictionCheckModel.id, RestrictionCheckModel.parcel_id).where(
                RestrictionCheckModel.id.in_(check_ids)
            ),
        )
        return {row.id: row.parcel_id for row in result.all()}

    @override
    async def delete(self, check_ids: list[UUID]) -> None:
        """See :class:`app.module.restriction.application.port.CheckRepository.delete`."""
        if not check_ids:
            return
        await self._session.execute(delete(RestrictionCheckModel).where(RestrictionCheckModel.id.in_(check_ids)))
        await self._session.flush()

    @staticmethod
    def _to_domain(model: RestrictionCheckModel, hits: list[RestrictionCheckHitModel]) -> RestrictionCheck:
        """Convert ORM models to a domain entity."""
        return RestrictionCheck(
            id=RestrictionCheckId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            hits=tuple(
                RestrictionHit(
                    kind=RestrictionKind(hit.kind),
                    overlap_area=Area(hit.overlap_area_m2),
                    overlap_share=Share(hit.overlap_share),
                    zone_names=ZoneNames(tuple(hit.zone_names)),
                    legal_basis=LegalBasis(hit.legal_basis),
                )
                for hit in hits
            ),
            rules_version=SemanticVersion(model.rules_version),
            created_at=model.created_at,
        )


__all__ = ("PostgresCheckRepository",)
