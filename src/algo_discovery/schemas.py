"""Versioned contract for the abstract-to-equation block."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EquationRequest(StrictModel):
    abstract: str = Field(min_length=20, max_length=30000)
    experiment_scope: str | None = Field(default=None, min_length=1, max_length=3000)


class Symbol(StrictModel):
    symbol: str = Field(min_length=1, description="Symbol in LaTeX, without math delimiters")
    meaning: str = Field(min_length=1)
    domain: str = Field(min_length=1)


class Equation(StrictModel):
    id: str = Field(min_length=1, description="Unique equation identifier, e.g. eq_1")
    label: str = Field(min_length=1)
    latex: str = Field(min_length=1, description="LaTeX expression without dollar delimiters")
    description: str = Field(min_length=1)
    provenance: Literal[
        "abstract_explicit", "abstract_inferred", "standard_background", "assumption"
    ]
    abstract_quote: str | None = Field(
        description="Exact supporting substring of abstract for abstract provenance; otherwise null"
    )
    justification: str = Field(min_length=1, description="Concise basis for this equation")
    assumptions: list[str]

    @model_validator(mode="after")
    def check_provenance(self):
        from_abstract = self.provenance in {"abstract_explicit", "abstract_inferred"}
        if from_abstract and not self.abstract_quote:
            raise ValueError("Abstract provenance requires an exact supporting quote.")
        if not from_abstract and self.abstract_quote is not None:
            raise ValueError("Background and assumption equations cannot claim abstract evidence.")
        if self.provenance == "assumption" and not self.assumptions:
            raise ValueError("Assumed equations must state their assumptions.")
        return self


class Register(StrictModel):
    name: str = Field(min_length=1)
    size: str = Field(
        min_length=1, description="Number of qubits or a symbolic size; unknown if absent"
    )
    role: str = Field(min_length=1)


class AlgorithmStep(StrictModel):
    description: str = Field(min_length=1)
    equation_ids: list[str]


class MathSpecification(StrictModel):
    status: Literal["specified", "partial", "insufficient_information", "not_applicable"]
    problem: str = Field(min_length=1)
    reconstruction_scope: str = Field(min_length=1)
    symbols: list[Symbol]
    equations: list[Equation]
    registers: list[Register]
    initial_state: str | None
    steps: list[AlgorithmStep]
    measurement: str | None
    classical_postprocessing: str | None
    assumptions: list[str]
    missing_information: list[str]

    @model_validator(mode="after")
    def check_consistency(self):
        ids = [equation.id for equation in self.equations]
        if len(set(ids)) != len(ids):
            raise ValueError("Equation IDs must be unique.")
        for step in self.steps:
            if not set(step.equation_ids).issubset(ids):
                raise ValueError("Algorithm steps refer to unknown equation IDs.")
        if self.status in {"specified", "partial"} and not self.equations:
            raise ValueError("Specified and partial results require at least one equation.")
        if self.status == "specified" and (
            self.missing_information
            or self.assumptions
            or any(e.assumptions or e.provenance == "assumption" for e in self.equations)
        ):
            raise ValueError(
                "Use partial when reconstruction requires assumptions or missing details."
            )
        if self.status == "insufficient_information" and not self.missing_information:
            raise ValueError("Insufficient information must identify missing details.")
        return self

    def validate_evidence(self, abstract: str) -> None:
        for equation in self.equations:
            if equation.abstract_quote is not None and equation.abstract_quote not in abstract:
                raise ValueError(f"Equation {equation.id} quotes text absent from the abstract.")


class Usage(StrictModel):
    input_tokens: int
    output_tokens: int
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


class GenerationParameters(StrictModel):
    max_tokens: int
    effort: str
    timeout_seconds: float


class EquationResult(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    run_id: str
    created_at: str
    model: str
    response_model: str
    prompt_version: str
    prompt_sha256: str
    abstract_sha256: str
    request_sha256: str
    elapsed_seconds: float
    usage: Usage
    stop_reason: str
    # Early v1 artifacts predate explicit generation settings.
    parameters: GenerationParameters | None = None
    mathematics_verified: Literal[False] = False
    specification: MathSpecification
