# Algo-Discovery-Sim

Hackathon project.

## Two workstreams

This repository holds two systems that attack the same problem from opposite ends, over the
same 300-paper corpus:

| | Workstream | Entry points | Docs |
|---|---|---|---|
| **A** | **Single-agent pipeline** — one agent takes an abstract to equations, to Qiskit, to a simulated result | `abstract-to-equations`, `run-pipeline`, ... | the blocks below |
| **B** | **Abstract2Method** — a decentralised agent swarm under an economic survival game, scored by a sealed judge against the paper's own method, and benchmarked against single-agent and central-planner baselines | `a2m` | [docs/SWARM.md](docs/SWARM.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |

Workstream B treats A's question as a benchmark: given only a claim, can agents rebuild a
correct, testable method? Quantum circuits and algorithms are its primary target (3 tasks);
chemistry, materials, biology and dynamics each contribute one task to show the design is not
quantum-specific.

```bash
uv run a2m tasks                                          # runnable benchmark tasks
uv run a2m run --system swarm --task arxiv-1409.3305 --llm mock --judge   # offline, no key
```

## Block 1: abstract to equations

One Claude Fable 5.1 call converts an abstract into a structured mathematical
specification. It records LaTeX equations, symbol definitions, registers, algorithm
steps, assumptions, missing information, and per-equation provenance. It does not
generate Qiskit itself; block 2 consumes its output. Schema and evidence checks do not
establish mathematical correctness.

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

## Block 2: equations to Qiskit

The same Fable model continues with the original abstract request and its saved
mathematical specification as conversation context. It produces a Python module
exposing `build_circuit(instance) -> QuantumCircuit`, an equation-to-code mapping,
an example instance, explicit changes to the specification, and unresolved issues.
This is a second stage of one reconstruction agent; no specialist agent or paper
retrieval is introduced. There are no automatic repair calls or model fallbacks yet.

```bash
uv sync --locked

# Generate source and run static checks; does not execute generated Python:
uv run equations-to-qiskit \
  --equations artifacts/7a0e6112-d9e3-4815-935f-eea6b25452e9/result.json

# Inspect the coding prompt and output schema without an API call:
uv run equations-to-qiskit \
  --equations artifacts/7a0e6112-d9e3-4815-935f-eea6b25452e9/result.json \
  --dry-run
```

Replace the path with a block-one `result.json` from your own run. By default the
original `request.json` is read from the same directory (`--request` overrides it).
Hashes bind the supplied abstract and experiment scope to the source run. Early
block-one artifacts without recorded generation parameters remain readable.

Build the isolated worker once to enable execution checks:

```bash
docker build -t algo-discovery-qiskit:local runtime

# Validate the scoped weighted-sum task from the demonstrated equation run:
uv run equations-to-qiskit \
  --equations artifacts/7a0e6112-d9e3-4815-935f-eea6b25452e9/result.json \
  --validate --reference modular_weighted_sum
```

`--validate` alone checks construction and transpilation. Adding the weighted-sum
reference supplies a public task contract: operation
`|x>|b> -> |x>|(b + sum_j weights[j]*x[j]) mod 2^n>` for binary `x`, classical
integer weights, and arbitrary initial accumulator `b`. Data qubits occupy indices
`0..m-1`; accumulator qubits occupy `m..m+n-1`; both registers are little-endian.
The circuit performs the operation only, without state preparation or measurement.
The reference checks all accumulator values as well as all data inputs, including
wraparound, and compares the full unitary up to a single global phase plus a
seeded complex superposition. Basis probabilities alone would miss relative phases.

This reference supports 1–4 data qubits and 1–4 target qubits (at most 8 total),
integer weights of magnitude at most 2^20, and a bound unitary circuit. This is the
first independent reference, not a universal quantum-algorithm verifier. It must
only be selected for a compatible declared scope. The reference contract is
additional task information and should be logged consistently in scored runs.
No full paper, textbook, or evaluator implementation is provided to Fable.

An optional `--instance-file path/to/instance.json` overrides the generated example.
For the weighted-sum contract, that file has exactly these fields:

```json
{"num_target_qubits": 3, "weights": [1, 2]}
```

Check already-saved code again, or use different instance parameters, without a
model call or API key:

