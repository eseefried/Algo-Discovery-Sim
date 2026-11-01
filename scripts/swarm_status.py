"""One-line status for a run-swarm summary. Usage: swarm_status.py SUMMARY_JSON EXIT_CODE"""

import json
import sys
from pathlib import Path

path, code = sys.argv[1], sys.argv[2]
try:
    summary = json.loads(Path(path).read_text(encoding="utf-8"))
except (OSError, ValueError):
    print(f"error (exit {code}, no summary; see log)")
    raise SystemExit
line = f"{summary.get('status')} spec={summary.get('specification_status')}"
line += f" tokens={summary.get('input_tokens', 0)}+{summary.get('output_tokens', 0)}"
if summary.get("error"):
    line += f" error={str(summary['error']).splitlines()[0][:80]}"
print(line)
