"""LLM prompt builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import MetricRole, Prompt


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from app.module.interpretation.domain.value_object import Aspect, AspectMetric, EvaluationBreakdown


_ASPECT_SYSTEM = """Ты — переводчик структурированных данных в человекочитаемый текст.
Твоя задача — объяснить, почему аспект оценки получил такой балл.
Ты используешь ТОЛЬКО переданные факты. Ты НЕ добавляешь своих суждений.
Ты НЕ придумываешь значений, которых нет во входных данных.
Отвечай ТОЛЬКО на русском языке.
Формат ответа: 2–4 предложения связного текста без списков и заголовков."""

_SUMMARY_SYSTEM = """Ты — переводчик структурированных данных в человекочитаемый текст.
Твоя задача — объяснить, как отдельные аспекты оценки повлияли на итоговый балл.
Ты используешь ТОЛЬКО переданные факты. Ты НЕ добавляешь своих суждений.
Ты НЕ придумываешь значений, которых нет во входных данных.
Отвечай ТОЛЬКО на русском языке.
Формат ответа: 3–5 предложений связного текста без списков и заголовков."""

_GRADER_SYSTEM = """Ты — строгий проверяющий текста объяснения.
Проверь, что объяснение использует ТОЛЬКО факты из блока ФАКТЫ, не выдумывает
числа и утверждения, соответствует формату (2–4 предложения для аспекта,
3–5 для итога) и написано на русском языке.
Не добавляй новых фактов. Верни ТОЛЬКО JSON без пояснений:
{"ok": true|false, "issues": ["..."], "corrected_text": "..."}
Поле corrected_text заполняй только если ok=false; иначе null."""


class LlmPromptBuilder:
    """Builds the Russian generation and grading prompts."""

    def aspect_prompt(self, aspect: Aspect, metrics: Sequence[AspectMetric]) -> Prompt:
        """Build the prompt for one aspect explanation."""
        strong, weak, neutral = self._split(metrics)
        lines = [
            f"Аспект: {self._name(aspect.name, aspect.key)}",
            f"Балл аспекта: {aspect.score:.2f} из 1.0",
            f"Вклад в итоговый балл: {aspect.contribution:.3f}",
            "",
            "Сильные метрики (внесли большой вклад):",
            self._format_metrics(strong),
            "",
            "Слабые метрики (низкое значение, не внесли вклад):",
            self._format_metrics(weak),
        ]
        if neutral:
            lines += ["", "Прочие метрики:", self._format_metrics(neutral)]
        lines += [
            "",
            "Объясни, почему аспект получил такой балл.",
            "Укажи, какие метрики сработали хорошо, а какие провалились.",
        ]
        return self._compose(_ASPECT_SYSTEM, "\n".join(lines))

    def summary_prompt(
        self,
        breakdown: EvaluationBreakdown,
        top_aspects: Sequence[Aspect],
        explanations: Mapping[str, str],
        weights_context: Mapping[str, float],
    ) -> Prompt:
        """Build the prompt for the combined top-aspects summary."""
        lines = [
            f"Итоговый балл: {breakdown.total_score:g} из {breakdown.scale}",
            f"Сценарий: {breakdown.scenario}",
        ]
        if breakdown.scenario_description:
            lines.append(f"Описание сценария: {breakdown.scenario_description}")
        lines += ["", "Топ-5 аспектов по вкладу:"]
        for aspect in top_aspects:
            explanation = explanations.get(aspect.key, "")
            lines.append(
                f"- {self._name(aspect.name, aspect.key)}: балл {aspect.score:.2f}, "
                f"вклад {aspect.contribution:.3f}. {explanation}".strip()
            )
        lines += ["", "Веса аспектов (доля вклада):"]
        for key, weight in weights_context.items():
            lines.append(f"- {key}: {weight:.2f}")
        lines += [
            "",
            "Объясни, как эти аспекты сформировали итоговый балл.",
            "Обрати внимание на аспекты с большим весом и высоким баллом.",
        ]
        return self._compose(_SUMMARY_SYSTEM, "\n".join(lines))

    def grader_prompt(self, facts: str, explanation: str) -> Prompt:
        """Build the prompt of the grader pass."""
        user = f"ФАКТЫ:\n{facts}\n\nОБЪЯСНЕНИЕ:\n{explanation}\n\nВерни JSON-вердикт."
        return self._compose(_GRADER_SYSTEM, user)

    @staticmethod
    def retry_prompt(prompt: Prompt, issues: Sequence[str]) -> Prompt:
        """Build the retry prompt from the rejected prompt and its issues."""
        correction = "; ".join(issues) or "нет"
        return Prompt(f"{prompt.unwrap()}\n\nИсправь замечания проверяющего: {correction}.")

    def facts(self, subject: str, metrics: Sequence[AspectMetric]) -> str:
        """Build the fact block used by the grader."""
        lines = [subject]
        for metric in metrics:
            lines.append(f"- {self._format_metric(metric)}")
        return "\n".join(lines)

    @staticmethod
    def _compose(system: str, user: str) -> Prompt:
        """Join the system instruction and the user body into one prompt."""
        return Prompt(f"{system}\n\n{user}")

    @staticmethod
    def _split(
        metrics: Sequence[AspectMetric],
    ) -> tuple[list[AspectMetric], list[AspectMetric], list[AspectMetric]]:
        strong = [metric for metric in metrics if metric.role is MetricRole.STRONG]
        weak = [metric for metric in metrics if metric.role is MetricRole.WEAK]
        neutral = [metric for metric in metrics if metric.role is MetricRole.NEUTRAL]
        return strong, weak, neutral

    @classmethod
    def _format_metrics(cls, metrics: Sequence[AspectMetric]) -> str:
        if not metrics:
            return "  (нет)"
        return "\n".join(f"  - {cls._format_metric(metric)}" for metric in metrics)

    @staticmethod
    def _format_metric(metric: AspectMetric) -> str:
        name = metric.label or metric.key
        raw = "нет данных" if metric.raw_value is None else f"{metric.raw_value:g}{metric.unit}"
        normalized = "нет" if metric.normalized_value is None else f"{metric.normalized_value:.2f}"
        contribution = "нет" if metric.contribution is None else f"{metric.contribution:.3f}"
        return f"{name} ({metric.key}): значение {raw}, норм. {normalized}, вклад {contribution}"

    @staticmethod
    def _name(name: str, key: str) -> str:
        return name or key


__all__ = ("LlmPromptBuilder",)
