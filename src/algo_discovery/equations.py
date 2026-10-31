"""One model call with constrained output and local evidence validation."""

import hashlib
import json
import time
from datetime import UTC, datetime
from uuid import uuid4

import anthropic
from pydantic import ValidationError

from .config import Settings
from .prompt import PROMPT_VERSION, SYSTEM_PROMPT, user_message
from .schemas import EquationRequest, EquationResult, GenerationParameters, MathSpecification, Usage


class GenerationError(RuntimeError):
    """Safe diagnostic that never contains provider bodies or credentials."""

    def __init__(self, message: str, reason: str = "provider_error"):
        super().__init__(message)
        self.reason = reason

    @property
    def model_output_failure(self) -> bool:
        """True when the model answered badly, as opposed to the API being unreachable."""
        return self.reason in MODEL_OUTPUT_FAILURES


MODEL_OUTPUT_FAILURES = {"truncated", "refused", "incomplete", "no_output", "invalid_output"}


def stop_failure(stop_reason: str | None) -> str:
    return {"max_tokens": "truncated", "refusal": "refused"}.get(stop_reason, "incomplete")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_equations(
    request: EquationRequest, settings: Settings, *, client=None
) -> EquationResult:
    if client is None:
        with anthropic.Anthropic(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout_seconds,
            max_retries=0,
        ) as owned_client:
            return generate_equations(request, settings, client=owned_client)

    message = user_message(request)
    started = time.monotonic()
    try:
        response = client.messages.parse(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}],
            output_format=MathSpecification,
            output_config={"effort": settings.effort},
        )
        if response.stop_reason != "end_turn":
            raise GenerationError(
                "Model did not complete the structured response (truncation or refusal). "
                "Check the token budget; no partial result was accepted.",
                stop_failure(response.stop_reason),
            )
        if response.parsed_output is None:
            raise GenerationError(
                "Model returned no structured mathematical specification.", "no_output"
            )
        # Validate even injected clients, and independently check quoted evidence.
        spec = MathSpecification.model_validate(response.parsed_output)
        spec.validate_evidence(request.abstract)
    except anthropic.APIStatusError as exc:
        raise GenerationError(
            f"Claude API returned HTTP {exc.status_code}. Check credentials, model access, "
            "endpoint, and quota. Provider response omitted."
        ) from None
    except anthropic.APIConnectionError:
        raise GenerationError("Claude API connection failed or timed out.") from None
    except (ValidationError, ValueError):
        raise GenerationError(
            "Model output failed schema, consistency, or exact-quote validation. "
            "No valid mathematical specification was accepted.",
            "invalid_output",
        ) from None

    result = EquationResult(
        run_id=str(uuid4()),
        created_at=datetime.now(UTC).isoformat(),
        model=settings.model,
        response_model=response.model,
        prompt_version=PROMPT_VERSION,
        prompt_sha256=sha256(SYSTEM_PROMPT),
        abstract_sha256=sha256(request.abstract),
        request_sha256=sha256(message),
        elapsed_seconds=round(time.monotonic() - started, 3),
        usage=Usage.model_validate(
            {name: getattr(response.usage, name, 0) or 0 for name in Usage.model_fields}
        ),
        stop_reason=response.stop_reason,
        parameters=GenerationParameters(
            max_tokens=settings.max_tokens,
            effort=settings.effort,
            timeout_seconds=settings.timeout_seconds,
        ),
        specification=spec,
    )
    save_artifacts(request, result, settings)
    return result


def render_markdown(result: EquationResult) -> str:
    spec = result.specification
    lines = [
        "# Abstract to equations",
        "",
        f"Status: **{spec.status}**",
        "",
        f"Model: `{result.response_model}`",
        "",
        "Mathematics has not been independently verified.",
        "",
        spec.problem,
        "",
        f"Scope: {spec.reconstruction_scope}",
        "",
    ]
    if spec.symbols:
        lines += ["## Symbols", ""]
        for symbol in spec.symbols:
            lines += [f"- ${symbol.symbol}$: {symbol.meaning}; domain: {symbol.domain}"]
        lines += [""]
    for equation in spec.equations:
        lines += [
            f"## {equation.id}: {equation.label}",
            "",
            "$$",
            equation.latex,
            "$$",
            "",
            equation.description,
            "",
            f"Provenance: `{equation.provenance}`. " + equation.justification,
            "",
        ]
        if equation.abstract_quote:
            lines += [f"Abstract evidence: {equation.abstract_quote}", ""]
        if equation.assumptions:
            lines += ["Equation assumptions:", ""]
            lines += [f"- {item}" for item in equation.assumptions] + [""]
    if spec.registers:
        lines += ["## Registers", ""]
        lines += [f"- {r.name}: {r.size} qubits; {r.role}" for r in spec.registers] + [""]
    for title, value in [
        ("Initial state", spec.initial_state),
        ("Measurement", spec.measurement),
        ("Classical postprocessing", spec.classical_postprocessing),
    ]:
        if value:
            lines += [f"## {title}", "", value, ""]
    if spec.steps:
        lines += ["## Algorithm steps", ""]
        lines += [
            f"{i}. {step.description} ({', '.join(step.equation_ids) or 'no equation reference'})"
            for i, step in enumerate(spec.steps, 1)
        ] + [""]
    for title, items in [
        ("Assumptions", spec.assumptions),
        ("Missing information", spec.missing_information),
    ]:
        if items:
            lines += [f"## {title}", ""] + [f"- {item}" for item in items] + [""]
    return "\n".join(lines)


def save_artifacts(request: EquationRequest, result: EquationResult, settings: Settings) -> None:
    directory = settings.artifact_dir / result.run_id
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "request.json").write_text(
        json.dumps(request.model_dump(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (directory / "result.json").write_text(
        result.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )
    (directory / "equations.md").write_text(render_markdown(result), encoding="utf-8")
