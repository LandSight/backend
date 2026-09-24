"""Analysis entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, override

from app.module.analysis.domain.value_object import (
    AnalysisId,
    AnalysisName,
    AnalysisScore,
    AnalysisStage,
    AnalysisStatus,
    ParcelId,
)
from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import InvariantViolationError


if TYPE_CHECKING:
    import datetime


class Analysis(BaseEntity[AnalysisId]):
    """Parcel analysis aggregate root.

    Attributes
    ----------
    id : AnalysisId
        Unique identifier for the analysis.
    parcel_id : ParcelId
        ID of the parcel being analysed.
    name : AnalysisName
        Human-readable name of the analysis.
    status : AnalysisStatus
        Current lifecycle status.
    stage : AnalysisStage
        Pipeline stage (metrics calculation or scoring).
    score : AnalysisScore | None
        Final score, set only when the analysis is completed.
    status_reason : str | None
        Human-readable explanation (e.g. failure reason).
    created_at : datetime | None
        When the analysis was created (UTC); ``None`` if not yet persisted.
    """

    def __init__(
        self,
        id: AnalysisId,
        parcel_id: ParcelId,
        *,
        name: AnalysisName,
        status: AnalysisStatus = AnalysisStatus.PENDING,
        stage: AnalysisStage = AnalysisStage.METRICS,
        score: AnalysisScore | None = None,
        status_reason: str | None = None,
        created_at: datetime.datetime | None = None,
    ) -> None:
        self._parcel_id: ParcelId = parcel_id
        self._name: AnalysisName = name
        self._status: AnalysisStatus = status
        self._stage: AnalysisStage = stage
        self._score: AnalysisScore | None = score
        self._status_reason: str | None = status_reason
        self._created_at: datetime.datetime | None = created_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        if self._status is AnalysisStatus.COMPLETED and self._score is None:
            message = "A completed analysis must carry a score."
            raise InvariantViolationError(message)
        if self._status is not AnalysisStatus.COMPLETED and self._score is not None:
            message = "Only a completed analysis may carry a score."
            raise InvariantViolationError(message)
        if self._status is AnalysisStatus.COMPLETED and self._stage is not AnalysisStage.SCORING:
            message = "A completed analysis must have finished the scoring stage."
            raise InvariantViolationError(message)
        if self._status is AnalysisStatus.FAILED and not self._status_reason:
            message = "A failed analysis must carry a status reason."
            raise InvariantViolationError(message)

    def mark_running(self) -> None:
        """Transition the analysis to ``RUNNING``."""
        if self._status is not AnalysisStatus.PENDING:
            self._raise_invalid_transition(AnalysisStatus.PENDING)
        self._status = AnalysisStatus.RUNNING
        self._status_reason = None

    def mark_metrics_calculated(self) -> None:
        """Transition the pipeline stage to ``SCORING`` once metrics are ready."""
        if self._status is not AnalysisStatus.RUNNING:
            self._raise_invalid_transition(AnalysisStatus.RUNNING)
        if self._stage is not AnalysisStage.METRICS:
            message = "Metrics have already been calculated."
            raise InvariantViolationError(message)
        self._stage = AnalysisStage.SCORING

    def complete(self, score: AnalysisScore, reason: str | None = None) -> None:
        """Transition the analysis to ``COMPLETED`` with its final score."""
        if self._status is not AnalysisStatus.RUNNING:
            self._raise_invalid_transition(AnalysisStatus.RUNNING)
        if self._stage is not AnalysisStage.SCORING:
            message = "Cannot complete an analysis before its metrics are calculated."
            raise InvariantViolationError(message)
        self._score = score
        self._status_reason = reason
        self._status = AnalysisStatus.COMPLETED

    def fail(self, reason: str) -> None:
        """Transition the analysis to ``FAILED`` with an explanation."""
        if self._status not in {AnalysisStatus.PENDING, AnalysisStatus.RUNNING}:
            self._raise_invalid_transition(AnalysisStatus.RUNNING)
        self._status = AnalysisStatus.FAILED
        self._status_reason = reason

    def _raise_invalid_transition(self, expected: AnalysisStatus) -> NoReturn:
        message = f"Analysis must be in '{expected}' status to perform this transition, got '{self._status}'."
        raise InvariantViolationError(message)

    @property
    def parcel_id(self) -> ParcelId:
        """ID of the parcel being analysed."""
        return self._parcel_id

    @property
    def name(self) -> AnalysisName:
        """Human-readable name of the analysis."""
        return self._name

    @property
    def status(self) -> AnalysisStatus:
        """Current lifecycle status."""
        return self._status

    @property
    def stage(self) -> AnalysisStage:
        """Current pipeline stage."""
        return self._stage

    @property
    def score(self) -> AnalysisScore | None:
        """Final score, set only when completed."""
        return self._score

    @property
    def status_reason(self) -> str | None:
        """Human-readable status explanation."""
        return self._status_reason

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the analysis was created (UTC)."""
        return self._created_at


__all__ = ("Analysis",)
