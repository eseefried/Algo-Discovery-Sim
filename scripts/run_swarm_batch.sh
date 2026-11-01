#!/usr/bin/env bash
# Phase 1: swarm specs for every paper in ID_DIR (one <arxiv_id>.json each; only names are used).
# Phase 2: those specs through run_code_sim.sh (code + Docker + Aer), then math scoring.
# Resumable: papers whose swarm finished (exit 0 or 2) are skipped; errors are retried.
# Usage: scripts/run_swarm_batch.sh ID_DIR [OUT_DIR] [PARALLEL]
set -euo pipefail
IDS=$(realpath "${1:?Usage: scripts/run_swarm_batch.sh ID_DIR [OUT_DIR] [PARALLEL]}")
cd "$(dirname "$0")/.."

OUT=${2:-swarm_full}
PARALLEL=${3:-3}
SWARM_MODEL=${SWARM_MODEL:-claude-haiku-5-5}
SWARM_MAX_CALLS=${SWARM_MAX_CALLS:-6}
CODE_MODEL=${CODE_MODEL:-claude-sonnet-5-5}
CODE_EFFORT=${CODE_EFFORT:-high}
mkdir -p "$OUT/logs" "$OUT/specs" /tmp/algo-discovery-swarm
TOTAL=$(ls "$IDS"/*.json | wc -l)
echo 0 > "$OUT/.progress"
echo "swarm=$SWARM_MODEL max_calls=$SWARM_MAX_CALLS code=$CODE_MODEL/$CODE_EFFORT parallel=$PARALLEL out=$OUT"
export OUT TOTAL SWARM_MODEL SWARM_MAX_CALLS

swarm_one() {
  local id=$1 code status n spec
  if [ -e "$OUT/logs/$id.done" ]; then
    status="skipped (already done)"
  else
    # One SQLite ledger per paper, on local disk (not NFS), so parallel runs never contend.
    .venv/bin/run-swarm --arxiv-id "$id" --model "$SWARM_MODEL" --max-calls "$SWARM_MAX_CALLS" \
      --db "/tmp/algo-discovery-swarm/$id.sqlite3" --output-dir "$OUT/runs" \
      > "$OUT/logs/$id.json" 2> "$OUT/logs/$id.log"
    code=$?
    echo "$id $code" >> "$OUT/exit_codes.txt"
    case $code in 0 | 2) touch "$OUT/logs/$id.done" ;; esac
    spec=$(.venv/bin/python -I -c 'import json,sys
try: print(json.load(open(sys.argv[1])).get("specification") or "")
except Exception: print("")' "$OUT/logs/$id.json")
    if [ -n "$spec" ] && [ -e "$spec" ]; then
      cp "$spec" "$OUT/specs/$id.json"
    fi
    status=$(.venv/bin/python -I scripts/swarm_status.py "$OUT/logs/$id.json" "$code")
  fi
  {
    flock 9
    n=$(( $(cat "$OUT/.progress") + 1 ))
    echo "$n" > "$OUT/.progress"
    echo "[swarm $n/$TOTAL] $(date +%H:%M:%S) $id $status"
  } 9> "$OUT/.progress.lock"
}
export -f swarm_one

ls "$IDS"/*.json | xargs -n1 basename | sed 's/\.json$//' |
  xargs -P "$PARALLEL" -I{} bash -c 'swarm_one "$1"' _ {}

echo "Swarm phase done: $(ls "$OUT/specs" | wc -l) specs. Starting code + simulation."
CLAUDE_MODEL=$CODE_MODEL CLAUDE_EFFORT=$CODE_EFFORT \
  scripts/run_code_sim.sh "$OUT/specs" "$OUT/results" "$PARALLEL"
