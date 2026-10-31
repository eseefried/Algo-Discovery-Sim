"""Data contracts. The visible side (ClaimCard) and sealed side (Vault) never mix."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskRecord(BaseModel):
    """One line of the dataset manifest. Unknown fields are preserved verbatim."""

    model_config = ConfigDict(extra="allow")

    id: str
    arxiv_id: str
    title: str
    source_url: str
    family: str
    suggested_order: int = 0
    selection_reason: str = ""
    proposed_simulation: dict[str, Any] = Field(default_factory=dict)
    files: dict[str, str] = Field(default_factory=dict)
    status: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------- visible side


class Criterion(BaseModel):
    """One measurable part of the claim, e.g. success_rate >= 1.0."""

    metric: str
    comparator: Literal[">=", "<=", "=="]
    target: float
    tolerance: float = 0.0
    scale: float = 1.0  # normalises the gap; violation of `scale` counts as a full miss


class TestSystem(BaseModel):
    name: str
    params: dict[str, Any]


class ClaimCard(BaseModel):
    """Everything a reconstruction system is allowed to see about a task."""

    task_id: str
    domain: Literal["quantum", "chemistry", "materials", "protein"] = "quantum"
    evaluator: str
    abstract: str
    claim: str
    criteria: list[Criterion]
    interface: str
    test_systems: list[TestSystem]
    qubit_cap: int
    allowed_imports: list[str]
    curation_status: Literal["curated", "draft"] = "draft"
    notes: str = ""


# ----------------------------------------------------------------- sealed side


class RubricItem(BaseModel):
    id: str
    text: str
    weight: float = 1.0
    keywords: list[str] = Field(default_factory=list)  # cheap lexical signal, never the verdict


class Vault(BaseModel):
    task_id: str
    rubric: list[RubricItem]
    hidden_test_systems: list[TestSystem]
    reported_numbers: dict[str, Any]
    reference_file: str = "reference.py"
    reference_family: str
    provenance: str = ""


# -------------------------------------------------------------- run artifacts


class Candidate(BaseModel):
    id: str
    parent: str | None = None
    family: str
    sketch: str
    code: str = ""
    chain: list[tuple[str, str]] = Field(default_factory=list)  # (agent_id, role), oldest first
    gap: float = 1.0
    results: dict[str, dict[str, Any]] = Field(default_factory=dict)
    status: Literal["sketch", "implemented", "failing", "passing", "ready", "broken"] = "sketch"
    critiques: list[dict[str, Any]] = Field(default_factory=list)
    attempts: int = 0  # implementation attempts along this lineage


class Submission(BaseModel):
    run_id: str
    task_id: str
    system: str
    seed: int
    config: dict[str, Any]
    candidates: list[Candidate]  # ranked by the system itself; the first is its answer
    usage: dict[str, Any]
    isolation: str
    stats: dict[str, Any] = Field(default_factory=dict)


class JudgeReport(BaseModel):
    run_id: str
    task_id: str
    system: str
    seed: int
    candidate_id: str | None
    claim_reproduced: bool
    method_match: float
    method_recovered: bool
    any_method_recovered: bool = False  # best of the submitted candidates (at most 3)
    valid_alternative: bool
    structural_similarity: float
    loopholes: list[str]
    human_review: list[str]
    rubric_scores: dict[str, dict[str, float]]
    candidate_numbers: dict[str, dict[str, Any]]
    reference_numbers: dict[str, dict[str, Any]]
    paper_numbers: dict[str, Any]
    usage: dict[str, Any]
    all_candidates: list[dict[str, Any]] = Field(default_factory=list)
