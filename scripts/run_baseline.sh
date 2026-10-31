#!/usr/bin/env bash
# Run the full pipeline over every dataset abstract. Resumable: papers that finished
# (exit 0 or 2) are skipped on rerun; errors and interrupted runs are retried.
# Usage: scripts/run_baseline.sh [OUT_DIR] [PARALLEL]
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=${1:-baseline_results}
PARALLEL=${2:-4}
mkdir -p "$OUT/logs"
TOTAL=$(ls data/circuit_dataset_300_v1/abstracts | wc -l)
echo 0 > "$OUT/.progress"
# Truncation at the 8,192 default was common; the environment value wins over .env.
export CLAUDE_MAX_TOKENS=${CLAUDE_MAX_TOKENS:-16384}
echo "CLAUDE_MAX_TOKENS=$CLAUDE_MAX_TOKENS, parallel=$PARALLEL, output=$OUT"
export OUT TOTAL

run_one() {
  local id=$1 code status n
  if [ -e "$OUT/logs/$id.done" ]; then
    status="skipped (already done)"
  else
    .venv/bin/run-pipeline --arxiv-id "$id" --artifact-dir "$OUT" \
      > "$OUT/logs/$id.json" 2> "$OUT/logs/$id.log"
    code=$?
    echo "$id $code" >> "$OUT/exit_codes.txt"
    case $code in 0 | 2) touch "$OUT/logs/$id.done" ;; esac
    status=$(.venv/bin/python -I scripts/baseline_status.py "$OUT/logs/$id.json" "$code")
  fi
  # Shared counter so parallel workers print one consistent [n/total] sequence.
  {
    flock 9
    n=$(( $(cat "$OUT/.progress") + 1 ))
    echo "$n" > "$OUT/.progress"
    echo "[$n/$TOTAL] $(date +%H:%M:%S) $id $status"
  } 9> "$OUT/.progress.lock"
}
export -f run_one

ls data/circuit_dataset_300_v1/abstracts | sed 's/^arxiv-//; s/\.txt$//' |
  xargs -P "$PARALLEL" -I{} bash -c 'run_one "$1"' _ {}

echo "Done. Rerun the same command to retry papers that ended in an error."
