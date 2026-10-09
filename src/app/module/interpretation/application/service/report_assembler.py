"""Report assembler application service.

Rebuilds the public report from the current evaluation and the stored
generated text. Scores, weights, metrics and evaluation metadata are
recomputed from the evaluation, so the stored entity stays a plain text and the
response contract can change without a data migration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.application.dto.response import (
    AspectInterpretationResponse,
    InterpretationResultResponse,
)


if TYPE_CHECKING:
    from app.module.interpretation.domain.entity import Interpretation
    from app.module.interpretation.domain.service import AspectExtractor
    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class ReportAssembler:
    """Assembles the interpretation response from evaluation facts and stored text."""

    def __init__(self, aspect_extractor: AspectExtractor) -> None:
        self._aspect_extractor = aspect_extractor

    def assemble(
        self,
        breakdown: EvaluationBreakdown,
        interpretation: Interpretation,
    ) -> InterpretationResultResponse:
        """Build the report response for a stored interpretation."""
        aspects = tuple(
            AspectInterpretationResponse(
                key=aspect.key,
                name=aspect.name,
                score=aspect.score,
                weight=aspect.weight,
                contribution=aspect.contribution,
                points=aspect.points,
                max_points=aspect.max_points,
                loss=aspect.loss,
                loss_share=aspect.loss_share,
                explanation=interpretation.explanation_for(aspect.key),
                top_metrics=self._aspect_extractor.top_metrics(aspect),
                metrics=self._aspect_extractor.all_metrics(aspect),
            )
            for aspect in breakdown.aspects
        )
        return InterpretationResultResponse(
            total_score=breakdown.total_score,
            scale_max=breakdown.scale_max,
            scenario=breakdown.scenario,
            status=interpretation.status,
            aspects=aspects,
            top_aspects_summary=interpretation.summary,
            verdict=breakdown.verdict,
        )


__all__ = ("ReportAssembler",)
