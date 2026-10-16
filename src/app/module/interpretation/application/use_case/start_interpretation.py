"""Start interpretation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.interpretation.application.dto.command import GenerateInterpretationCommand
from app.module.interpretation.application.dto.response import InterpretationResultResponse
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.event import INTERPRETATION_STARTED_EVENT, InterpretationStartedEvent
from app.module.interpretation.domain.value_object import InterpretationId, InterpretationStatus
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.interpretation.application.port import InterpretationRepository
    from app.module.shared.application.port import EventPublisher


class StartInterpretationUseCase(BaseUseCase[GenerateInterpretationCommand, InterpretationResultResponse]):
    """Start the generation of an interpretation report.

    Creates the report row immediately with the ``ordered`` status (or resets an
    existing one) and requests generation by writing an
    ``InterpretationStarted`` event to the transactional outbox in the same
    transaction, mirroring how analyses are started. The actual LLM generation
    runs in a worker.
    """

    def __init__(
        self,
        interpretation_repository: InterpretationRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._repository = interpretation_repository
        self._event_publisher = event_publisher
        self._logger = get_logger("app.interpretation.use_case.start")

    @override
    async def __call__(self, command: GenerateInterpretationCommand) -> InterpretationResultResponse:
        self._logger.info("Starting interpretation: analysis_id=%s", command.analysis_id)

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
            INTERPRETATION_STARTED_EVENT,
            InterpretationStartedEvent(
                analysis_id=command.analysis_id,
                current_user_id=command.current_user_id,
            ).to_payload(),
        )

        return InterpretationResultResponse(status=InterpretationStatus.ORDERED)


__all__ = ("StartInterpretationUseCase",)
