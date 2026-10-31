"""Specifications produced outside block one (e.g. a multi-agent swarm).

They enter the same code and simulation stages as single-agent runs. Each is saved as a
normal equation run so hashes, evidence checks, and evaluation apply unchanged; model
and usage fields record the external source instead of a block-one model call.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from pydantic import Field, model_validator

from .config import Settings
from .equations import save_artifacts, sha256
from .prompt import user_message
from .schemas import EquationRequest, EquationResult, MathSpecification, StrictModel, Usage

DATASET_ABSTRACTS = Path("data/circuit_dataset_300_v1/abstracts")


class ExternalSpec(StrictModel):
    source: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    arxiv_id: str | None = Field(default=None, pattern=r"^\d{4}\.\d{4,5}$")
    abstract: str | None = None
    experiment_scope: str | None = None
    specification: MathSpecification

    @model_validator(mode="after")
    def need_abstract(self):
        if self.abstract is None and self.arxiv_id is None:
            raise ValueError("Provide arxiv_id (dataset abstract) or the abstract text.")
        return self

    def request(self) -> EquationRequest:
        abstract = self.abstract
        if abstract is None:
            path = DATASET_ABSTRACTS / f"arxiv-{self.arxiv_id}.txt"
            abstract = path.read_text(encoding="utf-8")
        return EquationRequest(abstract=abstract, experiment_scope=self.experiment_scope)


def from_equation_run(result_file: Path, arxiv_id: str | None = None) -> ExternalSpec:
    """Wrap a saved block-one run so the single agent can take the same path."""
    result = EquationResult.model_validate_json(result_file.read_text(encoding="utf-8"))
    request = EquationRequest.model_validate_json(
        result_file.with_name("request.json").read_text(encoding="utf-8")
    )
    return ExternalSpec(
        source="single_agent",
        arxiv_id=arxiv_id,
        abstract=request.abstract,
        experiment_scope=request.experiment_scope,
        specification=result.specification,
    )


def load_spec(path: Path) -> ExternalSpec:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "abstract_sha256" in data:
        return from_equation_run(path)
    return ExternalSpec.model_validate(data)


def save_as_equation_run(spec: ExternalSpec, settings: Settings) -> EquationResult:
    request = spec.request()
    # Same exact-quote rule as block one: abstract_quote must appear in the abstract.
    spec.specification.validate_evidence(request.abstract)
    label = f"external:{spec.source}"
    result = EquationResult(
        run_id=str(uuid4()),
        created_at=datetime.now(UTC).isoformat(),
        model=label,
        response_model=label,
        prompt_version=label,
        prompt_sha256=sha256(spec.specification.model_dump_json()),
        abstract_sha256=sha256(request.abstract),
        request_sha256=sha256(user_message(request)),
        elapsed_seconds=0,
        usage=Usage(input_tokens=0, output_tokens=0),
        stop_reason="external",
        specification=spec.specification,
    )
    save_artifacts(request, result, settings)
    return result
