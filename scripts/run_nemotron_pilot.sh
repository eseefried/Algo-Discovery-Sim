#!/usr/bin/env bash
# Small resumable pilot, deliberately separate from the 96-paper benchmark.
# Usage: bash scripts/run_nemotron_pilot.sh OUT_DIR [WAIT_FOR_PID]
set -euo pipefail
cd "$(dirname "$0")/.."
PILOT_OUT=${1:?Pass an output directory}
PILOT_WAIT_PID=${2:-}
mkdir -p "$PILOT_OUT/ids"
for id in 1411.5949 1407.6402 1409.3305; do
  cp "single_agent_specs/$id.json" "$PILOT_OUT/ids/$id.json"
done
export A2M_BACKEND=local A2M_MODEL=nemotron-quantum A2M_VARIANT=swarm
export A2M_MAX_CALLS=30 A2M_MAX_SECONDS=1800 A2M_CODE_BUDGET=0.15
export CODE_BACKEND=anthropic CODE_MODEL=claude-sonnet-5-5 CODE_EFFORT=high
export NEMOTRON_BASE_URL=http://127.0.0.1:8000/v1
cat > "$PILOT_OUT/plan.txt" <<'PLAN'
Three-paper operational pilot: 1411.5949, 1407.6402, 1409.3305.
Six-agent swarm; one agent request at a time, one paper at a time.
Local calls: max 30 per paper; max 1800 seconds checked between actions.
Local output cap: 4096 tokens. In-flight actions can exceed the time limit.
Sonnet/high code feedback: $0.15 per paper, with one-call possible overshoot.
Final shared Sonnet/high code pass is additional paid usage.
This is not an algorithmic correctness evaluation or a completed benchmark.
PLAN
if [ -n "$PILOT_WAIT_PID" ]; then
  echo "Waiting for isolated timing request (PID $PILOT_WAIT_PID) to finish."
  while kill -0 "$PILOT_WAIT_PID" 2>/dev/null; do sleep 10; done
fi
echo "Starting three-paper pilot."
exec bash scripts/run_a2m_batch.sh "$PILOT_OUT/ids" "$PILOT_OUT/run" 1
