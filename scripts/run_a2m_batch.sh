#!/usr/bin/env bash
# Phase 1: the a2m swarm writes a spec for every paper in ID_DIR (one <arxiv_id>.json each).
# Phase 2: those specs through run_code_sim.sh (code + Docker + Aer), then math scoring.
# Resumable: papers whose swarm finished (exit 0 or 2) are skipped; errors are retried.
# Usage: scripts/run_a2m_batch.sh ID_DIR [OUT_DIR] [PARALLEL]
set -euo pipefail
IDS=$(realpath "${1:?Usage: scripts/run_a2m_batch.sh ID_DIR [OUT_DIR] [PARALLEL]}")
cd "$(dirname "$0")/.."

OUT=${2:-a2m_full}
PARALLEL=${3:-3}
A2M_BUDGET=${A2M_BUDGET:-0.50}
A2M_BACKEND=${A2M_BACKEND:-anthropic}
A2M_MAX_CALLS=${A2M_MAX_CALLS:-100}
A2M_MAX_SECONDS=${A2M_MAX_SECONDS:-1800}
A2M_CODE_BUDGET=${A2M_CODE_BUDGET:-0.15}
A2M_VARIANT=${A2M_VARIANT:-swarm}
if [ "$A2M_BACKEND" = local ]; then
  A2M_MODEL=${A2M_MODEL:-nemotron-quantum}
else
  A2M_MODEL=${A2M_MODEL:-claude-sonnet-5-5}
fi
A2M_EFFORT=${A2M_EFFORT:-medium}
CODE_BACKEND=${CODE_BACKEND:-anthropic}
if [ "$CODE_BACKEND" = local ]; then
  CODE_MODEL=${CODE_MODEL:-$A2M_MODEL}
else
  CODE_MODEL=${CODE_MODEL:-claude-sonnet-5-5}
fi
CODE_EFFORT=${CODE_EFFORT:-high}
mkdir -p "$OUT/logs" "$OUT/specs"
TOTAL=$(ls "$IDS"/*.json | wc -l)
echo 0 > "$OUT/.progress"
echo "a2m variant=$A2M_VARIANT backend=$A2M_BACKEND model=$A2M_MODEL/$A2M_EFFORT" \
  "runner+black box code=$CODE_MODEL/$CODE_EFFORT parallel=$PARALLEL out=$OUT"
if [ "$A2M_BACKEND" = local ]; then
  echo "Local limits: $A2M_MAX_CALLS calls, $A2M_MAX_SECONDS seconds; paid build feedback: \$$A2M_CODE_BUDGET/paper"
else
  echo "Shared model budget: \$$A2M_BUDGET/paper"
fi
export OUT TOTAL A2M_BUDGET A2M_VARIANT A2M_MODEL A2M_EFFORT CODE_MODEL CODE_EFFORT
export A2M_BACKEND A2M_MAX_CALLS A2M_MAX_SECONDS A2M_CODE_BUDGET
export CODE_BACKEND

a2m_one() {
  local id=$1 code status n
  if [ -e "$OUT/logs/$id.done" ]; then
    status="skipped (already done)"
  else
    if [ "$A2M_BACKEND" = local ]; then
      if ! .venv/bin/python -c '
import os, httpx
headers = {"Authorization": "Bearer " + os.environ["NEMOTRON_API_KEY"]} if os.getenv("NEMOTRON_API_KEY") else {}
try:
    r = httpx.get(os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1").rstrip("/") + "/models", headers=headers, timeout=10)
    r.raise_for_status()
    assert any(m.get("id") == os.environ["A2M_MODEL"] for m in r.json()["data"])
except Exception:
    raise SystemExit(1)
'; then
        echo "Local model unavailable; stopping batch before paper $id." >&2
        return 255
      fi
    fi
    .venv/bin/a2m-spec --arxiv-id "$id" --out "$OUT" --budget "$A2M_BUDGET" \
      --variant "$A2M_VARIANT" --model "$A2M_MODEL" --effort "$A2M_EFFORT" \
      --backend "$A2M_BACKEND" --max-calls "$A2M_MAX_CALLS" \
      --max-seconds "$A2M_MAX_SECONDS" --code-budget "$A2M_CODE_BUDGET" \
      --code-backend "$CODE_BACKEND" \
      --code-model "$CODE_MODEL" --code-effort "$CODE_EFFORT" --quiet \
      > "$OUT/logs/$id.json" 2> "$OUT/logs/$id.log"
    code=$?
    echo "$id $code" >> "$OUT/exit_codes.txt"
    case $code in 0 | 2) touch "$OUT/logs/$id.done" ;; esac
    status=$(.venv/bin/python -I scripts/swarm_status.py "$OUT/logs/$id.json" "$code")
  fi
  {
    flock 9
    n=$(( $(cat "$OUT/.progress") + 1 ))
    echo "$n" > "$OUT/.progress"
    echo "[a2m $n/$TOTAL] $(date +%H:%M:%S) $id $status"
  } 9> "$OUT/.progress.lock"
}
export -f a2m_one

ls "$IDS"/*.json | xargs -n1 basename | sed 's/\.json$//' |
  xargs -P "$PARALLEL" -I{} bash -c 'a2m_one "$1"' _ {}

echo "a2m phase done: $(ls "$OUT/specs" | wc -l) specs. Starting code + simulation."
if ! compgen -G "$OUT/specs/*.json" > /dev/null; then
  echo "No usable specifications produced; see runs/*/summary.json. Skipping code stage."
  exit 2
fi
MODEL_BACKEND=$CODE_BACKEND NEMOTRON_MODEL=$CODE_MODEL CLAUDE_MODEL=$CODE_MODEL CLAUDE_EFFORT=$CODE_EFFORT \
  scripts/run_code_sim.sh "$OUT/specs" "$OUT/results" "$PARALLEL"
