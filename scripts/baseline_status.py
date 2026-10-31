"""One-line status for a run-pipeline summary. Usage: baseline_status.py SUMMARY_JSON EXIT_CODE"""

import json
import sys
from pathlib import Path

path, code = sys.argv[1], sys.argv[2]
try:
    summary = json.loads(Path(path).read_text(encoding="utf-8"))
except (OSError, ValueError):
    print(f"error (exit {code}, no summary; see log)")
    raise SystemExit

stage = summary.get("stopped_at")
if stage is None:
    sim = summary["simulation"]
    if sim["status"] == "simulated":  # no reference, so nothing to pass
        print(f"ok simulated ({sim['cases_run']} cases)")
    else:
        print(f"ok {sim['status']} ({sim['cases_passed']}/{sim['cases_run']} cases)")
elif stage == "equations":
    print(f"stopped at equations: {summary['equations']['status']}")
elif stage == "code":
    print(f"stopped at code: {summary['code']['status']}")
elif stage == "validation":
    print(f"stopped at validation: {summary['code']['validation_status']}")
elif stage == "simulation":
    print(f"stopped at simulation: {summary['simulation']['status']}")
else:
    print(f"error (exit {code}): {summary.get('error', 'see log')[:80]}")
