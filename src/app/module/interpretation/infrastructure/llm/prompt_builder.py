"""LLM prompt builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import MetricRole, Prompt, ValuePosition


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from app.module.interpretation.domain.value_object import Aspect, AspectMetric, EvaluationBreakdown


_ASPECT_SYSTEM = """Ты — переводчик структурированных данных в человекочитаемый текст.
Твоя задача — объяснить, почему аспект оценки получил такой балл.
Ты используешь ТОЛЬКО переданные факты. Ты НЕ добавляешь своих суждений.
Ты НЕ придумываешь значений, которых нет во входных данных.
Отвечай ТОЛЬКО на русском языке.
Формат ответа: 2–4 предложения связного текста без списков и заголовков.
Упоминай баллы в конечных единицах (например, «2.08 из 4.00 балла»), а не в долях.
Указывай, сколько баллов аспект потерял от максимума.
Причину провала метрики объясняй через её зону: значение выше или ниже ожидаемого."""

_SUMMARY_SYSTEM = """Ты — переводчик структурированных данных в человекочитаемый текст.
Твоя задача — объяснить, как отдельные аспекты оценки повлияли на итоговый балл.
Ты используешь ТОЛЬКО переданные факты. Ты НЕ добавляешь своих суждений.
Ты НЕ придумываешь значений, которых нет во входных данных.
Отвечай ТОЛЬКО на русском языке.
Формат ответа: 3–5 предложений связного текста без списков и заголовков.
Упоминай баллы в конечных единицах (например, «2.08 из 4.00 балла»).
Указывай основной вклад и основные потери."""

_GRADER_SYSTEM = """Ты — строгий проверяющий текста объяснения.
Проверь, что объяснение использует ТОЛЬКО факты из блока ФАКТЫ, не выдумывает
числа и утверждения, соответствует формату (2–4 предложения для аспекта,
3–5 для итога) и написано на русском языке.
Не добавляй новых фактов. Верни ТОЛЬКО JSON без пояснений:
{"ok": true|false, "issues": ["..."], "corrected_text": "..."}
Поле corrected_text заполняй только если ok=false; иначе null."""

# Zone templates of every membership function; the placeholders are the
# function parameters (see the analysis module's fuzzy functions), rendered with
# the metric unit.
_ZONE_TEMPLATES: dict[tuple[str, ValuePosition], str] = {
    ("z_shaped", ValuePosition.OPTIMAL): "в оптимальной зоне (до {optimal_max})",
    ("z_shaped", ValuePosition.PARTIAL_HIGH): (
        "выше оптимума (до {optimal_max}), но ниже критического порога ({acceptable_max})"
    ),
    ("z_shaped", ValuePosition.OUT_HIGH): "за критическим порогом ({acceptable_max}), баллов не даёт",
    ("s_shaped", ValuePosition.OPTIMAL): "в оптимальной зоне (от {max})",
    ("s_shaped", ValuePosition.PARTIAL_LOW): "ниже оптимума (от {max}), но выше минимума ({min})",
    ("s_shaped", ValuePosition.OUT_LOW): "ниже минимума ({min}), баллов не даёт",
    ("trapezoidal", ValuePosition.OUT_LOW): "ниже нижнего порога ({low}), баллов не даёт",
    ("trapezoidal", ValuePosition.PARTIAL_LOW): (
        "ниже оптимальной зоны ({optimal_min}–{optimal_max}), но выше нижнего порога ({low})"
    ),
    ("trapezoidal", ValuePosition.OPTIMAL): "в оптимальной зоне ({optimal_min}–{optimal_max})",
    ("trapezoidal", ValuePosition.PARTIAL_HIGH): (
        "выше оптимальной зоны ({optimal_min}–{optimal_max}), но ниже верхнего порога ({high})"
    ),
    ("trapezoidal", ValuePosition.OUT_HIGH): "выше верхнего порога ({high}), баллов не даёт",
}


class LlmPromptBuilder:
    """Builds the Russian generation and grading prompts."""

    def aspect_prompt(self, aspect: Aspect, metrics: Sequence[AspectMetric]) -> Prompt:
        """Build the prompt for one aspect explanation."""
        strong, weak, neutral = self._split(metrics)
        lines = [
            *self._aspect_header(aspect),
            "",
            "Метрики, которые ДАЛИ баллы (положительно повлияли):",
            self._format_metrics(strong),
        ]
        if weak:
            lines += ["", "Метрики, которые ПРОВАЛИЛИСЬ (не дали баллов):", self._format_metrics(weak)]
        if neutral:
            lines += ["", "Прочие метрики:", self._format_metrics(neutral)]
        lines += [
            "",
            "Объясни:",
            "1. Какие метрики дали основной вклад и почему.",
            "2. Какие метрики провалились и почему (значение выше или ниже ожидаемого).",
            "3. Сколько баллов аспект недобрал от максимума.",
        ]
        return self._compose(_ASPECT_SYSTEM, "\n".join(lines))

    def summary_prompt(
        self,
        breakdown: EvaluationBreakdown,
        top_aspects: Sequence[Aspect],
        explanations: Mapping[str, str],
    ) -> Prompt:
        """Build the prompt for the combined top-aspects summary."""
        lines = [*self._summary_header(breakdown)]
        if breakdown.scenario_description:
            lines.append(f"Описание сценария: {breakdown.scenario_description}")
        lines += ["", "Разбивка по аспектам:", *self._aspect_breakdown(breakdown.aspects)]
        lines += ["", f"Топ-{len(top_aspects)} аспектов по вкладу:"]
        for aspect in top_aspects:
            explanation = explanations.get(aspect.key, "")
            lines.append(f"- {self._name(aspect.name, aspect.key)}: {aspect.points:.2f} балла. {explanation}".strip())
        lines += [
            "",
            "Объясни:",
            "1. Какой аспект дал основной вклад.",
            "2. Где потеряно больше всего баллов.",
            "3. Почему итоговый балл именно такой (что перевесило).",
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

    def aspect_facts(self, aspect: Aspect, metrics: Sequence[AspectMetric]) -> str:
        """Build the fact block of an aspect explanation used by the grader."""
        lines = self._aspect_header(aspect)
        lines += [f"- {self._format_metric(metric)}" for metric in metrics]
        return "\n".join(lines)

    def summary_facts(self, breakdown: EvaluationBreakdown) -> str:
        """Build the fact block of the combined summary used by the grader."""
        return "\n".join([*self._summary_header(breakdown), *self._aspect_breakdown(breakdown.aspects)])

    @staticmethod
    def _compose(system: str, user: str) -> Prompt:
        """Join the system instruction and the user body into one prompt."""
        return Prompt(f"{system}\n\n{user}")

    @classmethod
    def _aspect_header(cls, aspect: Aspect) -> list[str]:
        """Score, weight, points and loss of an aspect."""
        return [
            f"Аспект: {cls._name(aspect.name, aspect.key)}",
            f"Балл аспекта: {aspect.score:.2f} из 1.0",
            f"Вес аспекта: {aspect.weight:.2f} (максимум {aspect.max_points:.2f} балла от итога)",
            f"Фактический вклад: {aspect.points:.2f} из {aspect.max_points:.2f} балла",
            f"Потеряно: {aspect.loss:.2f} балла ({aspect.loss_share:.0%} от возможного)",
        ]

    @staticmethod
    def _summary_header(breakdown: EvaluationBreakdown) -> list[str]:
        """Total score, verdict and scenario of an evaluation."""
        return [
            f"Итоговый балл: {breakdown.total_score:.2f} из {breakdown.scale_max:g} ({breakdown.verdict.label})",
            f"Сценарий: {breakdown.scenario}",
        ]

    @classmethod
    def _aspect_breakdown(cls, aspects: Sequence[Aspect]) -> list[str]:
        """One line of points and loss per aspect."""
        return [
            f"- {cls._name(aspect.name, aspect.key)} (вес {aspect.weight:.2f}): "
            f"{aspect.points:.2f} из {aspect.max_points:.2f} балла "
            f"(потеряно {aspect.loss:.2f}, {aspect.loss_share:.0%})"
            for aspect in aspects
        ]

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

    @classmethod
    def _format_metric(cls, metric: AspectMetric) -> str:
        name = metric.label or metric.key
        raw = "нет данных" if metric.raw_value is None else cls._value(metric.raw_value, metric.unit)
        normalized = "нет" if metric.normalized_value is None else f"{metric.normalized_value:.2f}"
        contribution = "нет" if metric.contribution is None else f"{metric.contribution:.3f}"
        text = f"{name} ({metric.key}): значение {raw}, норм. {normalized}, вклад {contribution}"
        zone = cls._zone(metric)
        return f"{text}; зона: значение {zone}" if zone else text

    @classmethod
    def _zone(cls, metric: AspectMetric) -> str | None:
        """Describe where the raw value lies relative to the function zones."""
        if metric.membership is None:
            return None
        template = _ZONE_TEMPLATES.get((metric.membership.function, metric.position))
        if template is None:
            return None
        params = {key: cls._value(value, metric.unit) for key, value in metric.membership.params.items()}
        return template.format_map(params)

    @staticmethod
    def _value(value: float, unit: str) -> str:
        return f"{value:g}{unit}"

    @staticmethod
    def _name(name: str, key: str) -> str:
        return name or key


__all__ = ("LlmPromptBuilder",)