```bash
uv run validate-qiskit \
  --code artifacts/CODE_RUN_ID/circuit.py \
  --instance-file artifacts/CODE_RUN_ID/instance.json \
  --reference modular_weighted_sum \
  --report artifacts/CODE_RUN_ID/revalidation.json
```

Replace `CODE_RUN_ID` with the code-stage run ID. This writes a separate validation
report and leaves the original generation record unchanged. The reference caps
full-operator calculations at 2,000 elementary gates. General isolated build checks
allow up to 12 qubits and 50,000 transpiled elementary gates, with a 30-second worker limit.

Simulate saved code with Qiskit Aer, again without a model call or API key:

```bash
uv run simulate-qiskit \
  --run-dir artifacts/CODE_RUN_ID \
  --reference modular_weighted_sum
```

The worker builds the circuit in Docker as above; Aer then runs the reconstructed
elementary circuit on the host, so generated Python is still never imported there.
Each input case is prepared as a computational basis state and simulated with
`--shots` (default 1024) and `--seed` (default 42, offset per case). The report,
`RUN_DIR/simulation.json` by default (or `--report`), records Aer's counts and exact
pre-measurement probabilities for every case. Bitstrings use Qiskit order: qubit 0
is the rightmost character.

With `--reference modular_weighted_sum`, the default inputs are every `(x, b)` pair,
and a case passes only when the reference output has probability 1 and receives
every shot. Statuses are `simulated` (no reference), `reference_passed`, `failed`,
and `unavailable`. Basis inputs cannot detect relative-phase errors, so this
complements rather than replaces `validate-qiskit`. An optional `--inputs` file
selects cases, with at most 256:

```json
[{"x": 3, "b": 7}, {"x": 1, "b": 0}]
```

Without a reference, cases take the form `{"basis_state": 5}` (full-register
little-endian integer; default `|0...0>`). The simulator sits behind a small
`SimulationBackend` interface in `simulation.py`, so other backends can be added later.

Each code-stage run saves a new `artifacts/<run_id>/` directory containing:

- `circuit.py`: generated operation (defines the function; does not execute it).
- `instance.json`: parameters actually selected for validation.
- `implementation.md`: summary, equation mapping, register layout, changes, limitations.
- `request.json`, `result.json`, `validation.json`: inputs, parent run ID, hashes,
  model usage/settings, and machine-readable validation results.
- `compiled.qasm`: elementary circuit reconstructed from worker gate data, when validation succeeds far enough.

Validation statuses: `not_run`, `build_passed`, `reference_passed`, `failed`, and
`unavailable`. `reference_passed` checks only the declared finite operation and
instance; it does not verify every equation, the full paper, or a quantum speedup.
The original `partial` math specification and its assumptions remain in the saved
request. The CLI exits 0 on successful generation/requested validation, 1 on input
or provider errors, and 2 for abstention, static failure, or unsuccessful requested
validation. Failed static/build/reference results retain generated code for review.

Generated Python is imported only in Docker, with no network, credentials, project
mount, or evaluator files; a read-only root filesystem; an unprivileged user; and
CPU, memory, process, output, and wall-time limits. Only temporary source, instance,
and trusted worker files are mounted read-only. Static AST checks are additional
guardrails, not the execution security boundary. The host receives bounded JSON
elementary gates and reconstructs the circuit without importing generated source.
If Docker is absent, validation reports `unavailable`; it never runs on the host.

The API exposes `POST /qiskit` on the existing local server. Its JSON body is:

```json
{
  "equation_request": {"abstract": "the original abstract", "experiment_scope": null},
  "equation_result": {"...": "the complete block-one result.json object"},
  "validate_circuit": true,
  "reference": "modular_weighted_sum",
  "instance": {"num_target_qubits": 3, "weights": [1, 2]}
}
```

The `equation_result` placeholder above must be replaced by the complete saved
object. A successful HTTP response can contain a failed validation report; inspect
the returned status fields. Requests are synchronous and include model latency.

Extra checks (no paid model requests):

```bash
RUN_DOCKER_TESTS=1 uv run pytest -q
uv run ruff check src tests
```

