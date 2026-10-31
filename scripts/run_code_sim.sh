#!/usr/bin/env bash
# Run code generation + simulation for every spec in SPEC_DIR (one <arxiv_id>.json per paper).
# Same output layout as run_baseline.sh, so evaluate-baseline scores both paths alike.
# Resumable: papers that finished (exit 0 or 2) are skipped; errors/interruptions retried.
# Usage: scripts/run_code_sim.sh SPEC_DIR [OUT_DIR] [PARALLEL]
set -euo pipefail
SPECS=$(realpath "${1:?Usage: scripts/run_code_sim.sh SPEC_DIR [OUT_DIR] [PARALLEL]}")
cd "$(dirname "$0")/.."

OUT=${2:-code_sim_results}
PARALLEL=${3:-4}
mkdir -p "$OUT/logs"
TOTAL=$(ls "$SPECS"/*.json | wc -l)
echo 0 > "$OUT/.progress"
# Same budget as the baseline so both paths get identical code-stage settings.
export CLAUDE_MAX_TOKENS=${CLAUDE_MAX_TOKENS:-16384}
echo "CLAUDE_MAX_TOKENS=$CLAUDE_MAX_TOKENS, parallel=$PARALLEL, specs=$SPECS, output=$OUT"
export OUT TOTAL SPECS

run_one() {
  local id=$1 code status n
  if [ -e "$OUT/logs/$id.done" ]; then
    status="skipped (already done)"
  else
    .venv/bin/run-code-sim --spec "$SPECS/$id.json" --arxiv-id "$id" --artifact-dir "$OUT" \
      > "$OUT/logs/$id.json" 2> "$OUT/logs/$id.log"
    code=$?
    echo "$id $code" >> "$OUT/exit_codes.txt"
    case $code in 0 | 2) touch "$OUT/logs/$id.done" ;; esac
    status=$(.venv/bin/python -I scripts/baseline_status.py "$OUT/logs/$id.json" "$code")
  fi
  {
    flock 9
    n=$(( $(cat "$OUT/.progress") + 1 ))
    echo "$n" > "$OUT/.progress"
    echo "[$n/$TOTAL] $(date +%H:%M:%S) $id $status"
  } 9> "$OUT/.progress.lock"
}
export -f run_one

ls "$SPECS"/*.json | xargs -n1 basename | sed 's/\.json$//' |
  xargs -P "$PARALLEL" -I{} bash -c 'run_one "$1"' _ {}

echo "Done. Rerun the same command to retry papers that ended in an error."
echo "Scoring equations against the papers (no model calls)..."
.venv/bin/evaluate-baseline --results "$OUT" | tail -n 3
