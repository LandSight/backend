"""Concrete implementation of the Interpretation module's internal API.

See :class:`app.module.interpretation.interface.internal.port.InterpretationInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.interpretation.application.dto.command import (
    GenerateInterpretationCommand,
    GetInterpretationCommand,
)
from app.module.interpretation.interface.internal.dto import (
    AspectInterpretationResult,
    ConstraintInterpretationResult,
    GenerateInterpretationInput,
    GetInterpretationInput,
    InterpretationResult,
    MetricInfoResult,
)
from app.module.interpretation.interface.internal.port import InterpretationInternalAPI


if TYPE_CHECKING:
    from app.module.interpretation.application.dto.response import (
        AspectInterpretationResponse,
        InterpretationResultResponse,
    )
    from app.module.interpretation.application.use_case import (
        GetInterpretationUseCase,
        StartInterpretationUseCase,
    )
    from app.module.interpretation.domain.value_object import AspectMetric


class InterpretationInternal(InterpretationInternalAPI):
    """Concrete implementation of the Interpretation internal API."""

    def __init__(
        self,
        get_interpretation_use_case: GetInterpretationUseCase,
        start_interpretation_use_case: StartInterpretationUseCase,
    ) -> None:
        self._get_interpretation = get_interpretation_use_case
        self._start_interpretation = start_interpretation_use_case

    @override
    async def get_interpretation(self, input_data: GetInterpretationInput) -> InterpretationResult:
        """See :meth:`InterpretationInternalAPI.get_interpretation`."""
        result = await self._get_interpretation(
            GetInterpretationCommand(
                analysis_id=input_data.analysis_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def start_interpretation(self, input_data: GenerateInterpretationInput) -> InterpretationResult:
        """See :meth:`InterpretationInternalAPI.start_interpretation`."""
        result = await self._start_interpretation(
            GenerateInterpretationCommand(
                analysis_id=input_data.analysis_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @classmethod
    def _to_result(cls, result: InterpretationResultResponse) -> InterpretationResult:
        """Map an application response DTO to an internal result DTO."""
        return InterpretationResult(
            total_score=result.total_score,
            scale_max=result.scale_max,
            scenario=result.scenario,
            status=result.status,
            aspects=tuple(cls._to_aspect(aspect) for aspect in result.aspects),
            top_aspects_summary=result.top_aspects_summary,
            verdict=result.verdict,
            base_score=result.base_score,
            constraints_loss=result.constraints_loss,
            constraints_explanation=result.constraints_explanation,
            constraints=tuple(
                ConstraintInterpretationResult(
                    kind=constraint.kind,
                    label=constraint.label,
                    effect=constraint.effect,
                    factor=constraint.factor,
                    overlap_share=constraint.overlap_share,
                    zone_names=constraint.zone_names,
                    legal_basis=constraint.legal_basis,
                    score_reduction=constraint.score_reduction,
                    points_lost=constraint.points_lost,
                )
                for constraint in result.constraints
            ),
        )

    @classmethod
    def _to_aspect(cls, aspect: AspectInterpretationResponse) -> AspectInterpretationResult:
        """Map one aspect explanation."""
        return AspectInterpretationResult(
            key=aspect.key,
            name=aspect.name,
            score=aspect.score,
            weight=aspect.weight,
            contribution=aspect.contribution,
            points=aspect.points,
            max_points=aspect.max_points,
            loss=aspect.loss,
            loss_share=aspect.loss_share,
            explanation=aspect.explanation,
            top_metrics=tuple(cls._to_metric(metric) for metric in aspect.top_metrics),
            metrics=tuple(cls._to_metric(metric) for metric in aspect.metrics),
        )

    @staticmethod
    def _to_metric(metric: AspectMetric) -> MetricInfoResult:
        """Map one aspect metric."""
        return MetricInfoResult(
            key=metric.key,
            label=metric.label,
            raw_value=metric.raw_value,
            normalized_value=metric.normalized_value,
            contribution=metric.contribution,
            unit=metric.unit,
            role=metric.role,
            position=metric.position,
            membership_function=metric.membership.function if metric.membership else None,
            membership_params=metric.membership.params if metric.membership else None,
        )


__all__ = ("InterpretationInternal",)
