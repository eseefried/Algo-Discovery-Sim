# Local Nemotron swarm

## Native-equation evolutionary swarm

The active implementation is `algo_discovery.native_swarm` with configuration
`configs/systems/nemotron_native_swarm.yaml`:

```bash
source ~/.bashrc
uv run python -u -m algo_discovery.native_swarm \
  --arxiv-id 1407.6402 --out artifacts/native_swarm \
  --max-usd 0.50 --max-calls 40 --max-seconds 1200
```

Three logical agents use the existing a2m shared-index matching, role affinities,
virtual energy, retries and lineage. Nemotron proposes numbered LaTeX using its
unchanged training-format prompt. Agents differ in temperature, repetition penalty
and equation start index. Sonnet/medium proposes method plans, assembles full specs
and independently reviews the generated code; Sonnet/high remains the code stage.
The assembler can reject or repair native predictions using background knowledge.
Its notes, original native outputs and counts of retained/rewritten equations are
saved separately. This is a **hybrid** system, not an all-Nemotron swarm.

The scheduler settles actions immediately. After two initial method plans, it
prioritizes implementation, simulation and review before expanding more branches,
and exits after the first reviewed success. One agent is reserved outside all
implementation chains so a fresh independent reviewer is always available.
The coordinator and reviewer use the actual Qiskit worker contract, which compiles
explicit oracle parameters into ordinary gates. They do not inherit the sealed
curated-task harness's incompatible opaque-placeholder requirements. This permits
functional simulation but does not certify black-box query complexity.

Failures and code-stage abstentions receive no progress rewards and open repair
tasks with actual runner/reviewer diagnostics. Working circuits remain provisional
until review by an agent outside the implementation chain. Model objections route
back to revision; they are not counted as passes or verified counterexamples.
Only reproduced valid-instance execution failures qualify for a critic bounty.

Agents start with 5 virtual energy units. Actions consume energy. Depleted agents
die, and up to 6 replacements maintain the three-agent population. When measured
success exists, replacement selects the best earned/spent donor, clones its role
affinities and native decoding strategy, and mutates exactly one decoding gene.
Without a successful donor, it explores the initial strategies. Rewards are deferred
until execution and review succeed. There is no requirement to produce deaths in
every run; a successful population can survive without replacement.

Local GPU requests are serialized across native clients with a shared file lock,
before HTTP request timeout begins. A pilot may share the GPU with the baseline;
such wall times are not a controlled throughput comparison. The implementation is
a single-host logical swarm, not a multi-host fault-tolerant ledger service.

The per-paper resource limit counts native, coordinating and code calls. The
separate estimated USD cap covers all Sonnet roles; one in-flight call can exceed
the cap. Existing rates are estimates, not a billing guarantee. Raw model outputs,
energy movements, deaths, parentage, genotype changes and candidates are retained
under `OUT/runs/PAPER/UUID/`. An interrupted paper restarts as a new UUID rather
than resuming its in-memory population.

Fitness currently means Docker/Aer execution plus independent-agent model review.
It is **not** a guarantee of algorithmic correctness or complete-paper reproduction.
Independent functional contracts must be evaluated separately.

## Verified training task: abstract to LaTeX

The transferred training recipe establishes that this adapter was trained to
produce **numbered display equations**, not Qiskit code or JSON mathematical
specifications. The earlier JSON-spec swarm pilot is an out-of-format transfer
test, not an evaluation of the adapter's trained task.

Use the matching plain-text client first:

```bash
uv run nemotron-equations \
  --abstract-file data/circuit_dataset_300_v1/abstracts/arxiv-1411.5949.txt \
  --out artifacts/nemotron-equations-qft --max-blocks 1
```

The input is the whitespace-normalized abstract plus `Start equation: N`.
The system prompt matches the data preparation script exactly. Each block requests
up to eight equations; `<END_EQUATIONS>` signals the final block. The client
advances only after complete, consecutively numbered output; it does not feed
gold equations into subsequent requests. Responses, usage, numbering and whether
the paper is complete are saved separately. Truncated blocks are preserved for
inspection but are not accepted as equation predictions.

The server accepts omitted `response_format` or `{"type":"text"}` without adding
JSON instructions or applying JSON token filtering. It uses the training model
class and checks that all 258 expected LoRA modules attach. Reasoning remains off.

These raw equation predictions are not `MathSpecification` objects. Using them
for Qiskit generation requires a separate, explicitly evaluated conversion;
neither register layouts nor provenance claims should be invented by a parser.

The supplied preparation audit identifies 135 training and 15 validation papers,
all at manifest positions 151–300. Their IDs do not intersect the 96 benchmark IDs.
The original recipe and sample records are in the transferred, Git-ignored
`artifacts/nemotron-training-handoff/nemotron-quantum-lora-handoff/` directory.

Initial native-format tests are saved under `artifacts/nemotron-native/`.
Greedy LoRA returned eight copies of one formula (different tags) for the QFT
arithmetic abstract in 31 seconds. With `--repetition-penalty 1.12`, the same
abstract produced one formula and the end marker in 7 seconds. This is a changed
decoding profile and a single-example format result, not evidence of correct
reconstruction. The default penalty remains 1 for reproducibility. The CLI records
the selected penalty and reports repeated content separately from equation tags.

