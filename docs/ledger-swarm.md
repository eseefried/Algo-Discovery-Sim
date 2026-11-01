# Ledger swarm

Three independent OS processes reconstruct an abstract through a shared SQLite
ledger. They bid, contribute a portion, and post remaining requirements as child
contracts. A supervisor restores failed workers by cloning a successful genotype
and changing one execution setting. Output uses the existing `ExternalSpec` format.

This is a local-process prototype: decentralized execution, centralized state.
Workers on separate hosts would need a PostgreSQL/API ledger. SQLite must be on
local disk rather than the shared/NFS mount. The default database is
`/tmp/algo-discovery-swarm/ledger.sqlite3`; reports live in `artifacts/swarm/`.

## Run

```bash
source ~/.bashrc
cd /mnt/zgx1-shared/Algo-Discovery-Sim
uv sync --locked
uv run run-swarm --arxiv-id 1411.5949 --max-calls 12 --max-seconds 600
```

The default model is `claude-haiku-5-5`, medium effort. Credentials come from
`CLAUDE_HACKATHON_API`. Existing environment variables override `.env`; pass
`--model claude-haiku-5-5` to override a stale model selection for one run.
Historical Fable results are preserved. Each worker starts a fresh model request
with its contract and ledger context; it retains no private model conversation.

An exported root directory contains `specs/PAPER_ID.json` (or `specs/ROOT_ID.json`),
`ledger-summary.json`, and `events.jsonl`. Metadata is kept outside `specs/` so the
batch runner will not treat accounting files as papers. The spec works with
`run-code-sim --spec PATH` and `scripts/run_code_sim.sh SPECS_DIRECTORY`.

To invoke the black box afterward in the same command:

```bash
uv run run-swarm --arxiv-id 1411.5949 \
  --scope 'Two binary inputs, classical weights (1,2), three accumulator qubits; modular weighted sum.' \
  --max-calls 12 --blackbox --reference modular_weighted_sum
```

`--blackbox` adds the existing code-stage model call plus Docker/Aer work. That
extra model call is outside the reconstruction call budget, recorded in the usual
black-box artifacts. It is opt-in so math-only runs do not incur the extra cost.

## Contracts and settlement

The domain adapter has five requirements, with the indicated field ownership:

| Requirement | Fields |
| --- | --- |
| `problem` | Problem statement and finite scope |
| `equations` | Equations and symbol definitions |
| `circuit_plan` | Registers, initial state, algorithm steps |
| `measurement` | Measurement and classical postprocessing |
| `audit` | Review the full specification, assumptions, missing details, status |

Prerequisites preserve this order. Workers initially complete at most two parts
per contribution. The model chooses completed parts and groups remaining work
into children; the ledger enforces nonempty progress, exact coverage, ownership,
and prerequisites. The final audit can revise earlier work but must explain
substantive corrections. Independent roots run concurrently; one reconstruction
often forms a short chain because its fields depend on earlier math.

Tasks use `Open`, `Assigned`, `Completed`, and terminal `Failed`. A parent's own
portion can complete while its root tree is still open. The root completes only
when all descendants complete. An honest `insufficient_information` assessment
can complete the work tree but returns CLI exit 2 and cannot proceed through
reconstruction in the black box. Schema/quote checks and audit are not proof of
scientific correctness; independent references remain necessary.

## Virtual economics

Wallets use integer **virtual cents**, unrelated to provider billing. Each worker
starts with 10,000 cents (100 credits), and each root has 50,000 cents (500 credits).
Actual model calls and returned token usage are recorded separately.

Confidence is a capability-based proxy, not a calibrated probability or an extra
model call. Bids use a fraction of available funds weighted by confidence (20%
initially), with exposure capped relative to initial capital. The one-second
auction starts with the first bid, after all three processes register readiness.
Highest amount wins; confidence and agent ID break ties. Bid reservations prevent
overspending. Losing bids release reservations; only winning bids are burned.

Completing two of five requirements pays 200 credits and leaves 300 for children.
A 100-credit worker bidding 20 then holds 280 credits. Child creation, completion,
and payout are one transaction, and total reward cannot exceed the root's 500.
Replacement endowments are additional virtual system funding, explicitly logged.

## Recovery and evolution

Assigned tasks have a 30-second lease, renewed roughly every ten seconds.
Expiry reopens the task with a new auction round. Fencing tokens prevent late or
duplicate completion from collecting payment or creating children. Process startup
has a separate grace period. Invalid contributions bankrupt a worker and reopen
its contract immediately; hard crashes wait for lease expiry.

The spawner maintains three processes. It selects a historically successful
configuration by completed-task throughput and mutates exactly one small gene:
effort, token cap, progress limit, bid fraction, or one capability preference.
This mutates execution settings, not model weights. Fitness measures operational
completion, not scientific quality. There is no model-based central planner.

Provider interruptions are bounded and kept separate from genotype defects.
HTTP 400/401/403/404/422 stop the root with sanitized diagnostics; creating more
agents cannot fix an unavailable model or exhausted account credit. Defaults cap
a root at twelve model calls, a task at three assignments, and a supervisor at
twelve replacements. Runtime is bounded too. Missing returned token usage is
marked unknown rather than asserted to cost zero.

## Persistent service and inspection

```bash
uv run swarm-ledger --db /tmp/demo.sqlite3 init
uv run swarm-ledger --db /tmp/demo.sqlite3 submit --arxiv-id 1409.3305
uv run swarm-ledger --db /tmp/demo.sqlite3 serve --max-seconds 600
uv run swarm-ledger --db /tmp/demo.sqlite3 status ROOT_ID
uv run swarm-ledger --db /tmp/demo.sqlite3 export ROOT_ID
uv run swarm-ledger --db /tmp/demo.sqlite3 events
uv run swarm-ledger --db /tmp/demo.sqlite3 verify
```

Use the same DB path across terminals. A renewable supervisor lease prevents two
spawners from controlling one ledger. Shutdown stops its processes and releases
work; later `serve` invocations can continue pending roots without resetting their
call counts. `/tmp` is not a backup: use durable local storage to survive host
cleanup. Event hashes detect edits but are not signatures or protection against
someone able to rewrite the entire database and recompute its chain.

Tests make no paid requests:

```bash
uv run pytest -q tests/test_swarm_ledger.py tests/test_swarm_runtime.py
```

They cover auctions, reward conservation, concurrent settlement, stale-token
fencing, budgets, history tampering, supervisor exclusivity, three real processes,
a hard crash, cloning/mutation, and black-box export compatibility.

For architecture comparisons, rerun the single-agent control with the same Haiku
model and paper set. Historical Fable results are a different model condition.
Report actual reconstruction calls/tokens and keep downstream settings fixed;
virtual wallet balances are not a measure of provider cost or scientific quality.
