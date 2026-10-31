"""Aggregate judge reports into a comparison table across systems."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


def collect(runs_dir: Path) -> list[dict]:
    out = []
    for p in sorted(Path(runs_dir).rglob("judge.json")):
        if "latest" in p.parts:
            continue
        r = json.loads(p.read_text())
        sub = json.loads((p.parent / "submission.json").read_text())
        out.append({
            "task": r["task_id"], "system": r["system"], "seed": r["seed"], "run_id": r["run_id"],
            "llm": sub["config"].get("llm", "?"),
            "claim_reproduced": r["claim_reproduced"], "method_recovered": r["method_recovered"],
            "any_recovered": r.get("any_method_recovered", False),
            "valid_alternative": r["valid_alternative"], "method_match": r["method_match"],
            "structural": r["structural_similarity"], "usd": r["usage"].get("usd", 0.0),
            "calls": r["usage"].get("calls", 0), "wall_s": r["usage"].get("wall_seconds", 0.0),
            "deaths": sub["stats"].get("deaths", ""),
            "colony_deaths": sub["stats"].get("colony_deaths", ""),
            "candidates": sub["stats"].get("candidates_total", 0),
        })
    return out


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["llm"], r["system"])].append(r)
    table = []
    for (llm, system), rs in sorted(groups.items()):
        table.append({
            "llm": llm, "system": system, "runs": len(rs), "tasks": len({r["task"] for r in rs}),
            "claim_reproduced": mean(r["claim_reproduced"] for r in rs),
            "method_recovered": mean(r["method_recovered"] for r in rs),
            "any_recovered": mean(r["any_recovered"] for r in rs),
            "valid_alternative": mean(r["valid_alternative"] for r in rs),
            "method_match": mean(r["method_match"] for r in rs),
            "usd_per_run": mean(r["usd"] for r in rs),
            "usd_per_reproduction": (sum(r["usd"] for r in rs)
                                     / max(1, sum(r["claim_reproduced"] for r in rs))),
            "wall_s": mean(r["wall_s"] for r in rs),
        })
    return table


def write(runs_dir: Path, out_dir: Path) -> Path:
    rows = collect(runs_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(out_dir / "runs.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    table = summarize(rows)
    lines = ["# Abstract2Method results", "",
             ("Rates are over runs (task x seed). Mock-LLM rows test the harness only; "
              "they are not results."), "",
             ("| llm | system | runs | tasks | claim reproduced | method recovered | "
              "recovered in top 3 | valid alternative | method match | $/run | $/reproduction "
              "| wall s |"),
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in table:
        lines.append(
            f"| {t['llm']} | {t['system']} | {t['runs']} | {t['tasks']} | "
            f"{t['claim_reproduced']:.0%} | {t['method_recovered']:.0%} | "
            f"{t['any_recovered']:.0%} | "
            f"{t['valid_alternative']:.0%} | {t['method_match']:.2f} | {t['usd_per_run']:.3f} | "
            f"{t['usd_per_reproduction']:.3f} | {t['wall_s']:.0f} |")
    path = out_dir / "summary.md"
    path.write_text("\n".join(lines) + "\n")
    return path
