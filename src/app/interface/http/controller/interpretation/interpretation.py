"""Interpretation HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_202_ACCEPTED

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.interpretation import (
    AspectInterpretationSchema,
    ConstraintInterpretationSchema,
    InterpretationResultSchema,
    MetricInfoSchema,
)
from app.interface.http.util.guards import require_authorization
from app.module.interpretation.interface.internal.dto import (
    AspectInterpretationResult,
    CancelInterpretationInput,
    GenerateInterpretationInput,
    GetInterpretationInput,
    InterpretationResult,
    MetricInfoResult,
)
from app.module.interpretation.interface.internal.port import InterpretationInternalAPI


class InterpretationController(Controller):
    """Endpoints for reading and regenerating interpretation reports."""

    path = "/"
    tags = ("interpretation",)
    guards = [require_authorization]

    @get(
        "/{analysis_id:uuid}/interpretation",
        status_code=HTTP_200_OK,
        description="Get the interpretation report of an analysis.",
    )
    async def get_interpretation(
        self,
        analysis_id: UUID,
        current_user: CurrentUser,
        interpretation_api: InterpretationInternalAPI,
    ) -> InterpretationResultSchema:
        """Return the stored interpretation report of an analysis."""
        result = await interpretation_api.get_interpretation(
            GetInterpretationInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @post(
        "/{analysis_id:uuid}/interpretation",
        status_code=HTTP_202_ACCEPTED,
        description="Start (re)generation of the interpretation report of an analysis.",
    )
    async def start_interpretation(
        self,
        analysis_id: UUID,
        current_user: CurrentUser,
        interpretation_api: InterpretationInternalAPI,
    ) -> InterpretationResultSchema:
        """Start (re)generation of the interpretation report.

        The report row is created with the ``ordered`` status and generation is
        requested through the transactional outbox; the actual LLM work runs in
        the worker. Poll ``GET /{analysis_id}/interpretation`` for the status.
        """
        result = await interpretation_api.start_interpretation(
            GenerateInterpretationInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @post(
        "/{analysis_id:uuid}/interpretation/cancel",
        status_code=HTTP_200_OK,
        description="Cancel the generation of the interpretation report of an analysis.",
    )
    async def cancel_interpretation(
        self,
        analysis_id: UUID,
        current_user: CurrentUser,
        interpretation_api: InterpretationInternalAPI,
    ) -> InterpretationResultSchema:
        """Cancel an ordered or running report.

        The report is marked ``cancelled`` at once; the worker stops at its next
        step and discards its result. A finished report is returned as is.
        """
        result = await interpretation_api.cancel_interpretation(
            CancelInterpretationInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @classmethod
    def _to_schema(cls, result: InterpretationResult) -> InterpretationResultSchema:
        """Map an internal result DTO to the HTTP schema."""
        return InterpretationResultSchema(
            total_score=result.total_score,
            scale_max=result.scale_max,
            scenario=result.scenario,
            status=result.status,
            progress_done=result.progress_done,
            progress_total=result.progress_total,
            aspects=[cls._to_aspect_schema(aspect) for aspect in result.aspects],
            top_aspects_summary=result.top_aspects_summary,
            verdict=result.verdict.value if result.verdict else None,
            verdict_label=result.verdict.label if result.verdict else None,
            base_score=result.base_score,
            constraints_loss=result.constraints_loss,
            constraints_explanation=result.constraints_explanation,
            constraints=[
                ConstraintInterpretationSchema(
                    kind=constraint.kind,
                    label=constraint.label,
                    effect=constraint.effect,
                    factor=constraint.factor,
                    overlap_share=constraint.overlap_share,
                    zone_names=list(constraint.zone_names),
                    legal_basis=constraint.legal_basis,
                    score_reduction=constraint.score_reduction,
                    points_lost=constraint.points_lost,
                )
                for constraint in result.constraints
            ],
        )

    @classmethod
    def _to_aspect_schema(cls, aspect: AspectInterpretationResult) -> AspectInterpretationSchema:
        return AspectInterpretationSchema(
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
            top_metrics=[cls._to_metric_schema(metric) for metric in aspect.top_metrics],
            metrics=[cls._to_metric_schema(metric) for metric in aspect.metrics],
        )

    @staticmethod
    def _to_metric_schema(metric: MetricInfoResult) -> MetricInfoSchema:
        return MetricInfoSchema(
            key=metric.key,
            label=metric.label,
            raw_value=metric.raw_value,
            normalized_value=metric.normalized_value,
            contribution=metric.contribution,
            unit=metric.unit,
            role=metric.role.value,
            position=metric.position.value,
            membership_function=metric.membership_function,
            membership_params=dict(metric.membership_params) if metric.membership_params is not None else None,
        )


__all__ = ("InterpretationController",)
