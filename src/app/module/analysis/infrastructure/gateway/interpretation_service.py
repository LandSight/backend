"""Interpretation gateway backed by the Interpretation module's Internal API."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import InterpretationService
from app.module.interpretation.interface.internal.dto import GenerateInterpretationInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.interface.internal.port import InterpretationInternalAPI


class InterpretationServiceImpl(InterpretationService):
    """Starts report generation through the Interpretation module's Internal API."""

    def __init__(self, interpretation_api: InterpretationInternalAPI) -> None:
        self._interpretation_api = interpretation_api

    @override
    async def start(self, analysis_id: UUID, current_user_id: UUID) -> None:
        """See :class:`app.module.analysis.application.port.InterpretationService.start`."""
        await self._interpretation_api.start_interpretation(
            GenerateInterpretationInput(
                analysis_id=analysis_id,
                current_user_id=current_user_id,
            ),
        )


__all__ = ("InterpretationServiceImpl",)
