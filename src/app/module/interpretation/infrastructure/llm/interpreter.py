"""LLM-backed interpreter.

Generates the report text aspect by aspect, then the combined summary and the
explanation of the restriction zones: a draft is verified by the grader
and, on rejection, regenerated once with the grader's remarks; any failure
degrades to safe fallback text so a report is always produced.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final, override
from uuid import uuid6

from app.module.interpretation.application.error import InterpretationGenerationError
from app.module.interpretation.application.port import Interpreter
from app.module.interpretation.domain.entity import Interpretation
from app.module.interpretation.domain.value_object import (
    AspectExplanation,
    GradeVerdict,
    InterpretationId,
)
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.service import AspectExtractor, ConstraintExtractor, TopAspectSelector
    from app.module.interpretation.domain.value_object import Aspect, EvaluationBreakdown, Prompt
    from app.module.interpretation.infrastructure.llm.grader import LlmGrader
    from app.module.interpretation.infrastructure.llm.llm_client import LLMClient
    from app.module.interpretation.infrastructure.llm.prompt_builder import LlmPromptBuilder


class LlmInterpreter(Interpreter):
    """Generates the interpretation report with a local LLM."""

    _WRAPPING_QUOTES: Final = "\"'«»"
    # Section labels the model sometimes copies from the prompt structure; they
    # are dropped at the start of the text or of a sentence.
    _SECTION_LABEL: Final = re.compile(r"(?:^|(?<=[.!?] ))(?:Aspect|Summary|Explanation|Answer)\s*:\s*")

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_builder: LlmPromptBuilder,
        grader: LlmGrader,
        aspect_extractor: AspectExtractor,
        top_aspect_selector: TopAspectSelector,
        constraint_extractor: ConstraintExtractor,
        model: str,
    ) -> None:
        self._llm_client = llm_client
        self._prompt_builder = prompt_builder
        self._grader = grader
        self._aspect_extractor = aspect_extractor
        self._top_aspect_selector = top_aspect_selector
        self._constraint_extractor = constraint_extractor
        self._model = model
        self._logger = get_logger("app.interpretation.interpreter")

    @override
    async def explain(self, analysis_id: UUID, breakdown: EvaluationBreakdown) -> Interpretation:
        """See :class:`app.module.interpretation.application.port.Interpreter.explain`."""
        self._logger.info("Interpreting evaluation: analysis_id=%s scenario=%s", analysis_id, breakdown.scenario)

        explanations = {aspect.key: await self._explain(aspect) for aspect in breakdown.aspects}
        top_aspects = self._top_aspect_selector.top_aspects(breakdown.aspects)
        summary = await self._summarize(breakdown, top_aspects, explanations)
        constraints_explanation = await self._explain_constraints(breakdown)
        return Interpretation(
            id=InterpretationId(uuid6()),
            analysis_id=analysis_id,
            model=self._model,
            summary=summary,
            explanations=tuple(AspectExplanation(key=key, text=text) for key, text in explanations.items()),
            constraints_explanation=constraints_explanation,
        )

    async def _explain(self, aspect: Aspect) -> str:
        """Generate one aspect explanation, falling back to a safe text."""
        metrics = self._aspect_extractor.top_metrics(aspect)
        fallback = self.aspect_fallback(aspect.name or aspect.key)
        if not metrics:
            return fallback

        facts = self._prompt_builder.aspect_facts(aspect, metrics)
        return await self._generate(self._prompt_builder.aspect_prompt(aspect, metrics), facts, fallback)

    async def _summarize(
        self,
        breakdown: EvaluationBreakdown,
        top_aspects: tuple[Aspect, ...],
        explanations: dict[str, str],
    ) -> str:
        """Generate the combined top-aspects summary."""
        facts = self._prompt_builder.summary_facts(breakdown, top_aspects, explanations)
        prompt = self._prompt_builder.summary_prompt(breakdown, top_aspects, explanations)
        return await self._generate(prompt, facts, self.summary_fallback(breakdown))

    async def _explain_constraints(self, breakdown: EvaluationBreakdown) -> str:
        """Generate the restrictions explanation; empty when no zone applied."""
        constraints = self._constraint_extractor.top_constraints(breakdown)
        if not constraints:
            return ""
        facts = self._prompt_builder.constraints_facts(breakdown, constraints)
        prompt = self._prompt_builder.constraints_prompt(breakdown, constraints)
        return await self._generate(prompt, facts, self.constraints_fallback(breakdown))

    async def _generate(self, prompt: Prompt, facts: str, fallback: str) -> str:
        """Generate one text and verify it, regenerating once with the grader's remarks.

        The grader only reviews; the text is always written by the generator.
        When the regenerated text is still rejected it is kept anyway (the
        remarks are logged): a small grader also rejects correct texts, so
        discarding the answer would lose more than it protects.
        """
        draft = await self._complete(prompt)
        if draft is None:
            return fallback
        verdict = await self._grade(facts, draft)
        if verdict.ok:
            return draft

        retry = await self._complete(self._prompt_builder.retry_prompt(prompt, draft, verdict.issues))
        if retry is None:
            return draft
        final = await self._grade(facts, retry)
        if not final.ok:
            self._logger.warning("Explanation still rejected after the retry: issues=%s", final.issues)
        return retry

    async def _complete(self, prompt: Prompt) -> str | None:
        """Call the model and clean the answer, returning ``None`` on failure."""
        try:
            completion = await self._llm_client.complete(prompt)
        except InterpretationGenerationError as error:
            self._logger.warning("LLM completion failed: %s", error)
            return None
        return self._clean(completion.unwrap())

    async def _grade(self, facts: str, explanation: str) -> GradeVerdict:
        """Grade an explanation, accepting it when the grader itself fails."""
        try:
            return await self._grader.grade(facts, explanation)
        except InterpretationGenerationError as error:
            self._logger.warning("Grader failed, accepting the draft: %s", error)
            return GradeVerdict(ok=True, issues=("grader_error",))

    @classmethod
    def _clean(cls, text: str) -> str | None:
        """Collapse whitespace, strip wrapping quotes and section labels; ``None`` when empty."""
        cleaned = " ".join(text.split()).strip(cls._WRAPPING_QUOTES).strip()
        cleaned = cls._SECTION_LABEL.sub("", cleaned).strip()
        return cleaned or None

    @staticmethod
    def aspect_fallback(name: str) -> str:
        """Safe text used when an aspect explanation cannot be generated."""
        return f'Could not generate an explanation for the "{name}" aspect.'

    @staticmethod
    def summary_fallback(breakdown: EvaluationBreakdown | None = None) -> str:
        """Safe text used when the combined summary cannot be generated.

        A prohibition is a fact that must reach the reader even without the
        model, so it is stated from the data.
        """
        text = "Could not generate the summary explanation."
        if breakdown is not None and breakdown.prohibited:
            zones = ", ".join(constraint.label for constraint in breakdown.constraints if constraint.prohibits)
            text = f"The parcel is unsuitable: building is barred by a restriction zone ({zones}). {text}"
        return text

    @staticmethod
    def constraints_fallback(breakdown: EvaluationBreakdown) -> str:
        """Safe text used when the restrictions explanation cannot be generated.

        The restrictions are what lowered the score, so their effect is stated
        from the data rather than replaced with an apology.
        """
        zones = "; ".join(
            f"{constraint.label}: {'prohibition' if constraint.prohibits else 'penalty'}, "
            f"{constraint.points_lost:.2f} points"
            for constraint in breakdown.constraints
        )
        return (
            f"Restrictions lowered the score from {breakdown.aspects_score:.2f} to "
            f"{breakdown.total_score:.2f} of {breakdown.scale_max:g} ({zones})."
        )


__all__ = ("LlmInterpreter",)
