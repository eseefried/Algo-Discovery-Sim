"""Task loading. `load_card` is the visible side; `load_vault` is judge-only."""

from __future__ import annotations

import json
from pathlib import Path

from a2m import config
from a2m.schema import ClaimCard, TaskRecord, Vault


def load_manifest(path: Path | None = None) -> list[TaskRecord]:
    path = path or config.dataset_dir() / "manifest.jsonl"
    recs = [TaskRecord.model_validate(json.loads(line))
            for line in path.read_text().splitlines() if line.strip()]
    return sorted(recs, key=lambda r: (r.suggested_order or 10**6, r.id))


def ready_task_ids() -> list[str]:
    """Tasks with a curated claim card and a sealed vault."""
    ids = []
    for p in sorted(config.tasks_dir().glob("*.json")):
        card = ClaimCard.model_validate_json(p.read_text())
        if card.curation_status == "curated" and (config.vault_dir() / card.task_id).is_dir():
            ids.append(card.task_id)
    return ids


def load_card(task_id: str) -> ClaimCard:
    return ClaimCard.model_validate_json((config.tasks_dir() / f"{task_id}.json").read_text())


def load_vault(task_id: str) -> tuple[Vault, str]:
    d = config.vault_dir() / task_id
    vault = Vault.model_validate_json((d / "vault.json").read_text())
    return vault, (d / vault.reference_file).read_text()
