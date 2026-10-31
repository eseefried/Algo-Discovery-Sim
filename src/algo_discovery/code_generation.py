"""Continue the same agent with its abstract and saved mathematical state."""

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import anthropic
from pydantic import ValidationError

from .code_prompt import PROMPT_VERSION, SYSTEM_PROMPT, code_messages
from .code_schemas import CircuitArtifact, CircuitValidation, CodeRequest, CodeResult
from .config import Settings
from .equations import GenerationError, sha256
from .sandbox import validate_in_docker
from .schemas import EquationRequest, EquationResult, GenerationParameters, Usage
from .source_checks import check_source


def load_code_request(
    equations_file: Path, *, request_file: Path | None = None, **kwargs
) -> CodeRequest:
    original = (
        request_file if request_file is not None else equations_file.with_name("request.json")
    )
    return CodeRequest(
        equation_request=EquationRequest.model_validate_json(original.read_text(encoding="utf-8")),
        equation_result=EquationResult.model_validate_json(
            equations_file.read_text(encoding="utf-8")
        ),
        **kwargs,
    )


def check_mapping(artifact: CircuitArtifact, request: CodeRequest) -> None:
    expected = {e.id for e in request.equation_result.specification.equations}
    mapped = [item.equation_id for item in artifact.equation_mapping]
    if len(mapped) != len(set(mapped)) or set(mapped) != expected:
        raise ValueError("Each source equation must be mapped exactly once.")
    if any(
        item.disposition == "implemented" and not item.code_location
        for item in artifact.equation_mapping
    ):
        raise ValueError("Implemented equations need code locations.")
    if any(
        not set(change.equation_ids).issubset(expected) for change in artifact.specification_changes
    ):
        raise ValueError("Specification changes refer to unknown equations.")


def generate_code(request: CodeRequest, settings: Settings, *, client=None) -> CodeResult:
    if client is None:
        with anthropic.Anthropic(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout_seconds,
            max_retries=0,
        ) as owned_client:
            return generate_code(request, settings, client=owned_client)
    messages = code_messages(request)
    started = time.monotonic()
    try:
        response = client.messages.parse(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=SYSTEM_PROMPT,
            messages=messages,
            output_format=CircuitArtifact,
            output_config={"effort": settings.effort},
        )
        if response.stop_reason != "end_turn" or response.parsed_output is None:
            raise GenerationError(
                "Model did not complete a structured code artifact; no code accepted."
            )
        artifact = CircuitArtifact.model_validate(response.parsed_output)
        check_mapping(artifact, request)
    except anthropic.APIStatusError as exc:
        raise GenerationError(
            f"Claude API returned HTTP {exc.status_code}. Check credentials, model access, "
            "endpoint, and quota. Provider response omitted."
        ) from None
    except anthropic.APIConnectionError:
        raise GenerationError("Claude API connection failed or timed out.") from None
    except (ValidationError, ValueError):
        raise GenerationError(
            "Code artifact failed schema or equation-mapping validation."
        ) from None

    validation = CircuitValidation(
        status="not_run", reference=request.reference, detail="No generated source was executed."
    )
    source_passed = False
    compiled_qasm = None
    instance = (
        request.instance
        if request.instance is not None
        else json.loads(artifact.example_instance_json)
    )
    if artifact.status == "generated":
        try:
            check_source(artifact.source_python)
            source_passed = True
        except (ValueError, SyntaxError, TypeError, RecursionError) as exc:
            validation = CircuitValidation(
                status="failed",
                reference=request.reference,
                detail="Generated source was not executed: "
                + type(exc).__name__
                + ": "
                + str(exc)[:300],
            )
        if source_passed and request.validate_circuit:
            validation, compiled_qasm = validate_in_docker(
                artifact.source_python, instance, request.reference
            )

    result = CodeResult(
        run_id=str(uuid4()),
        parent_run_id=request.equation_result.run_id,
        created_at=datetime.now(UTC).isoformat(),
        model=settings.model,
        response_model=response.model,
        prompt_version=PROMPT_VERSION,
        prompt_sha256=sha256(SYSTEM_PROMPT),
        request_sha256=sha256(json.dumps(messages, ensure_ascii=False)),
        source_specification_sha256=sha256(request.equation_result.specification.model_dump_json()),
        source_python_sha256=sha256(artifact.source_python),
        elapsed_seconds=round(time.monotonic() - started, 3),
        usage=Usage.model_validate(
            {k: getattr(response.usage, k, 0) or 0 for k in Usage.model_fields}
        ),
        stop_reason=response.stop_reason,
        parameters=GenerationParameters(
            max_tokens=settings.max_tokens,
            effort=settings.effort,
            timeout_seconds=settings.timeout_seconds,
        ),
        static_checks_passed=source_passed,
        artifact=artifact,
        validation=validation,
    )
    save_code_artifacts(request, result, instance, compiled_qasm, settings)
    return result


def save_code_artifacts(
    request: CodeRequest,
    result: CodeResult,
    instance: dict,
    compiled_qasm: str | None,
    settings: Settings,
) -> None:
    directory = settings.artifact_dir / result.run_id
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "request.json").write_text(
        request.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )
    (directory / "result.json").write_text(
        result.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )
    (directory / "validation.json").write_text(
        result.validation.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )
    (directory / "instance.json").write_text(
        json.dumps(instance, indent=2) + "\n", encoding="utf-8"
    )
    if result.artifact.source_python:
        (directory / "circuit.py").write_text(
            result.artifact.source_python + "\n", encoding="utf-8"
        )
    if compiled_qasm:
        (directory / "compiled.qasm").write_text(compiled_qasm + "\n", encoding="utf-8")
    lines = [
        "# Equation to Qiskit",
        "",
        result.artifact.summary,
        "",
        f"Source equation run: `{result.parent_run_id}`",
        "",
        f"Generation: **{result.artifact.status}**; validation: **{result.validation.status}**.",
        "",
        result.validation.detail,
        "",
        "Paper fidelity has not been independently verified.",
        "",
    ]
    for title, entries in [
        ("Register layout", result.artifact.register_layout),
        ("Assumptions", result.artifact.assumptions),
        ("Unresolved issues", result.artifact.unresolved_issues),
    ]:
        if entries:
            lines += [f"## {title}", ""] + [f"- {item}" for item in entries] + [""]
    lines += ["## Equation mapping", ""]
    for item in result.artifact.equation_mapping:
        lines += [
            (
                f"- `{item.equation_id}`: {item.disposition}; "
                f"{item.code_location or 'no code location'}. {item.explanation}"
            )
        ]
    lines += ["", "## Specification changes", ""]
    for change in result.artifact.specification_changes:
        lines += [f"- {', '.join(change.equation_ids)}: {change.change} Reason: {change.reason}"]
    (directory / "implementation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
