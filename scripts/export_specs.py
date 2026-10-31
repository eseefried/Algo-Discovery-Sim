"""Export single-agent equation runs as spec files for run_code_sim.sh.

Usage: python scripts/export_specs.py [RESULTS_DIR] [OUT_DIR]
Writes OUT_DIR/<arxiv_id>.json in the same format the swarm must produce, so both
paths can go through identical code generation and simulation.
"""

import json
import sys
from pathlib import Path

from algo_discovery.external_spec import from_equation_run

results = Path(sys.argv[1] if len(sys.argv) > 1 else "baseline_results")
out = Path(sys.argv[2] if len(sys.argv) > 2 else "single_agent_specs")
out.mkdir(parents=True, exist_ok=True)
exported = 0
for log in sorted((results / "logs").glob("*.json")):
    text = log.read_text(encoding="utf-8").strip()
    artifacts = json.loads(text).get("equations", {}).get("artifacts") if text else None
    if not artifacts or not Path(artifacts, "result.json").exists():
        continue
    spec = from_equation_run(Path(artifacts, "result.json"), arxiv_id=log.stem)
    (out / f"{log.stem}.json").write_text(spec.model_dump_json(indent=2) + "\n", encoding="utf-8")
    exported += 1
print(f"Exported {exported} specs to {out}/")
