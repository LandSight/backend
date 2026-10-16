"""PostgreSQL interpretation report repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from sqlalchemy import delete, select

from app.module.interpretation.application.port import InterpretationRepository
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.value_object import (
    AspectExplanation,
    InterpretationId,
    InterpretationStatus,
)
from app.module.interpretation.infrastructure.model import InterpretationModel
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresInterpretationRepository(BaseSQLAlchemyRepository, InterpretationRepository):
    """Interpretation repository backed by PostgreSQL.

    Only the generated text and the model that produced it are stored; scores
    and evaluation metadata are not duplicated and facts are recomputed when the
    report is read.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def get(self, analysis_id: UUID) -> Interpretation | None:
        """See :class:`app.module.interpretation.application.port.InterpretationRepository.get`."""
        result = await self._session.execute(
            select(InterpretationModel).where(InterpretationModel.analysis_id == analysis_id).limit(1),
        )
        model = result.scalars().first()
        return self._to_domain(model) if model is not None else None

    @override
    async def save(self, interpretation: Interpretation) -> Interpretation:
        """See :class:`app.module.interpretation.application.port.InterpretationRepository.save`.

        One row per analysis: the report is inserted on the first save (with the
        ``ordered`` status) and updated in place on every later save, mirroring
        the analysis aggregate lifecycle.
        """
        model = await self._session.get(InterpretationModel, interpretation.id.unwrap())
        if model is None:
            model = InterpretationModel(
                id=interpretation.id.unwrap(),
                analysis_id=interpretation.analysis_id,
                model=interpretation.model,
                summary=interpretation.summary,
                constraints_explanation=interpretation.constraints_explanation,
                status=interpretation.status.value,
                aspect_explanations={explanation.key: explanation.text for explanation in interpretation.explanations},
            )
            self._session.add(model)
        else:
            model.analysis_id = interpretation.analysis_id
            model.model = interpretation.model
            model.summary = interpretation.summary
            model.constraints_explanation = interpretation.constraints_explanation
            model.status = interpretation.status.value
            model.aspect_explanations = {
                explanation.key: explanation.text for explanation in interpretation.explanations
            }

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    @override
    async def delete(self, analysis_id: UUID) -> None:
        """See :class:`app.module.interpretation.application.port.InterpretationRepository.delete`."""
        await self._session.execute(
            delete(InterpretationModel).where(InterpretationModel.analysis_id == analysis_id),
        )
        await self._session.flush()

    @staticmethod
    def _to_domain(model: InterpretationModel) -> Interpretation:
        """Convert an ORM model to a domain entity."""
        return Interpretation(
            id=InterpretationId(model.id),
            analysis_id=model.analysis_id,
            model=model.model,
            summary=model.summary,
            constraints_explanation=model.constraints_explanation,
            status=InterpretationStatus(model.status),
            explanations=tuple(
                AspectExplanation(key=key, text=text) for key, text in model.aspect_explanations.items()
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


__all__ = ("PostgresInterpretationRepository",)
