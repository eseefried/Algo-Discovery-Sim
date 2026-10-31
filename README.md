# Algo-Discovery-Sim

Hackathon project.

## Block 1: abstract to equations

One Claude Fable 5.1 call converts an abstract into a structured mathematical
specification. It records LaTeX equations, symbol definitions, registers, algorithm
steps, assumptions, missing information, and per-equation provenance. It does not
generate Qiskit yet. Schema and evidence checks do not establish mathematical correctness.

Install with Python 3.12+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync --locked --group dev
cp .env.example .env  # Only if you do not already have a populated .env
```

Set `CLAUDE_HACKATHON_API` in `.env` or the environment. `CLAUDE_MODEL` defaults
to `claude-fable-5-1`. The app intentionally uses the hackathon key rather than an
unrelated `ANTHROPIC_API_KEY`. Existing environment values take precedence over `.env`.
Run commands from this project directory so `.env` and artifact paths resolve correctly.

```bash
uv run abstract-to-equations \
  --abstract-file data/circuit_dataset_300_v1/abstracts/arxiv-1411.5949.txt

# Inspect the complete prompt and response schema without a key or model call:
uv run abstract-to-equations \
  --abstract-file data/circuit_dataset_300_v1/abstracts/arxiv-1407.6402.txt \
  --dry-run

# Optional scope is recorded as a user target, never as abstract evidence:
uv run abstract-to-equations \
  --abstract-file data/circuit_dataset_300_v1/abstracts/arxiv-1411.5949.txt \
  --scope 'Two 2-bit registers; modular addition only.'
```

Each accepted result saves `request.json`, `result.json`, and a readable
`equations.md` under `artifacts/<run_id>/`. The JSON includes requested/response
model IDs, prompt version/hash, request/abstract hashes, usage, timing, generation settings, and
`mathematics_verified: false`. Credentials are excluded. There are no automatic
retries or model fallbacks; truncation, refusal, invalid output, and unsupported
model access produce errors. The 8,192-token default includes any model thinking;
increase `CLAUDE_MAX_TOKENS` explicitly if needed (up to the 32,768-token app cap).
`CLAUDE_EFFORT` is explicitly set to `high` by default and recorded in each run;
it can be changed to `low`, `medium`, `xhigh`, or `max` for separate experiments.

Statuses are `specified`, `partial`, `insufficient_information`, and
`not_applicable`. Partial results can supply useful background equations while
identifying absent paper-specific details. Abstract-supported equations require
an exact substring quote; this validates the quote's presence, not its scientific entailment.
No paper, equation export, textbook, or catalog is loaded by the generation code.

Run the local API:

```bash
uv run uvicorn algo_discovery.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` for the `POST /equations` request form. The body
is `{"abstract": "...", "experiment_scope": null}`. Calls are synchronous with a
configurable provider timeout; there is no job queue yet. This local endpoint has
no authentication or rate limiting; keep it bound to localhost. The generation
call sends the abstract and optional scope to Anthropic. Do not expose it publicly
with your API key attached.

Checks:

```bash
uv run pytest
uv run ruff check src tests
```

Tests use mocked HTTP responses through the real Anthropic SDK and make no paid
requests. Model and output integration follow Anthropic's
[Fable 5.1 model documentation](https://platform.claude.com/docs/en/models/fable-5-1/overview)
and [structured output documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

## Data

`data/circuit_dataset_300_v1/` holds 300 arXiv quantum-algorithm papers (abstracts, full text, extracted equations), Qiskit textbook chapters, and a `manifest.jsonl` catalog. See its [README](data/circuit_dataset_300_v1/README.md).

Original build paths in the provenance fields have been replaced with the `<QRAG_ROOT>/` placeholder.
