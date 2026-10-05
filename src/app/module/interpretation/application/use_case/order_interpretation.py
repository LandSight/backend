"""Order interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.analysis.interface.internal.dto import GetAnalysisEvaluationInput
from app.module.interpretation.application.dto.command import GenerateInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.event import INTERPRETATION_ORDERED_EVENT, InterpretationOrderedEvent
from app.module.interpretation.domain.value_object import InterpretationId, InterpretationStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.interface.internal.port import AnalysisInternalAPI
    from app.module.interpretation.application.port import (
        EvaluationBreakdownBuilder,
        InterpretationRepository,
    )
    from app.module.interpretation.domain.value_object import EvaluationBreakdown
    from app.module.shared.application.port import EventPublisher


class OrderInterpretationUseCase(BaseUseCase[GenerateInterpretationCommand, InterpretationResultResponse]):
    """Order the generation of an interpretation report.

    Creates the report row immediately with the ``ordered`` status (or resets an
    existing one) and requests generation by writing an
    ``InterpretationOrdered`` event to the transactional outbox in the same
    transaction, mirroring how analyses are started. The actual LLM generation
    runs in a worker.
    """

    def __init__(
        self,
        analysis_api: AnalysisInternalAPI,
        interpretation_repository: InterpretationRepository,
        breakdown_builder: EvaluationBreakdownBuilder,
        event_publisher: EventPublisher,
    ) -> None:
        self._analysis_api = analysis_api
        self._repository = interpretation_repository
        self._breakdown_builder = breakdown_builder
        self._event_publisher = event_publisher
        self._logger = get_logger("app.interpretation.use_case.order")

    @override
    async def __call__(self, command: GenerateInterpretationCommand) -> InterpretationResultResponse:
        self._logger.info("Ordering interpretation: analysis_id=%s", command.analysis_id)

        breakdown = await self._load_breakdown(command)
        existing = await self._repository.get(command.analysis_id)
        if existing is None:
            interpretation = Interpretation(
                id=InterpretationId(uuid6()),
                analysis_id=command.analysis_id,
                model="",
                summary="",
                status=InterpretationStatus.ORDERED,
            )
        else:
            existing.reset_to_ordered()
            interpretation = existing
        await self._repository.save(interpretation)
        await self._event_publisher.publish(
            INTERPRETATION_ORDERED_EVENT,
            InterpretationOrderedEvent(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            ).to_payload(),
        )
        return InterpretationResultResponse(
            total_score=breakdown.total_score,
            scale_max=breakdown.scale_max,
            scenario=breakdown.scenario,
            status=InterpretationStatus.ORDERED,
        )

    async def _load_breakdown(self, command: GenerateInterpretationCommand) -> EvaluationBreakdown:
        """Read the evaluation through the analysis API and flatten it."""
        evaluation = await self._analysis_api.get_analysis_evaluation(
            GetAnalysisEvaluationInput(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            ),
        )
        return self._breakdown_builder.build(evaluation)


__all__ = ("OrderInterpretationUseCase",)