Quantum dependencies live in the `quantum` group and Aer in the host-only
`simulation` group; both are installed by default. The worker
uses a pinned Python image and hashed requirements exported from `uv.lock`. When
upgrading quantum dependencies, also update the frozen API guide in `code_prompt.py`,
regenerate `runtime/requirements.txt`, and rebuild the image:

```bash
uv export --only-group quantum --no-emit-project --no-header \
  --format requirements-txt --output-file runtime/requirements.txt --quiet
docker build -t algo-discovery-qiskit:local runtime
```

Circuit APIs follow [QFTGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFTGate)
and [Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator).

## Full pipeline: abstract to simulation

`run-pipeline` chains all three stages in one command: abstract to equations, then
equations to Qiskit with Docker validation, then Aer simulation. It makes two model
calls and needs `CLAUDE_HACKATHON_API` and the Docker worker image.

```bash
# Dataset paper by arXiv ID, checked against the weighted-sum reference:
uv run run-pipeline --arxiv-id 1411.5949 \
  --reference modular_weighted_sum \
  --instance-file artifacts/24065ab1-da09-469b-a5c2-2b64107ddd09/instance.json

# Any abstract, simulated without a correctness reference:
uv run run-pipeline --abstract-file my_abstract.txt --scope 'At most 6 qubits.'
```

Input options match `abstract-to-equations` (`--abstract-file`, `--abstract`,
`--stdin`), plus `--arxiv-id` for `data/circuit_dataset_300_v1/abstracts/`.
`--scope`, `--model`, and `--artifact-dir` apply to both model stages;
`--instance-file` and `--reference` go to code generation, and the reference is also
used for simulation along with `--inputs`, `--shots`, and `--seed`.

Each stage saves its usual artifacts. The equation stage writes to its own run
directory, and the code-stage directory also receives `simulation.json` and a
`pipeline.json` summary of both run IDs, each stage's status, and `stopped_at`.
The pipeline stops at the first unsuccessful stage. It records `equations`
(the abstract was insufficient), `code`, `validation`, `simulation`, or `error`
for input/provider failures. Exit codes match the stage CLIs: 0 on success, 1 for
input or provider errors, and 2 when a stage abstains or fails.

## Black-box code generation and simulation (any spec source)

`run-code-sim` runs stages 2–3 only (equations to Qiskit, Docker validation, Aer
simulation) on a math specification from any producer, such as a multi-agent swarm.
Different stage-one methods then share an identical code stage and can be compared
directly.

The input is one JSON file per paper:

```json
{
  "source": "swarm",
  "arxiv_id": "1406.2040",
  "specification": {"status": "partial", "problem": "...", "equations": [...], "...": "..."}
}
```

`specification` uses exactly the block-one schema (`uv run run-code-sim --print-schema`
prints the full JSON schema). `arxiv_id` selects the dataset abstract; alternatively
supply `"abstract": "..."` (and optionally `"experiment_scope"`). Block-one rules apply
unchanged: `status` must be `specified` or `partial` to continue, equation IDs must be
unique, and any `abstract_quote` must appear verbatim in the abstract. A spec that
fails these checks is recorded as `invalid_spec` at the equations stage (exit 2), like
invalid model output. A block-one `result.json` is also accepted directly.

```bash
# One spec:
uv run run-code-sim --spec swarm_specs/1406.2040.json

# A folder of <arxiv_id>.json specs, resumable, scored at the end:
scripts/run_code_sim.sh swarm_specs swarm_results 4

# The single agent's specs, in the same format, through the same path:
uv run python scripts/export_specs.py baseline_results single_agent_specs
scripts/run_code_sim.sh single_agent_specs single_agent_results 4
```

Each spec is saved as an equation run with `model` set to `external:<source>` and zero
usage, so the existing hashes, artifacts, `pipeline.json`, and `evaluate-baseline`
work unchanged. Model and token counts of the external producer are not recorded here.


`data/circuit_dataset_300_v1/` holds 300 arXiv quantum-algorithm papers (abstracts, full text, extracted equations), Qiskit textbook chapters, and a `manifest.jsonl` catalog. See its [README](data/circuit_dataset_300_v1/README.md).

Original build paths in the provenance fields have been replaced with the `<QRAG_ROOT>/` placeholder.
