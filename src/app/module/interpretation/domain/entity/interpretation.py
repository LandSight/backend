"""Interpretation report entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.interpretation.domain.value_object import AspectExplanation, InterpretationId
from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


class Interpretation(BaseEntity[InterpretationId]):
    """Generated interpretation report of one analysis.

    The aggregate stores only the generated text and the model that produced it:
    the combined summary and the per-aspect explanations. Scores, weights and
    evaluation metadata are recomputed from the current evaluation when the
    report is read.

    Attributes
    ----------
    id : InterpretationId
        Unique identifier for the report.
    analysis_id : UUID
        Analysis the report belongs to.
    model : str
        Identifier of the model that generated the report (an LLM name or a
        template name).
    summary : str
        Combined top-aspects summary text.
    explanations : tuple[AspectExplanation, ...]
        Per-aspect explanation texts.
    created_at : datetime.datetime | None
        When the report was stored (UTC); ``None`` if not yet persisted.
    updated_at : datetime.datetime | None
        When the report was last updated (UTC); ``None`` if not yet persisted.
    """

    def __init__(
        self,
        id: InterpretationId,
        analysis_id: UUID,
        *,
        model: str,
        summary: str,
        explanations: tuple[AspectExplanation, ...] = (),
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self._analysis_id: UUID = analysis_id
        self._model: str = model
        self._summary: str = summary
        self._explanations: tuple[AspectExplanation, ...] = explanations
        self._created_at: datetime.datetime | None = created_at
        self._updated_at: datetime.datetime | None = updated_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        if not self._model:
            message = "An interpretation must carry a model."
            raise InvariantViolationError(message)
        if not self._summary:
            message = "An interpretation must carry a summary."
            raise InvariantViolationError(message)

    @property
    def analysis_id(self) -> UUID:
        """Analysis the report belongs to."""
        return self._analysis_id

    @property
    def model(self) -> str:
        """Model that generated the report."""
        return self._model

    @property
    def summary(self) -> str:
        """Combined top-aspects summary text."""
        return self._summary

    @property
    def explanations(self) -> tuple[AspectExplanation, ...]:
        """Per-aspect explanation texts."""
        return self._explanations

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the report was stored (UTC)."""
        return self._created_at

    @property
    def updated_at(self) -> datetime.datetime | None:
        """When the report was last updated (UTC)."""
        return self._updated_at

    def explanation_for(self, aspect_key: str) -> str:
        """Return the explanation text of an aspect, or an empty string."""
        for explanation in self._explanations:
            if explanation.key == aspect_key:
                return explanation.text
        return ""


__all__ = ("Interpretation",)
