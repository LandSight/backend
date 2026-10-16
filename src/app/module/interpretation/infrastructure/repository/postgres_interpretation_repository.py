"""PostgreSQL interpretation report repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast, override

from sqlalchemy import and_, delete, select, update

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

    from sqlalchemy.engine import CursorResult
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
                attempt_id=interpretation.attempt_id,
                progress_done=interpretation.progress_done,
                progress_total=interpretation.progress_total,
                aspect_explanations={explanation.key: explanation.text for explanation in interpretation.explanations},
            )
            self._session.add(model)
        else:
            model.analysis_id = interpretation.analysis_id
            model.model = interpretation.model
            model.summary = interpretation.summary
            model.constraints_explanation = interpretation.constraints_explanation
            model.status = interpretation.status.value
            model.attempt_id = interpretation.attempt_id
            model.progress_done = interpretation.progress_done
            model.progress_total = interpretation.progress_total
            model.aspect_explanations = {
                explanation.key: explanation.text for explanation in interpretation.explanations
            }

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    @override
    async def update_progress(self, analysis_id: UUID, attempt_id: UUID, done: int, total: int) -> bool:
        """See :class:`app.module.interpretation.application.port.InterpretationRepository.update_progress`."""
        return await self._update_owned(analysis_id, attempt_id, {"progress_done": done, "progress_total": total})

    @override
    async def complete_attempt(self, interpretation: Interpretation) -> bool:
        """See :class:`app.module.interpretation.application.port.InterpretationRepository.complete_attempt`."""
        if interpretation.attempt_id is None:
            return False
        return await self._update_owned(
            interpretation.analysis_id,
            interpretation.attempt_id,
            {
                "model": interpretation.model,
                "summary": interpretation.summary,
                "constraints_explanation": interpretation.constraints_explanation,
                "aspect_explanations": {
                    explanation.key: explanation.text for explanation in interpretation.explanations
                },
                "status": InterpretationStatus.COMPLETED.value,
                "progress_done": InterpretationModel.progress_total,
            },
        )

    async def _update_owned(self, analysis_id: UUID, attempt_id: UUID, values: dict[str, object]) -> bool:
        """Update the report only while it is running under ``attempt_id``; return whether it was."""
        result = cast(
            "CursorResult[Any]",
            await self._session.execute(
                update(InterpretationModel)
                .where(
                    and_(
                        InterpretationModel.analysis_id == analysis_id,
                        InterpretationModel.status == InterpretationStatus.RUNNING.value,
                        InterpretationModel.attempt_id == attempt_id,
                    )
                )
                .values(values)
                .execution_options(synchronize_session=False),
            ),
        )
        return result.rowcount > 0

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
            attempt_id=model.attempt_id,
            progress_done=model.progress_done,
            progress_total=model.progress_total,
            explanations=tuple(
                AspectExplanation(key=key, text=text) for key, text in model.aspect_explanations.items()
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


__all__ = ("PostgresInterpretationRepository",)
