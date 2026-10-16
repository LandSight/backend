"""Interpretation report entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, override

from app.module.interpretation.domain.value_object import (
    AspectExplanation,
    InterpretationId,
    InterpretationStatus,
)
from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


class Interpretation(BaseEntity[InterpretationId]):
    """Generated interpretation report of one analysis.

    The aggregate stores only the generated text and the model that produced it:
    the combined summary, the per-aspect explanations and the explanation of the
    restriction zones. Scores, weights and
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
    constraints_explanation : str
        Explanation of the restriction zones that barred the scenario or
        lowered the score; empty when no zone applied.
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
        constraints_explanation: str = "",
        status: InterpretationStatus = InterpretationStatus.COMPLETED,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self._analysis_id: UUID = analysis_id
        self._model: str = model
        self._summary: str = summary
        self._explanations: tuple[AspectExplanation, ...] = explanations
        self._constraints_explanation: str = constraints_explanation
        self._status: InterpretationStatus = status
        self._created_at: datetime.datetime | None = created_at
        self._updated_at: datetime.datetime | None = updated_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        # A report that is not yet completed may be a placeholder row created at
        # ordering time; only a completed report must carry the generated text.
        if self._status == InterpretationStatus.COMPLETED:
            if not self._model:
                message = "A completed interpretation must carry a model."
                raise InvariantViolationError(message)
            if not self._summary:
                message = "A completed interpretation must carry a summary."
                raise InvariantViolationError(message)

    def mark_running(self) -> None:
        """Transition the report to ``RUNNING``."""
        if self._status is not InterpretationStatus.ORDERED:
            self._raise_invalid_transition(InterpretationStatus.ORDERED)
        self._status = InterpretationStatus.RUNNING

    def complete(self) -> None:
        """Transition the report to ``COMPLETED``.

        Callers must fill the generated text (model/summary/explanations) before
        saving so the validation of a completed report passes.
        """
        if self._status is not InterpretationStatus.RUNNING:
            self._raise_invalid_transition(InterpretationStatus.RUNNING)
        self._status = InterpretationStatus.COMPLETED

    def fail(self) -> None:
        """Transition the report to ``FAILED``."""
        if self._status not in {InterpretationStatus.ORDERED, InterpretationStatus.RUNNING}:
            self._raise_invalid_transition(InterpretationStatus.RUNNING)
        self._status = InterpretationStatus.FAILED

    def reset_to_ordered(self) -> None:
        """Reset a stored report for regeneration: clear the text, mark ordered."""
        self._status = InterpretationStatus.ORDERED
        self._model = ""
        self._summary = ""
        self._explanations = ()
        self._constraints_explanation = ""

    def _raise_invalid_transition(self, expected: InterpretationStatus) -> NoReturn:
        message = (
            f"Interpretation must be in '{expected.value}' status to perform this transition, "
            f"got '{self._status.value}'."
        )
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
    def constraints_explanation(self) -> str:
        """Explanation of the restriction zones."""
        return self._constraints_explanation

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the report was stored (UTC)."""
        return self._created_at

    @property
    def updated_at(self) -> datetime.datetime | None:
        """When the report was last updated (UTC)."""
        return self._updated_at

    @property
    def status(self) -> InterpretationStatus:
        """Generation status of the report."""
        return self._status

    def explanation_for(self, aspect_key: str) -> str:
        """Return the explanation text of an aspect, or an empty string."""
        for explanation in self._explanations:
            if explanation.key == aspect_key:
                return explanation.text
        return ""


__all__ = ("Interpretation",)
