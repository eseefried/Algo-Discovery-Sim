"""Run a resumable hybrid swarm on the same completed-paper cohort as a baseline."""

import argparse
import json
import math
import os
import sys
from pathlib import Path

import httpx

from algo_discovery.native_swarm import run


def completed_ids(baseline, limit):
    ids = sorted(p.stem for p in (baseline / "logs").glob("*.done"))
    if len(ids) < limit:
        raise ValueError(f"Baseline has {len(ids)} completed papers; {limit} requested.")
    return ids[:limit]


def total_spend(out):
    # Include every attempt, not just selected/successful candidates.
    return sum(json.loads(p.read_text())["paid_budget"]["usd"]
               for p in (out / "runs").glob("*/*/summary.json"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path("artifacts/nemotron_native_full"))
    parser.add_argument("--limit", type=int, default=65)
    parser.add_argument("--out", type=Path, default=Path("artifacts/native_swarm_65"))
    parser.add_argument("--paper-seconds", type=float, default=180)
    parser.add_argument("--paper-usd", type=float, default=0.30)
    parser.add_argument("--max-usd", type=float, default=10)
    parser.add_argument("--max-calls", type=int, default=24)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    for key in ("limit", "paper_seconds", "paper_usd", "max_usd", "max_calls"):
        value = getattr(args, key)
        if not math.isfinite(value) or value <= 0:
            parser.error(f"{key} must be positive and finite")
    try:
        ids = completed_ids(args.baseline, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    out = args.out
    (out / "logs").mkdir(parents=True, exist_ok=True)
    plan = {"papers": ids, "baseline": str(args.baseline.resolve()),
            "system": "hybrid_native_equation_swarm", "seed": args.seed,
            "paper_seconds": args.paper_seconds, "paper_usd": args.paper_usd,
            "max_calls": args.max_calls,
            "execution_policy": "settle_each_action_prioritize_validation_reserved_reviewer"}
    path = out / "plan.json"
    if path.exists() and json.loads(path.read_text()) != plan:
        parser.error("Different experiment plan in output directory; choose a new output directory.")
    path.write_text(json.dumps(plan, indent=2))
    for index, paper in enumerate(ids, 1):
        done = out / "logs" / f"{paper}.done"
        if done.exists():
            print(f"[{index}/{len(ids)}] {paper}: already finished", flush=True)
            continue
        unfinished = [p for p in (out / "runs" / paper).glob("*")
                      if p.is_dir() and not (p / "summary.json").exists()]
        if unfinished:
            print(f"Interrupted attempt requires review before more paid work: {unfinished[0]}", flush=True)
            return 1
        remaining = args.max_usd - total_spend(out)
        if remaining <= 0:
            print(f"Estimated total spend limit reached: ${total_spend(out):.4f}. Resume with a larger --max-usd.", flush=True)
            return 3
        headers = {"Authorization": "Bearer " + os.environ["NEMOTRON_API_KEY"]} if os.getenv("NEMOTRON_API_KEY") else {}
        try:
            response = httpx.get(os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1").rstrip("/") + "/models", timeout=10, headers=headers)
            response.raise_for_status()
            if not any(m["id"] == "nemotron-quantum" for m in response.json()["data"]):
                raise ValueError("Native model alias missing")
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            print(f"Local model unavailable ({type(exc).__name__}); restart server and rerun.", flush=True)
            return 1
        print(f"[{index}/{len(ids)}] {paper}: swarm; estimated cumulative spend ${total_spend(out):.4f}", flush=True)
        try:
            result = run(paper, out, max_usd=min(args.paper_usd, remaining),
                         max_calls=args.max_calls, max_seconds=args.paper_seconds, seed=args.seed)
        except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
            print(f"Swarm stopped for review: {type(exc).__name__}: {str(exc)[:300]}", flush=True)
            return 1
        (out / "logs" / f"{paper}.json").write_text(json.dumps(result, indent=2))
        done.touch()
        print(f"[{index}/{len(ids)}] {paper}: {result['status']} in {result['wall_seconds']:.1f}s; "
              f"deaths={result['swarm']['deaths']} respawns={result['swarm']['respawns']} "
              f"estimated total=${total_spend(out):.4f}", flush=True)
        summaries = [json.loads(p.read_text()) for p in (out / "logs").glob("*.json")]
        (out / "summary.json").write_text(json.dumps({
            "planned_papers": len(ids), "completed_papers": len(summaries),
            "reviewed_ready": sum(s["status"] == "ready" for s in summaries),
            "estimated_api_usd": round(total_spend(out), 6),
            "fitness": "Execution plus model review, not independent algorithm correctness",
        }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
