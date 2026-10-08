"""LLM prompt builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import MetricRole, Prompt, ValuePosition


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from app.module.interpretation.domain.value_object import Aspect, AspectMetric, EvaluationBreakdown


_ASPECT_SYSTEM = """You turn structured data into human-readable text.
Your task is to explain why an evaluation aspect received its score.
Use ONLY the facts provided. Do NOT add your own judgments.
Do NOT invent values that are not in the input.
Answer ONLY in English.
Answer format: 2-4 sentences of plain prose, no lists or headings.
State points on the final scale (for example, "2.08 of 4.00 points"), not fractions.
State how many points the aspect lost from its maximum.
Explain why a metric failed through its zone: the value is above or below the expected range.
Refer to metrics by their names exactly as given."""

_SUMMARY_SYSTEM = """You turn structured data into human-readable text.
Your task is to explain how the individual aspects shaped the total score.
Use ONLY the facts provided. Do NOT add your own judgments.
Do NOT invent values that are not in the input.
Answer ONLY in English.
Answer format: 3-5 sentences of plain prose, no lists or headings.
State points on the final scale (for example, "2.08 of 4.00 points").
Name the main contribution and the main losses."""

_GRADER_SYSTEM = """You are a strict reviewer of an explanation text.
Check that the explanation uses ONLY the facts from the FACTS block, does not
invent numbers or claims, follows the format (2-4 sentences for an aspect,
3-5 for the summary) and is written in English.
Do not add new facts. Return ONLY JSON without any commentary:
{"ok": true|false, "issues": ["..."], "corrected_text": "..."}
Fill corrected_text only when ok=false; otherwise null."""

# Zone templates of every membership function; the placeholders are the
# function parameters (see the analysis module's fuzzy functions), rendered with
# the metric unit.
_ZONE_TEMPLATES: dict[tuple[str, ValuePosition], str] = {
    ("z_shaped", ValuePosition.OPTIMAL): "in the optimal zone (up to {optimal_max})",
    ("z_shaped", ValuePosition.PARTIAL_HIGH): (
        "above the optimum (up to {optimal_max}) but below the critical threshold ({acceptable_max})"
    ),
    ("z_shaped", ValuePosition.OUT_HIGH): "beyond the critical threshold ({acceptable_max}), earns no points",
    ("s_shaped", ValuePosition.OPTIMAL): "in the optimal zone (from {max})",
    ("s_shaped", ValuePosition.PARTIAL_LOW): "below the optimum (from {max}) but above the minimum ({min})",
    ("s_shaped", ValuePosition.OUT_LOW): "at or below the minimum ({min}), earns no points",
    ("trapezoidal", ValuePosition.OUT_LOW): "below the lower threshold ({low}), earns no points",
    ("trapezoidal", ValuePosition.PARTIAL_LOW): (
        "below the optimal range ({optimal_min} to {optimal_max}) but above the lower threshold ({low})"
    ),
    ("trapezoidal", ValuePosition.OPTIMAL): "in the optimal range ({optimal_min} to {optimal_max})",
    ("trapezoidal", ValuePosition.PARTIAL_HIGH): (
        "above the optimal range ({optimal_min} to {optimal_max}) but below the upper threshold ({high})"
    ),
    ("trapezoidal", ValuePosition.OUT_HIGH): "above the upper threshold ({high}), earns no points",
}

# Display symbols of the unit codes used by the metric modules.
_UNIT_SYMBOLS: dict[str, str] = {
    "deg": "°",
    "degC": "°C",
    "m2": "m²",
    "km/km2": "km/km²",
}
_RATIO_UNIT = "ratio"
_ATTACHED_UNITS = frozenset({"°", "%"})


class LlmPromptBuilder:
    """Builds the English generation and grading prompts."""

    def aspect_prompt(self, aspect: Aspect, metrics: Sequence[AspectMetric]) -> Prompt:
        """Build the prompt for one aspect explanation."""
        strong, weak, neutral = self._split(metrics)
        lines = [
            *self._aspect_header(aspect),
            "",
            "Metrics that EARNED points (positive influence):",
            self._format_metrics(strong),
        ]
        if weak:
            lines += ["", "Metrics that FAILED (earned no points):", self._format_metrics(weak)]
        if neutral:
            lines += ["", "Other metrics:", self._format_metrics(neutral)]
        lines += [
            "",
            "Explain:",
            "1. Which metrics made the main contribution and why.",
            "2. Which metrics failed and why (the value is above or below the expected range).",
            "3. How many points the aspect fell short of its maximum.",
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
            lines.append(f"Scenario description: {breakdown.scenario_description}")
        lines += ["", "Breakdown by aspect:", *self._aspect_breakdown(breakdown.aspects)]
        lines += ["", f"Top {len(top_aspects)} aspects by contribution:"]
        for aspect in top_aspects:
            explanation = explanations.get(aspect.key, "")
            lines.append(f"- {self._name(aspect.name, aspect.key)}: {aspect.points:.2f} points. {explanation}".strip())
        lines += [
            "",
            "Explain:",
            "1. Which aspect made the main contribution.",
            "2. Where the most points were lost.",
            "3. Why the total score is what it is (what outweighed what).",
        ]
        return self._compose(_SUMMARY_SYSTEM, "\n".join(lines))

    def grader_prompt(self, facts: str, explanation: str) -> Prompt:
        """Build the prompt of the grader pass."""
        user = f"FACTS:\n{facts}\n\nEXPLANATION:\n{explanation}\n\nReturn the JSON verdict."
        return self._compose(_GRADER_SYSTEM, user)

    @staticmethod
    def retry_prompt(prompt: Prompt, issues: Sequence[str]) -> Prompt:
        """Build the retry prompt from the rejected prompt and its issues."""
        correction = "; ".join(issues) or "none"
        return Prompt(f"{prompt.unwrap()}\n\nFix the reviewer's remarks: {correction}.")

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
            f"Aspect: {cls._name(aspect.name, aspect.key)}",
            f"Aspect score: {aspect.score:.2f} of 1.0",
            f"Aspect weight: {aspect.weight:.2f} (up to {aspect.max_points:.2f} points of the total)",
            f"Actual contribution: {aspect.points:.2f} of {aspect.max_points:.2f} points",
            f"Lost: {aspect.loss:.2f} points ({aspect.loss_share:.0%} of the maximum)",
        ]

    @staticmethod
    def _summary_header(breakdown: EvaluationBreakdown) -> list[str]:
        """Total score, verdict and scenario of an evaluation."""
        return [
            f"Total score: {breakdown.total_score:.2f} of {breakdown.scale_max:g} ({breakdown.verdict.label})",
            f"Scenario: {breakdown.scenario}",
        ]

    @classmethod
    def _aspect_breakdown(cls, aspects: Sequence[Aspect]) -> list[str]:
        """One line of points and loss per aspect."""
        return [
            f"- {cls._name(aspect.name, aspect.key)} (weight {aspect.weight:.2f}): "
            f"{aspect.points:.2f} of {aspect.max_points:.2f} points "
            f"(lost {aspect.loss:.2f}, {aspect.loss_share:.0%})"
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
            return "  (none)"
        return "\n".join(f"  - {cls._format_metric(metric)}" for metric in metrics)

    @classmethod
    def _format_metric(cls, metric: AspectMetric) -> str:
        # Only the label is shown: echoing the canonical key made the model
        # write things like "Min distance to (power_line:min_distance_to)".
        name = metric.label or metric.key
        raw = "no data" if metric.raw_value is None else cls._value(metric.raw_value, metric.unit)
        normalized = "n/a" if metric.normalized_value is None else f"{metric.normalized_value:.2f}"
        contribution = "n/a" if metric.contribution is None else f"{metric.contribution:.3f}"
        text = f"{name}: value {raw}, normalized {normalized}, contribution {contribution}"
        zone = cls._zone(metric)
        return f"{text}; zone: the value is {zone}" if zone else text

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
        """Render a value with a readable unit (``135.2 m``, ``6.2°``, ``6%``)."""
        if unit == _RATIO_UNIT:
            return f"{value * 100:.3g}%"
        symbol = _UNIT_SYMBOLS.get(unit, unit)
        if not symbol:
            return f"{value:g}"
        separator = "" if symbol in _ATTACHED_UNITS or symbol.startswith("°") else " "
        return f"{value:g}{separator}{symbol}"

    @staticmethod
    def _name(name: str, key: str) -> str:
        return name or key


__all__ = ("LlmPromptBuilder",)
