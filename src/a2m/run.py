"""Run one system on one task and write a self-contained run directory."""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from a2m import config
from a2m.baselines.central_planner import CentralPlanner, PlannerConfig
from a2m.baselines.single_agent import SingleAgent, SingleAgentConfig
from a2m.llm.client import LLM, Budget
from a2m.sandbox import Sandbox, SandboxError
from a2m.schema import Submission
from a2m.swarm.colonies import Colonies, ColoniesConfig
from a2m.swarm.runtime import Swarm, SwarmConfig
from a2m.tasks import load_card
from a2m.workspace import Workspace

SYSTEMS = {
    "swarm": (Swarm, SwarmConfig),
    "single_agent": (SingleAgent, SingleAgentConfig),
    "central_planner": (CentralPlanner, PlannerConfig),
    "colonies": (Colonies, ColoniesConfig),
}
CONFIG_DIR = Path("configs")


def load_defaults() -> dict[str, Any]:
    return yaml.safe_load((CONFIG_DIR / "default.yaml").read_text())


def load_system(variant: str) -> dict[str, Any]:
    path = CONFIG_DIR / "systems" / f"{variant}.yaml"
    if not path.exists():
        known = sorted(p.stem for p in (CONFIG_DIR / "systems").glob("*.yaml"))
        raise SystemExit(f"unknown system {variant!r}; known: {', '.join(known)}")
    return yaml.safe_load(path.read_text())


def make_sandbox(defaults: dict, profile: str | None, require_isolation: bool) -> Sandbox:
    sb = defaults.get("sandbox", {})
    sandbox = Sandbox(profile=profile or sb.get("profile", "auto"), timeout_s=sb.get("timeout_s", 90))
    if require_isolation and sandbox.profile == "none":
        raise SandboxError("isolation required but bubblewrap is unavailable; refusing to run")
    return sandbox


def run(variant: str, task_id: str, seed: int = 0, llm_mode: str = "anthropic",
        budget_usd: float | None = None, verbose: bool = True, sandbox_profile: str | None = None,
        require_isolation: bool = False) -> Path:
    defaults = load_defaults()
    sys_cfg = load_system(variant)
    cls, cfg_cls = SYSTEMS[sys_cfg["system"]]
    cfg = cfg_cls.from_dict({k: v for k, v in sys_cfg.items() if k != "system"})
    card = load_card(task_id)
    b = defaults.get("budget", {})
    budget = Budget(budget_usd if budget_usd is not None else b.get("max_usd", 2.0),
                    b.get("max_tokens"))
    models = set(cfg.models) | ({cfg.planner_model} if hasattr(cfg, "planner_model") else set())
    llms = {m: LLM(m, budget, llm_mode, effort=defaults.get("effort", "medium"), mock_seed=seed)
            for m in sorted(models)}
    sandbox = make_sandbox(defaults, sandbox_profile, require_isolation)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{task_id}__{variant}__s{seed}__{stamp}"
    run_dir = config.runs_dir() / task_id / variant / run_id
    ws = Workspace(card, sandbox, budget, run_dir, verbose=verbose)
    ws.log("run_start", run_id=run_id, system=variant, llm=llm_mode, sandbox=sandbox.profile,
           budget_usd=budget.max_usd)
    t0 = time.time()
    system = cls(ws, llms, cfg, seed)
    chosen = system.run()
    wall = time.time() - t0

    usage = {**budget.snapshot(), "wall_seconds": round(wall, 1),
             "sandbox_seconds": round(sandbox.seconds_used, 1),
             "sandbox_executions": sandbox.executions}
    sub = Submission(run_id=run_id, task_id=task_id, system=variant, seed=seed,
                     config={"system": sys_cfg, "defaults": defaults, "llm": llm_mode},
                     candidates=chosen, usage=usage, isolation=sandbox.profile,
                     stats={"candidates_total": len(ws.candidates),
                            "families": ws.families(), **system.stats()})
    (run_dir / "submission.json").write_text(sub.model_dump_json(indent=2))
    (run_dir / "all_candidates.json").write_text(json.dumps(
        [c.model_dump() for c in ws.candidates.values()], indent=2))
    ws.log("run_end", submitted=",".join(c.id for c in chosen), usd=round(budget.usd, 4),
           wall_s=round(wall, 1))
    ws.close()
    latest = config.runs_dir() / "latest"
    if latest.is_symlink() or latest.exists():
        latest.unlink()
    latest.symlink_to(run_dir.resolve())
    return run_dir
