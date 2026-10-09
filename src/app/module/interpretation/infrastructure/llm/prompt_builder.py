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
Use ONE scale: points of the total score (for example, "earned 2.08 of 4.00 points, losing 1.92").
You may add the share of the aspect's maximum as a percentage (for example, "52% of its maximum").
NEVER write a score as a fraction of 1.0.
Strengths earned their full points; weaknesses lost points.
Explain why a weakness lost points through its zone: the value is above or below the expected range.
Attribute the lost points to the weaknesses by the points each of them lost.
Only the most significant metrics are listed; never call a listed metric the only reason.
Refer to metrics by their names exactly as given.
Do NOT start with or include labels such as "Aspect:" or "Summary:"; write plain prose only."""

_SUMMARY_SYSTEM = """You turn structured data into human-readable text.
Your task is to explain how the individual aspects shaped the total score.
Use ONLY the facts provided. Do NOT add your own judgments.
Do NOT invent values that are not in the input.
Answer ONLY in English.
Answer format: 3-5 sentences of plain prose, no lists or headings.
Use ONE scale: points of the total score (for example, "2.08 of 4.00 points").
NEVER write a score as a fraction of 1.0.
Name the main contribution and the main losses.
Do NOT start with or include labels such as "Aspect:" or "Summary:"; write plain prose only."""

_GRADER_SYSTEM = """You are a strict reviewer of an explanation text.
The FACTS block is exactly the input the explanation was written from.
Check that the explanation:
- uses only numbers that appear in the FACTS block (rounding is fine);
- names only metrics and aspects that appear in the FACTS block;
- never calls a strength a weakness or a weakness a strength;
- describes every zone in the same direction as the FACTS (above or below);
- makes no claims or causes that the FACTS block does not support.
Rephrasing, shortening and leaving facts out are fine and are NOT issues.
Do NOT rewrite the explanation. Return ONLY JSON without any commentary:
{"ok": true|false, "issues": ["..."]}
Each issue quotes the wrong statement and says what the FACTS state instead.
issues is empty when ok is true."""

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
        lines = [
            *self._aspect_body(aspect, metrics),
            "",
            "Explain:",
            "1. Which strengths earned the most points.",
            "2. Which weaknesses lost the most points and why (the value is above or below the expected range).",
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
        lines = [
            *self._summary_body(breakdown, top_aspects, explanations),
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
    def retry_prompt(prompt: Prompt, draft: str, issues: Sequence[str]) -> Prompt:
        """Build the retry prompt from the rejected prompt, its draft and the reviewer remarks."""
        remarks = "\n".join(f"- {issue}" for issue in issues) or "- none"
        return Prompt(
            f"{prompt.unwrap()}\n\nYour previous answer:\n{draft}\n\n"
            f"A reviewer found these problems in it:\n{remarks}\n\n"
            "Write the answer again, fixing these problems and following all the rules above."
        )

    def aspect_facts(self, aspect: Aspect, metrics: Sequence[AspectMetric]) -> str:
        """Build the fact block of an aspect explanation: the same data the generator gets."""
        return "\n".join(self._aspect_body(aspect, metrics))

    def summary_facts(
        self,
        breakdown: EvaluationBreakdown,
        top_aspects: Sequence[Aspect],
        explanations: Mapping[str, str],
    ) -> str:
        """Build the fact block of the combined summary: the same data the generator gets."""
        return "\n".join(self._summary_body(breakdown, top_aspects, explanations))

    @staticmethod
    def _compose(system: str, user: str) -> Prompt:
        """Join the system instruction and the user body into one prompt."""
        return Prompt(f"{system}\n\n{user}")

    @classmethod
    def _aspect_body(cls, aspect: Aspect, metrics: Sequence[AspectMetric]) -> list[str]:
        """Header, strengths and weaknesses of an aspect: the data of its prompt and facts."""
        strong = [metric for metric in metrics if metric.role is MetricRole.STRONG]
        weak = [metric for metric in metrics if metric.role is MetricRole.WEAK]
        lines = cls._aspect_header(aspect)
        if weak:
            listed_loss = sum(metric.loss for metric in weak)
            lines.append(
                f"The weaknesses listed below account for {listed_loss:.2f} of the {aspect.loss:.2f} points lost."
            )
        lines += [
            "",
            "Strengths (metrics that earned their full points):",
            cls._format_metrics(strong),
            "",
            "Weaknesses (metrics that lost points, the biggest loss first):",
            cls._format_metrics(weak),
        ]
        return lines

    @classmethod
    def _aspect_header(cls, aspect: Aspect) -> list[str]:
        """Score, weight, points and loss of an aspect."""
        # One scale only: points of the total score, plus the share of the
        # aspect's maximum as a percentage. A 0-1 aspect score next to points
        # made the model write "scored 0.46 of 1.0, lost 0.81 points".
        return [
            f"The {cls._name(aspect.name, aspect.key)} aspect can contribute up to "
            f"{aspect.max_points:.2f} points to the total score.",
            f"It earned {aspect.points:.2f} of {aspect.max_points:.2f} points "
            f"({aspect.score:.0%} of its maximum) and lost {aspect.loss:.2f} points.",
        ]

    @classmethod
    def _summary_body(
        cls,
        breakdown: EvaluationBreakdown,
        top_aspects: Sequence[Aspect],
        explanations: Mapping[str, str],
    ) -> list[str]:
        """Total score, per-aspect breakdown and top aspects: the data of the summary prompt and facts."""
        lines = [
            f"Total score: {breakdown.total_score:.2f} of {breakdown.scale_max:g} ({breakdown.verdict.label})",
            f"Scenario: {breakdown.scenario}",
        ]
        if breakdown.scenario_description:
            lines.append(f"Scenario description: {breakdown.scenario_description}")
        lines += ["", "Breakdown by aspect:"]
        lines += [
            f"- {cls._name(aspect.name, aspect.key)}: earned {aspect.points:.2f} of "
            f"{aspect.max_points:.2f} points ({aspect.score:.0%} of its maximum), lost {aspect.loss:.2f} points"
            for aspect in breakdown.aspects
        ]
        lines += ["", f"Top {len(top_aspects)} aspects by contribution:"]
        for aspect in top_aspects:
            explanation = explanations.get(aspect.key, "")
            lines.append(f"- {cls._name(aspect.name, aspect.key)}: {aspect.points:.2f} points. {explanation}".strip())
        return lines

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
        # Metric points are on the same scale as the aspect points (points of
        # the total score), so the prompt keeps a single scale.
        points = f"earned {metric.points:.2f} of {metric.max_points:.2f} points"
        if metric.role is MetricRole.WEAK:
            points += f", lost {metric.loss:.2f}"
        text = f"{name}: value {raw}; {points}"
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