## Earlier JSON-spec experiments

`a2m-spec --backend local` runs the a2m specification agents against an
OpenAI-compatible **chat completions** server. The server must load the base model
and LoRA adapter and expose the adapter under the model name passed to `--model`.
This client does not load weights or start a GPU server.

## Starting the shared local model

```bash
bash scripts/serve_nemotron.sh
```

The launcher checks weight access, creates an isolated `.venv-nemotron` on first
use, installs CUDA 13 PyTorch and Transformers/PEFT, then downloads the base
model if needed. Downloads can be large. It uses the saved adapter tokenizer/chat
template with reasoning disabled and JSON Schema token filtering via
[LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer). It loads one
GPU model and queues agent requests through one process bound to `127.0.0.1:8000`.
The launcher overrides inherited Hugging Face cache variables with the writable,
Git-ignored `.cache/huggingface` directory in this project. Set
`NEMOTRON_CACHE_DIR` to choose another location; stale paths such as `/netdisk`
from another machine will not be reused.
The normal benchmark Python environment is unchanged. Keep this terminal open.

The loader follows the full multimodal architecture indicated in
[NVIDIA's model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-BF16),
so the adapter's `language_model` target modules remain available. GPU loading
and decoder compatibility still require a live smoke test; the server API is
covered by offline tests. Set `INFERENCE_PYTHON` to use an existing GPU environment.

Checkpoint:
`/mnt/zgx1-shared/nemotron-bolt-e4b-quantum-lora-20261101T010128Z-5eb582d7`

Base: `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-BF16`. The weights file currently needs
read permission from its owner. Serving-engine support for this particular base
and adapter must be verified on the hardware before a live run.

The endpoint must support `response_format.type=json_schema` and return
`usage.prompt_tokens` and `usage.completion_tokens`. Responses are also validated
locally against each role's JSON Schema. Truncated, refused, malformed and
schema-invalid responses fail the action. There is no silent fallback to Claude.
See the [vLLM structured-output contract](https://docs.vllm.ai/en/latest/features/structured_outputs/).

Once the model is served as `nemotron-quantum`:

```bash
export NEMOTRON_BASE_URL=http://127.0.0.1:8000/v1
# Optional authentication for the local server:
# export NEMOTRON_API_KEY=...

uv run a2m-spec --arxiv-id 1411.5949 --out a2m_nemotron \
  --backend local --model nemotron-quantum \
  --max-calls 100 --token-budget 500000 --max-seconds 1800 \
  --code-budget 0.15
```

Local inference records **zero API USD**, tokens and calls. This is not a claim of
zero hardware cost. `--budget` does not constrain local mode. Instead it stops
on calls, tokens, elapsed time or the existing swarm stopping conditions (including
max ticks). Limits are checked between actions/requests; in-flight requests can
finish past a limit. Failed local requests consume a call, too.

The agents' virtual energy economy, deaths, spawning and lineage are unchanged.
They remain available even without API spending.

Local runs retain six agents but default to one in-flight agent action
(`--local-parallel 1`) because the simple server serializes GPU generation.
This prevents requests timing out merely while waiting behind other agents.
Local responses are limited to 4096 output tokens (`--local-max-output-tokens`);
both settings are recorded in the run summary. Do not run several papers in
parallel against this server. Restart the server after a timed-out run to clear
any requests still generating in the background.

The black-box code stage still uses Claude and requires `CLAUDE_HACKATHON_API`.
Its **separate** `--code-budget` defaults to $0.15 per paper. When this cap is
exhausted, further builds are skipped while agents may continue until their own
execution limits. As with existing paid runs, an in-flight code call can overshoot
the cap. Set `--code-budget 0` to skip paid build feedback; the current adapter still
loads Claude configuration, so its key must be configured even then.

The summary records the backend, execution limits, token usage and paid code budget.
Existing Anthropic runs retain the original shared per-paper dollar budget.

For a batch:

```bash
A2M_BACKEND=local A2M_MODEL=nemotron-quantum \
  A2M_MAX_CALLS=100 A2M_MAX_SECONDS=1800 A2M_CODE_BUDGET=0.15 \
  scripts/run_a2m_batch.sh single_agent_specs a2m_nemotron 1
```

`NEMOTRON_BASE_URL` and `NEMOTRON_API_KEY` are inherited by the batch workers.
The batch script subsequently runs the final code/simulation stage using Claude;
that separate stage is not covered by the swarm's code-feedback cap. Use the
single-paper CLI to test the integration before launching a paid batch.

## Optional fully local code stage

The comparison default remains **Sonnet/high** for code generation, including
when the swarm agents are Nemotron. Source the current hackathon credentials
with `source ~/.bashrc` before paid runs; environment values take precedence over `.env`.

For a separate fully local experiment, explicitly add `--code-backend local
--code-model nemotron-quantum` to the single-paper command. This does not require
a Claude key, and `--code-budget` is ignored. The same source checks, equation
mapping checks, Docker build and Aer simulation apply to either code provider.

For a fully local batch set `CODE_BACKEND=local CODE_MODEL=nemotron-quantum`.
For standalone saved specs use `MODEL_BACKEND=local NEMOTRON_MODEL=nemotron-quantum
uv run run-code-sim --spec <spec.json>`. Local code artifacts record `backend=local`.
