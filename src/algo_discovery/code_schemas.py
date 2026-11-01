"""Contracts for the second stage; generated Python is data until isolated execution."""

import hashlib
import json
from typing import Any, Literal

from pydantic import Field, model_validator

from .prompt import user_message
from .schemas import EquationRequest, EquationResult, GenerationParameters, StrictModel, Usage

Reference = Literal["none", "modular_weighted_sum"]


class CodeRequest(StrictModel):
    equation_request: EquationRequest
    equation_result: EquationResult
    validate_circuit: bool = False
    reference: Reference = "none"
    instance: dict[str, Any] | None = None

    @model_validator(mode="after")
    def check_source(self):
        abstract_hash = hashlib.sha256(self.equation_request.abstract.encode()).hexdigest()
        request_hash = hashlib.sha256(user_message(self.equation_request).encode()).hexdigest()
        if abstract_hash != self.equation_result.abstract_sha256:
            raise ValueError("Abstract does not match the equation run.")
        if request_hash != self.equation_result.request_sha256:
            raise ValueError("Original abstract/scope request does not match the equation run.")
        self.equation_result.specification.validate_evidence(self.equation_request.abstract)
        if self.equation_result.specification.status not in {"specified", "partial"}:
            raise ValueError("The equation stage did not provide a reconstructable specification.")
        if self.reference != "none" and not self.validate_circuit:
            raise ValueError("A reference check requires validate_circuit=true.")
        if self.instance is not None:
            json.dumps(self.instance, allow_nan=False)
        return self


class EquationMapping(StrictModel):
    equation_id: str
    disposition: Literal["implemented", "background", "out_of_scope"]
    code_location: str | None
    explanation: str


class SpecificationChange(StrictModel):
    equation_ids: list[str]
    change: str
    reason: str


class CircuitArtifact(StrictModel):
    status: Literal["generated", "insufficient_information", "unsupported"]
    summary: str = Field(min_length=1)
    source_python: str = Field(max_length=40000)
    example_instance_json: str = Field(
        max_length=10000,
        description="A JSON object for build_circuit(instance), encoded as a string",
    )
    register_layout: list[str] = Field(description="Qubit indices and encoding for the example")
    equation_mapping: list[EquationMapping]
    specification_changes: list[SpecificationChange]
    assumptions: list[str]
    unresolved_issues: list[str]

    @model_validator(mode="after")
    def check_artifact(self):
        instance = json.loads(self.example_instance_json)
        if not isinstance(instance, dict):
            raise ValueError("Example instance must be a JSON object.")  # noqa: TRY004 - Pydantic validator.
        json.dumps(instance, allow_nan=False)
        if self.status == "generated" and not self.source_python.strip():
            raise ValueError("Generated status requires source code.")
        if self.status != "generated" and self.source_python.strip():
            raise ValueError("Abstentions must not contain executable source.")
        return self


class CircuitValidation(StrictModel):
    status: Literal["not_run", "build_passed", "reference_passed", "failed", "unavailable"]
    detail: str
    reference: Reference = "none"
    worker_image_id: str | None = None
    qiskit_version: str | None = None
    num_qubits: int | None = None
    gate_count: int | None = None
    depth: int | None = None
    basis_states_checked: int = 0
    basis_probabilities_passed: bool | None = None
    full_operator_error: float | None = None
    superposition_fidelity: float | None = None
    paper_fidelity_verified: Literal[False] = False


class CodeResult(StrictModel):
    backend: Literal["anthropic", "local"] = "anthropic"
    schema_version: Literal["1.0"] = "1.0"
    stage: Literal["equations_to_qiskit"] = "equations_to_qiskit"
    run_id: str
    parent_run_id: str
    created_at: str
    model: str
    response_model: str
    prompt_version: str
    prompt_sha256: str
    request_sha256: str
    source_specification_sha256: str
    source_python_sha256: str
    elapsed_seconds: float
    usage: Usage
    stop_reason: str
    parameters: GenerationParameters
    static_checks_passed: bool
    artifact: CircuitArtifact
    validation: CircuitValidation
