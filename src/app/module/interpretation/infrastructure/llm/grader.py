"""LLM-backed interpretation grader."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from dacite import Config, DaciteError, from_dict

from app.module.interpretation.domain.value_object import GradeVerdict
from app.module.shared.domain.error import ValidationError
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.interpretation.infrastructure.llm.llm_client import LLMClient
    from app.module.interpretation.infrastructure.llm.prompt_builder import LlmPromptBuilder


class LlmGrader:
    """Grades an explanation with a second model pass.

    The grader must not invent facts; it only validates the draft. When the
    answer cannot be parsed into a :class:`GradeVerdict` the draft is accepted
    (and logged) rather than failing the whole report.
    """

    def __init__(self, llm_client: LLMClient, prompt_builder: LlmPromptBuilder) -> None:
        self._llm_client = llm_client
        self._prompt_builder = prompt_builder
        self._logger = get_logger("app.interpretation.grader")

    async def grade(self, facts: str, explanation: str) -> GradeVerdict:
        """Grade ``explanation`` against ``facts``."""
        completion = await self._llm_client.complete(self._prompt_builder.grader_prompt(facts, explanation))
        return self._parse(completion.unwrap())

    def _parse(self, raw: str) -> GradeVerdict:
        """Parse the grader answer into a verdict."""
        payload = self._extract_json(raw)
        if payload is None:
            self._logger.warning("Grader returned an unparseable answer: %r", raw[:200])
            return GradeVerdict(ok=True, issues=("grader_unparseable",))
        try:
            verdict = from_dict(data_class=GradeVerdict, data=payload, config=Config(cast=[tuple]))
        except DaciteError, ValidationError:
            self._logger.warning("Grader answer did not match the expected shape: %r", raw[:200])
            return GradeVerdict(ok=True, issues=("grader_unparseable",))

        corrected_text = verdict.corrected_text.strip() if verdict.corrected_text else None
        if verdict.ok:
            corrected_text = None
        return GradeVerdict(ok=verdict.ok, issues=tuple(verdict.issues), corrected_text=corrected_text)

    @staticmethod
    def _extract_json(raw: str) -> dict[str, object] | None:
        """Extract the first JSON object from a text answer."""
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end < start:
            return None
        try:
            payload = json.loads(raw[start : end + 1])
        except json.JSONDecodeError:
            return None
        return payload if isinstance(payload, dict) else None


__all__ = ("LlmGrader",)
