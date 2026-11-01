"""Export completed hybrid-swarm runs as portable CSVs and linked evidence."""

import argparse
import csv
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def write_csv(path, rows, fields):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def export(batch, out, repo):
    out.mkdir(parents=True, exist_ok=True)
    tables = {name: [] for name in ("runs", "agents", "events", "candidates", "probabilities")}
    for marker in sorted((batch / "logs").glob("*.done")):
        summary = json.loads(marker.with_suffix(".json").read_text())
        source = Path(summary["directory"])
        if not source.is_absolute():
            source = repo / source
        run_id, paper = source.name, summary["paper"]
        dest = out / "artifacts" / paper / run_id
        dest.mkdir(parents=True, exist_ok=True)

        # Copy evidence, not environment/configuration files or credentials.
        for name in ("summary.json", "events.jsonl", "all_candidates.json",
                     "selected_spec.json", "native_evidence.json"):
            if (source / name).exists():
                shutil.copy2(source / name, dest / name)
        for subdir, names in (
            ("blackbox", {"circuit.py", "compiled.qasm", "instance.json", "result.json",
                          "validation.json", "implementation.md", "equations.md"}),
            ("native", {"response.txt", "equations.txt"}),
            ("candidates", None),
        ):
            for file in (source / subdir).rglob("*"):
                if file.is_file() and (names is None or file.name in names):
                    target = dest / file.relative_to(source)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, target)
        abstract = repo / "data/circuit_dataset_300_v1/abstracts" / f"arxiv-{paper}.txt"
        if abstract.exists():
            shutil.copy2(abstract, dest / "abstract.txt")

        def link(relative):
            file = dest / relative
            return file.relative_to(out).as_posix() if file.exists() else ""

        records = [json.loads(line) for line in (source / "events.jsonl").read_text().splitlines() if line.strip()]
        candidates = json.loads((source / "all_candidates.json").read_text())
        by_candidate = {c["id"]: c for c in candidates}
        for candidate in candidates:
            snapshot = dest / "candidates" / f"{candidate['id']}.json"
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(json.dumps(candidate, indent=2))
        deaths = {d["agent_id"]: d for d in summary["swarm"]["lineage"]["deaths"]}
        agent_records = {}
        for record in records:
            aid = record.get("who", record.get("agent", ""))
            if aid:
                agent_records.setdefault(aid, []).append(record)

        def candidate_links(cid):
            candidate = by_candidate.get(cid, {})
            result = candidate.get("results", {}).get("spec", {})
            code_id = result.get("code_run_id", "")
            base = f"blackbox/{code_id}"
            return {
                "candidate_artifact": link(f"candidates/{cid}.json"),
                "code_artifact": link(f"{base}/circuit.py"),
                "qasm_artifact": link(f"{base}/compiled.qasm"),
                "instance_artifact": link(f"{base}/instance.json"),
                "validation_artifact": link(f"{base}/validation.json"),
            }

        tables["runs"].append({
            "run_id": run_id, "paper_id": paper, "status": summary["status"],
            "selected_candidate_key": f"{run_id}:{summary['selected_candidate']}" if summary.get("selected_candidate") else "",
            "wall_seconds": summary["wall_seconds"], "estimated_api_usd": summary["paid_budget"]["usd"],
            "agents_created": len(summary["swarm"]["agents"]),
            "deaths": summary["swarm"]["deaths"], "replacements": summary["swarm"]["respawns"],
            "abstract_artifact": link("abstract.txt"), "summary_artifact": link("summary.json"),
            "events_artifact": link("events.jsonl"),
        })
        for agent in summary["swarm"]["agents"]:
            aid = agent["id"]
            history = agent_records.get(aid, [])
            birth = next((r for r in history if r["kind"] == "genotype"), {})
            death = next((r for r in history if r["kind"] == "death"), {})
            # Preserve the last recorded activity before death, without inventing causality.
            before_death = history[:history.index(death)] if death else history
            activity = next((r for r in reversed(before_death) if r["kind"] not in {"genotype", "respawn", "spawn"}), {})
            cid = activity.get("cand", "")
            if not cid:
                cid = next((r["cand"] for r in reversed(before_death) if r.get("cand")), "")
            tables["agents"].append({
                "agent_key": f"{run_id}:{aid}", "run_id": run_id, "paper_id": paper, "agent_id": aid,
                "generation": agent["generation"],
                "parent_agent_key": f"{run_id}:{agent['parent']}" if agent.get("parent") else "",
                "state_at_run_end": "alive" if agent["alive"] else "dead",
                "born_seconds": birth.get("t", ""), "born_tick": agent.get("born_tick", ""),
                "death_seconds": death.get("t", ""), "death_tick": death.get("tick", ""),
                "death_trigger": "virtual_energy_depleted" if death else "",
                "recorded_failure_context": deaths.get(aid, {}).get("reason", death.get("reason", "")),
                "last_activity": activity.get("action", activity.get("kind", "")),
                "last_candidate_key": f"{run_id}:{cid}" if cid else "",
                "final_energy": agent["energy"], "earned_energy": agent["earned"], "spent_energy": agent["spent"],
                "roles_json": compact(agent.get("roles", {})), "profile_json": compact(birth.get("profile", {})),
                "event_count": len(history), "summary_artifact": link("summary.json"),
            })
        for sequence, record in enumerate(records):
            aid = record.get("who", record.get("agent", ""))
            cid = record.get("cand", "")
            tables["events"].append({
                "event_key": f"{run_id}:e{sequence:04d}", "run_id": run_id, "paper_id": paper,
                "sequence": sequence, "elapsed_seconds": record["t"], "tick": record["tick"],
                "agent_key": f"{run_id}:{aid}" if aid else "", "agent_id": aid,
                "kind": record["kind"], "action": record.get("action", ""),
                "candidate_key": f"{run_id}:{cid}" if cid else "", "candidate_id": cid,
                "provider": record.get("provider", ""), "status": record.get("status", ""),
                "reason": record.get("reason", record.get("error", "")),
                **candidate_links(cid), "details_json": compact(record),
            })
        for candidate in candidates:
            cid = candidate["id"]
            result = candidate.get("results", {}).get("spec", {})
            simulation = result.get("simulation", "")
            distributions = []
            simulation_parse_status = "not_recorded"
            if simulation:
                try:
                    distributions = json.loads(simulation) if isinstance(simulation, str) else simulation
                    simulation_parse_status = "complete"
                except json.JSONDecodeError:
                    # The runner saves some previews truncated at 600 characters.
                    # Keep the exact preview; do not fabricate missing probabilities.
                    simulation_parse_status = "unparseable_saved_preview"
            tables["candidates"].append({
                "candidate_key": f"{run_id}:{cid}", "run_id": run_id, "paper_id": paper, "candidate_id": cid,
                "parent_candidate_key": f"{run_id}:{candidate['parent']}" if candidate.get("parent") in by_candidate else "",
                "family": candidate.get("family", ""), "status": candidate["status"],
                "selected": cid == summary.get("selected_candidate"),
                "attempts": candidate.get("attempts", ""), "method_description": candidate.get("sketch", ""),
                "contributors_json": compact([{"agent_key": f"{run_id}:{aid}", "role": role}
                                              for aid, role in candidate.get("chain", [])]),
                "simulation_detail": result.get("detail", ""), "instance_json": compact(result.get("instance", {})),
                "simulation_json": simulation, "simulation_parse_status": simulation_parse_status,
                "reviews_json": compact(candidate.get("critiques", [])),
                **candidate_links(cid),
            })
            if simulation_parse_status == "complete":
                for case, distribution in enumerate(distributions):
                    for state, probability in distribution.items():
                        tables["probabilities"].append({
                            "run_id": run_id, "candidate_key": f"{run_id}:{cid}",
                            "case_index": case, "bitstring": state, "probability": probability,
                        })

    schemas = {
        "runs": "run_id paper_id status selected_candidate_key wall_seconds estimated_api_usd agents_created deaths replacements abstract_artifact summary_artifact events_artifact",
        "agents": "agent_key run_id paper_id agent_id generation parent_agent_key state_at_run_end born_seconds born_tick death_seconds death_tick death_trigger recorded_failure_context last_activity last_candidate_key final_energy earned_energy spent_energy roles_json profile_json event_count summary_artifact",
        "events": "event_key run_id paper_id sequence elapsed_seconds tick agent_key agent_id kind action candidate_key candidate_id provider status reason candidate_artifact code_artifact qasm_artifact instance_artifact validation_artifact details_json",
        "candidates": "candidate_key run_id paper_id candidate_id parent_candidate_key family status selected attempts method_description contributors_json simulation_detail instance_json simulation_json simulation_parse_status reviews_json candidate_artifact code_artifact qasm_artifact instance_artifact validation_artifact",
        "probabilities": "run_id candidate_key case_index bitstring probability",
    }
    for name, fields in schemas.items():
        write_csv(out / f"{name}.csv", tables[name], fields.split())
    manifest = {"exported_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_batch": str(batch), "rows": {k: len(v) for k, v in tables.items()},
                "outcomes": dict(Counter(r["status"] for r in tables["runs"]))}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (out / "README.md").write_text("""# Qatalyst visualization data

A snapshot of completed papers from the real Nemotron + Sonnet hybrid swarm.
Start with paper **0710.3196**, selected candidate **c003**, for the Grover demo.
Choose a run with `deaths > 0` in runs.csv to show actual culling and replacement.

- **runs.csv**: run selector, outcomes, spending, population and artifact links.
- **agents.csv**: clickable lobsters, parent links, birth/death times, final energy,
  last recorded activity/candidate and recorded failure context.
- **events.csv**: chronological replay, action details and code/evidence links.
- **candidates.csv**: method cards, complete review feedback, instances and outputs.
- **probabilities.csv**: histogram rows, keyed by candidate and simulation case.

Join agents and events on `agent_key`, and candidates on `candidate_key`.
Agent IDs reset for each paper, so use the global keys, not bare a01/a02 IDs.
Playback uses `elapsed_seconds`, with `sequence` breaking ties. All times are
seconds since that paper run began; ticks are logical rounds, not seconds.
Events without an agent key are run/candidate-level events; do not attribute them
to a lobster. Nested data is JSON inside correctly quoted CSV cells.

All artifact paths are relative to this directory. Host or copy the entire export
folder to preserve click-through links. Python uses build_circuit(instance);
compiled.qasm is also provided where saved. Raw equations live in artifacts/*/*/native/.
Original events and summaries are retained alongside generated code and validation.

`alive` means alive when that run ended, not currently running. Culling means
virtual-energy depletion, not necessarily a process crash. Failure context and
last activity describe recorded history, not an independently proven cause.
Energy is the saved final balance; per-event energy balances were not recorded.
Replacement agents need not have a donor parent when no successful donor exists.
Simulation probabilities are exact saved outputs, not invented shot counts.
Some saved simulation previews are truncated: these are flagged in candidates.csv
and excluded from probabilities.csv, while their original text is preserved.
Successful execution and model review are recorded separately and do not certify
full-paper reproduction. No unfinished run is included in this snapshot.

Candidate/code links show saved final snapshots for that candidate; event details
preserve the recorded activity at that moment. Repeated implementation attempts
may have intermediate artifacts in blackbox/, but not every event records an
exact intermediate code ID.
""")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, default=Path("artifacts/native_swarm_65"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/swarm_viz_export"))
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    print(json.dumps(export(args.batch, args.out, repo), indent=2))


if __name__ == "__main__":
    main()
