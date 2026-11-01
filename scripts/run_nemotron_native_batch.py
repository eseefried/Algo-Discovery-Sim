"""Resumable native-LaTeX Nemotron -> shared Sonnet/high -> Docker/Aer batch.

The USD limit is estimated from recorded token usage using the repo's model rates.
It is checked before each paid call; one in-flight call can overshoot the limit.
"""

import argparse
import json
import math
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import httpx

from a2m.llm.client import Budget
from algo_discovery.code_sim_cli import run as code_sim
from algo_discovery.config import Settings
from algo_discovery.nemotron_equations import external_spec


def spend(out):
    budget = Budget(None)
    for file in (out / "results").glob("*/result.json"):
        result = json.loads(file.read_text())
        if result.get("stage") != "equations_to_qiskit":
            continue
        usage = result["usage"]
        budget.charge(result["model"],
                      usage["input_tokens"] + usage.get("cache_creation_input_tokens", 0),
                      usage["output_tokens"], usage.get("cache_read_input_tokens", 0))
    return budget.usd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids-dir", type=Path, default=Path("single_agent_specs"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/nemotron_native_full"))
    parser.add_argument("--max-usd", type=float, default=10, help="Estimated total code spend; one-call possible overshoot")
    parser.add_argument("--limit", type=int, help="Optional small pilot subset")
    args = parser.parse_args()
    if not math.isfinite(args.max_usd) or args.max_usd <= 0:
        parser.error("--max-usd must be positive and finite")
    ids = sorted(p.stem for p in args.ids_dir.glob("*.json"))
    if args.limit is not None:
        if args.limit < 1:
            parser.error("--limit must be positive")
        ids = ids[:args.limit]
    if not ids:
        parser.error("No paper IDs found")
    out = args.out
    for name in ("native", "specs", "logs", "native_logs", "results"):
        (out / name).mkdir(parents=True, exist_ok=True)
    plan = {"system": "native_nemotron_single_equation_generator", "papers": ids,
            "model": "nemotron-quantum", "repetition_penalty": 1.12,
            "max_blocks": 1, "max_output_tokens": 2048,
            "code_model": "claude-sonnet-5-5", "code_effort": "high", "code_max_tokens": 16384,
            "conversion": "Predicted equations retained as unverified assumptions; no generated registers or steps",
            "spend_policy": "Repo token-price estimate; checked before call; one-call overshoot possible"}
    plan_path = out / "plan.json"
    if plan_path.exists() and json.loads(plan_path.read_text()) != plan:
        parser.error("Output directory has a different experiment plan; use a new directory")
    plan_path.write_text(json.dumps(plan, indent=2))
    settings = replace(Settings.from_env(backend="anthropic", model="claude-sonnet-5-5"),
                       effort="high", max_tokens=16384, artifact_dir=out / "results")
    for index, paper in enumerate(ids, 1):
        done = out / "logs" / f"{paper}.done"
        if done.exists():
            print(f"[{index}/{len(ids)}] {paper}: already finished", flush=True)
            continue
        spent = spend(out)
        if spent >= args.max_usd:
            print(f"Stopped: estimated code spend ${spent:.4f} reached ${args.max_usd:.2f}. Resume with a larger --max-usd.", flush=True)
            return 3
        # Stop on infrastructure failure rather than marking the remaining papers failed.
        try:
            response = httpx.get("http://127.0.0.1:8000/v1/models", timeout=10)
            response.raise_for_status()
            if not any(m["id"] == "nemotron-quantum" for m in response.json()["data"]):
                raise ValueError("Nemotron model alias unavailable")
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            print(f"Local server unavailable ({type(exc).__name__}); restart it and rerun this command.", flush=True)
            return 1
        native = out / "native" / paper
        print(f"[{index}/{len(ids)}] {paper}: Nemotron equations; estimated code spend ${spent:.4f}", flush=True)
        if (native / "result.json").exists():
            previous = json.loads((native / "result.json").read_text())
            if previous.get("failure_stage") == "transport":
                native.rename(native.with_name(paper + ".transport-error-" + str(uuid4())[:8]))
        if not (native / "result.json").exists():
            if native.exists():
                native.rename(native.with_name(paper + ".interrupted-" + str(uuid4())[:8]))
            command = [sys.executable, "-u", "-m", "algo_discovery.nemotron_equations",
                       "--abstract-file", f"data/circuit_dataset_300_v1/abstracts/arxiv-{paper}.txt",
                       "--out", str(native), "--max-blocks", "1", "--max-output-tokens", "2048",
                       "--repetition-penalty", "1.12"]
            with (out / "native_logs" / f"{paper}.log").open("w") as log:
                completed = subprocess.run(command, check=False, stdout=log, stderr=subprocess.STDOUT)
            if not (native / "result.json").exists():
                print(f"Native process failed (exit {completed.returncode}); see {log.name}. Resume after fixing.", flush=True)
                return 1
        prediction = json.loads((native / "result.json").read_text())
        summary = {"arxiv_id": paper, "native_result": str(native / "result.json")}
        if prediction["status"] == "failed":
            if prediction.get("failure_stage") == "transport":
                print("Native transport failure; stopped for review. Saved response retained.", flush=True)
                return 1
            summary.update(stopped_at="equations", equations={"status": "native_generation_failed", "error": prediction.get("error")})
        else:
            spec = out / "specs" / f"{paper}.json"
            spec.write_text(external_spec(prediction).model_dump_json(indent=2) + "\n")
            stage_args = SimpleNamespace(spec=spec, source=None, arxiv_id=paper,
                                         instance_file=None, reference="none", inputs=None,
                                         shots=1024, seed=42)
            print(f"[{index}/{len(ids)}] {paper}: Sonnet/high code + Docker/Aer", flush=True)
            try:
                code_sim(stage_args, settings, summary)
            except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
                summary.update(stopped_at="error", error=f"{type(exc).__name__}: {str(exc)[:300]}")
                (out / "logs" / f"{paper}.json").write_text(json.dumps(summary, indent=2))
                print("Code-stage error; stopped for review because unreported API usage may exist. See saved log.", flush=True)
                return 1
        summary["estimated_total_code_usd"] = round(spend(out), 6)
        (out / "logs" / f"{paper}.json").write_text(json.dumps(summary, indent=2))
        done.touch()
        print(f"[{index}/{len(ids)}] {paper}: stopped_at={summary.get('stopped_at')} simulation={summary.get('simulation', {}).get('status')} estimated total=${summary['estimated_total_code_usd']:.4f}", flush=True)
    print(f"Finished {len(ids)} papers. Estimated code spend: ${spend(out):.4f}. Results: {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
