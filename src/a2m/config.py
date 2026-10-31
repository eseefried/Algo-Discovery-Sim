"""Paths and credentials. Environment values take precedence over `.env`."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

REPO_DATASET = "data/circuit_dataset_300_v1"
SHARED_DATASET = "/mnt/zgx1-shared/Algo-Discovery-Sim/data/circuit_dataset_300_v1"


def dataset_dir() -> Path:
    """Evaluator-side corpus: manifest, abstracts, papers, equations. Prefers the copy in this
    repository, then the shared mount."""
    if os.getenv("A2M_DATASET_DIR"):
        return Path(os.environ["A2M_DATASET_DIR"])
    return Path(REPO_DATASET) if Path(REPO_DATASET).is_dir() else Path(SHARED_DATASET)


def tasks_dir() -> Path:
    """Visible task material (claim cards). The only task input agents receive."""
    return Path(os.getenv("A2M_TASKS_DIR", "data/tasks"))


def vault_dir() -> Path:
    """Sealed judge material: rubrics, hidden tests, reference implementations."""
    return Path(os.getenv("A2M_VAULT_DIR", "data/vaults"))


def runs_dir() -> Path:
    return Path(os.getenv("A2M_RUNS_DIR", "runs"))


def api_key() -> str | None:
    # Same convention as the team's abstract-to-equations block: the hackathon key wins.
    return os.getenv("CLAUDE_HACKATHON_API") or os.getenv("ANTHROPIC_API_KEY")


def judge_models() -> list[str]:
    raw = os.getenv("A2M_JUDGE_MODELS", "claude-opus-5-5,claude-sonnet-5-5")
    return [m.strip() for m in raw.split(",") if m.strip()]
