"""Dependency injection for the Interpretation module.

Wires the domain rule-based services, the LLM infrastructure and the public
use cases. The module talks to the Analysis module only through the
:class:`AnalysisInternalAPI` port.
"""

from __future__ import annotations

from celery import Celery
from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.analysis.interface.internal.port import AnalysisInternalAPI
from app.module.interpretation.application.service import ReportAssembler
from app.module.interpretation.application.use_case import (
    GenerateInterpretationUseCase,
    GetInterpretationUseCase,
)
from app.module.interpretation.domain.service import AspectExtractor, MetricClassifier, TopAspectSelector
from app.module.interpretation.domain.value_object import InterpretationPolicy
from app.module.interpretation.infrastructure.breakdown import AnalysisEvaluationBreakdownBuilder
from app.module.interpretation.infrastructure.llm import (
    LlmGrader,
    LlmInterpreter,
    LlmPromptBuilder,
    OpenAICompatibleLLMClient,
)
from app.module.interpretation.infrastructure.queue import CeleryInterpretationTaskQueue
from app.module.interpretation.infrastructure.repository import PostgresInterpretationRepository
from app.platform.config.loaders import load_llm_config


GENERATE_INTERPRETATION_USE_CASE_KEY = "generate_interpretation_use_case"
GET_INTERPRETATION_USE_CASE_KEY = "get_interpretation_use_case"


# ----- Domain services -----
def provide_interpretation_policy() -> InterpretationPolicy:
    return InterpretationPolicy()


def provide_metric_classifier(
    interpretation_policy: NamedDependency[InterpretationPolicy],
) -> MetricClassifier:
    return MetricClassifier(interpretation_policy)


def provide_aspect_extractor(
    interpretation_policy: NamedDependency[InterpretationPolicy],
) -> AspectExtractor:
    return AspectExtractor(interpretation_policy)


def provide_top_aspect_selector(
    interpretation_policy: NamedDependency[InterpretationPolicy],
) -> TopAspectSelector:
    return TopAspectSelector(interpretation_policy)


# ----- LLM infrastructure -----
def provide_prompt_builder() -> LlmPromptBuilder:
    return LlmPromptBuilder()


def provide_llm_client() -> OpenAICompatibleLLMClient:
    return OpenAICompatibleLLMClient(load_llm_config())


def provide_grader(
    llm_client: NamedDependency[OpenAICompatibleLLMClient],
    prompt_builder: NamedDependency[LlmPromptBuilder],
) -> LlmGrader:
    return LlmGrader(llm_client, prompt_builder)


def provide_interpreter(
    llm_client: NamedDependency[OpenAICompatibleLLMClient],
    prompt_builder: NamedDependency[LlmPromptBuilder],
    grader: NamedDependency[LlmGrader],
    aspect_extractor: NamedDependency[AspectExtractor],
    top_aspect_selector: NamedDependency[TopAspectSelector],
) -> LlmInterpreter:
    return LlmInterpreter(
        llm_client,
        prompt_builder,
        grader,
        aspect_extractor,
        top_aspect_selector,
        model=load_llm_config().model,
    )


def provide_report_assembler(
    aspect_extractor: NamedDependency[AspectExtractor],
) -> ReportAssembler:
    return ReportAssembler(aspect_extractor)


def provide_evaluation_breakdown_builder(
    metric_classifier: NamedDependency[MetricClassifier],
) -> AnalysisEvaluationBreakdownBuilder:
    return AnalysisEvaluationBreakdownBuilder(metric_classifier)


def provide_interpretation_task_queue(
    celery_app: NamedDependency[Celery],
) -> CeleryInterpretationTaskQueue:
    return CeleryInterpretationTaskQueue(celery_app)


# ----- Repository -----
def provide_interpretation_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresInterpretationRepository:
    return PostgresInterpretationRepository(session)


# ----- Use cases -----
def provide_generate_interpretation_use_case(
    analysis_api: NamedDependency[AnalysisInternalAPI],
    interpretation_repository: NamedDependency[PostgresInterpretationRepository],
    evaluation_breakdown_builder: NamedDependency[AnalysisEvaluationBreakdownBuilder],
    interpreter: NamedDependency[LlmInterpreter],
    report_assembler: NamedDependency[ReportAssembler],
) -> GenerateInterpretationUseCase:
    return GenerateInterpretationUseCase(
        analysis_api,
        interpretation_repository,
        evaluation_breakdown_builder,
        interpreter,
        report_assembler,
    )


def provide_get_interpretation_use_case(
    analysis_api: NamedDependency[AnalysisInternalAPI],
    interpretation_repository: NamedDependency[PostgresInterpretationRepository],
    evaluation_breakdown_builder: NamedDependency[AnalysisEvaluationBreakdownBuilder],
    report_assembler: NamedDependency[ReportAssembler],
) -> GetInterpretationUseCase:
    return GetInterpretationUseCase(
        analysis_api,
        interpretation_repository,
        evaluation_breakdown_builder,
        report_assembler,
    )


interpretation_dependencies = {
    "interpretation_policy": Provide(provide_interpretation_policy, use_cache=True, sync_to_thread=False),
    "metric_classifier": Provide(provide_metric_classifier, use_cache=True, sync_to_thread=False),
    "aspect_extractor": Provide(provide_aspect_extractor, use_cache=True, sync_to_thread=False),
    "top_aspect_selector": Provide(provide_top_aspect_selector, use_cache=True, sync_to_thread=False),
    "prompt_builder": Provide(provide_prompt_builder, use_cache=True, sync_to_thread=False),
    "llm_client": Provide(provide_llm_client, use_cache=True, sync_to_thread=False),
    "grader": Provide(provide_grader, use_cache=True, sync_to_thread=False),
    "interpreter": Provide(provide_interpreter, use_cache=True, sync_to_thread=False),
    "report_assembler": Provide(provide_report_assembler, use_cache=True, sync_to_thread=False),
    "evaluation_breakdown_builder": Provide(
        provide_evaluation_breakdown_builder,
        use_cache=True,
        sync_to_thread=False,
    ),
    "interpretation_task_queue": Provide(provide_interpretation_task_queue, use_cache=True, sync_to_thread=False),
    "interpretation_repository": Provide(provide_interpretation_repository, sync_to_thread=False),
    GENERATE_INTERPRETATION_USE_CASE_KEY: Provide(
        provide_generate_interpretation_use_case,
        sync_to_thread=False,
    ),
    GET_INTERPRETATION_USE_CASE_KEY: Provide(provide_get_interpretation_use_case, sync_to_thread=False),
}


__all__ = (
    "GENERATE_INTERPRETATION_USE_CASE_KEY",
    "GET_INTERPRETATION_USE_CASE_KEY",
    "interpretation_dependencies",
)
