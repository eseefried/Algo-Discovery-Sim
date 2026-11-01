#!/usr/bin/env bash
# Use a separate GPU environment so serving dependencies do not alter the benchmark environment.
set -euo pipefail
cd "$(dirname "$0")/.."
# Do not inherit stale cache paths from another machine (for example /netdisk).
export HF_HOME="${NEMOTRON_CACHE_DIR:-$PWD/.cache/huggingface}"
export HF_HUB_CACHE="$HF_HOME/hub"
export HUGGINGFACE_HUB_CACHE="$HF_HUB_CACHE"
export HF_XET_CACHE="$HF_HOME/xet"
unset TRANSFORMERS_CACHE
mkdir -p "$HF_HUB_CACHE" "$HF_XET_CACHE"
if [ ! -w "$HF_HUB_CACHE" ] || [ ! -w "$HF_XET_CACHE" ]; then
  echo "Nemotron cache is not writable: $HF_HOME" >&2
  exit 1
fi
echo "Nemotron model cache: $HF_HOME"
.venv/bin/python -m algo_discovery.nemotron_server --check "$@"
INFERENCE_PYTHON=${INFERENCE_PYTHON:-.venv-nemotron/bin/python}
if [ ! -x "$INFERENCE_PYTHON" ]; then
  if [ "$INFERENCE_PYTHON" != .venv-nemotron/bin/python ]; then
    echo "INFERENCE_PYTHON does not point to an executable Python." >&2
    exit 1
  fi
  uv venv .venv-nemotron --python 3.12
fi
if [ "$INFERENCE_PYTHON" = .venv-nemotron/bin/python ] && [ ! -f .venv-nemotron/.ready ]; then
  uv pip install --python "$INFERENCE_PYTHON" 'torch>=2.10' \
    --index-url https://download.pytorch.org/whl/cu130
  uv pip install --python "$INFERENCE_PYTHON" 'transformers>=5,<6' \
    'peft>=0.21,<1' accelerate lm-format-enforcer fastapi uvicorn jsonschema
  touch .venv-nemotron/.ready
fi
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$INFERENCE_PYTHON" -m algo_discovery.nemotron_server "$@"
