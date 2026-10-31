"""The domain adapter: ledger contributions become the existing ExternalSpec contract."""

import json

from ..schemas import EquationRequest, MathSpecification
from .ledger import Ledger
from .models import (
    FIELDS,
    PENDING_EQUATIONS,
    PREREQUISITES,
    REQUIREMENTS,
    Contribution,
    Genotype,
)


def assemble(ledger: Ledger, root_id: str) -> dict:
    payload = json.loads(ledger.root(root_id)["payload"])
    current = {
        "status": "insufficient_information",
        "problem": "Reconstruct the supplied abstract.",
        "reconstruction_scope": payload.get("experiment_scope")
        or "Small finite circuit experiment.",
        "symbols": [],
        "equations": [],
        "registers": [],
        "initial_state": None,
        "steps": [],
        "measurement": None,
        "classical_postprocessing": None,
        "assumptions": [],
        "missing_information": [],
    }
    tasks = sorted(
        (task for task in ledger.tasks(root_id) if task["status"] == "Completed"),
        key=lambda task: (task["updated"], task["id"]),
    )
    for task in tasks:
        result = json.loads(task["result"])
        candidate = result["specification"]
        if "audit" not in result["completed_requirements"]:
            for field in ["assumptions", "missing_information"]:
                current[field] = list(dict.fromkeys(current[field] + candidate[field]))
        for part in result["completed_requirements"]:
            for field in FIELDS[part]:
                current[field] = candidate[field]
        if "audit" not in result["completed_requirements"]:
            current["status"] = "partial" if current["equations"] else "insufficient_information"
    current["missing_information"] = [
        item for item in current["missing_information"] if item != PENDING_EQUATIONS
    ]
    return current


def context(ledger: Ledger, task: dict, genotype: Genotype) -> dict:
    root = ledger.root(task["root_id"])
    payload = json.loads(root["payload"])
    completed = {
        part
        for t in ledger.tasks(task["root_id"])
        if t["status"] == "Completed"
        for part in json.loads(t["result"])["completed_requirements"]
    }
    return {
        "abstract": payload["abstract"],
        "experiment_scope": payload.get("experiment_scope"),
        "task_id": task["id"],
        "requirements": json.loads(task["requirements"]),
        "attempts": task["attempts"],
        "already_completed": sorted(completed),
        "requirements_elsewhere": sorted(
            set(REQUIREMENTS) - completed - set(json.loads(task["requirements"]))
        ),
        "suggested_requirements": planned_parts(task, completed, genotype),
        "current_specification": assemble(ledger, task["root_id"]),
        "max_parts": genotype.max_parts,
        "capabilities": genotype.preferences,
    }


def planned_parts(task: dict, completed: set[str], genotype: Genotype) -> list[str]:
    remaining = set(json.loads(task["requirements"]))
    chosen = []
    while remaining and len(chosen) < genotype.max_parts:
        ready = [p for p in remaining if PREREQUISITES[p] <= completed | set(chosen)]
        if not ready:
            break
        part = max(ready, key=lambda p: (genotype.preferences.get(p, 0.1), -REQUIREMENTS.index(p)))
        chosen.append(part)
        remaining.remove(part)
    return chosen


def proposal(ledger: Ledger, task: dict, agent: dict) -> tuple[int, float] | None:
    genotype = Genotype.model_validate_json(agent["genotype"])
    completed = {
        p
        for t in ledger.tasks(task["root_id"])
        if t["status"] == "Completed"
        for p in json.loads(t["result"])["completed_requirements"]
    }
    chosen = planned_parts(task, completed, genotype)
    if not chosen:
        return None
    confidence = sum(genotype.preferences.get(p, 0.1) for p in chosen) / len(chosen)
    available = agent["balance"] - agent["reserved"]
    if available < 1:
        return None
    # Cap exposure at the initial capital; rewards do not let a rich generalist monopolize every task.
    amount = max(1, int(min(available, 10000) * genotype.bid_fraction * confidence))
    return min(amount, available), confidence


def check_contribution(result: Contribution, ctx: dict, genotype: Genotype):
    solved = result.completed_requirements
    if not 1 <= len(solved) <= genotype.max_parts or len(set(solved)) != len(solved):
        raise ValueError("Contribution exceeds its progress limit or repeats a requirement.")
    if not set(solved) <= set(ctx["requirements"]):
        raise ValueError("Contribution claims work outside its contract.")
    done = set(ctx["already_completed"]) | set(solved)
    if any(not PREREQUISITES[p] <= done for p in solved):
        raise ValueError("Contribution skips prerequisite work.")
    remaining = sorted(set(ctx["requirements"]) - set(solved))
    children = [p for group in result.child_groups for p in group]
    if any(not group for group in result.child_groups) or sorted(children) != remaining:
        raise ValueError("Child groups must partition the remaining contract exactly once.")
    result.specification.validate_evidence(ctx["abstract"])
    if "audit" in solved:
        changed = any(
            result.specification.model_dump()[field] != ctx["current_specification"][field]
            for part in REQUIREMENTS
            if part != "audit"
            for field in FIELDS[part]
        )
        if changed and not result.changes:
            raise ValueError("Audit changes to earlier work require a provenance explanation.")


def final_specification(ledger: Ledger, root_id: str) -> MathSpecification:
    if ledger.root(root_id)["status"] != "completed":
        raise ValueError("The whole task tree has not completed.")
    spec = MathSpecification.model_validate(assemble(ledger, root_id))
    payload = json.loads(ledger.root(root_id)["payload"])
    request = EquationRequest(
        abstract=payload["abstract"], experiment_scope=payload.get("experiment_scope")
    )
    spec.validate_evidence(request.abstract)
    return spec
