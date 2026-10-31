# Abstract2Method

Can agents infer a correct, testable method from a paper's claim alone?

A paper's abstract states a claim: *a method exists that achieves a measurable result*.
Abstract2Method gives a reconstruction system **only the abstract and a claim card**. The system
must build a working method, run it in simulation, and meet the claimed numbers. A **sealed
judge** then reruns the method on hidden tests and compares it with the paper's own method.

The main system is a **decentralised swarm** under an economic survival game. It is benchmarked
against a **single strong agent** and a **central planner** on the same dollar budget.

```
 abstract + claim card ──▶ reconstruction system ──▶ submitted code (≤ 3 candidates)
        (visible)          swarm | single agent | planner            │
                                │  ▲                                  ▼
                                ▼  │ metrics only            ┌─────────────────┐
                         trusted runner (Qiskit Aer)         │  sealed judge   │
                         owns instances, oracles, scoring    │ hidden tests,   │
                                                             │ reference code, │
 paper, equations, rubric, reference ── vault (judge only) ─▶│ rubric graders  │
                                                             └────────┬────────┘
                                         claim_reproduced · method_match · valid_alternative
```

## Status

MVP. The first domain is quantum circuits. The loop works end to end, offline with a scripted
mock LLM and live with Claude. **No benchmark results exist yet**; mock runs test the harness
only.

| Component | State |
|---|---|
| Swarm: shared index, pressure matching, economy, deaths, respawns, lineage feedback | done |
| Baselines: single agent, central planner; ablations (no economy, no critics, no diversity) | done |
| Trusted runner + evaluators: black-box oracle tasks, unitary tasks | done (2 evaluators) |
| Sealed judge: hidden tests, loophole checks, two-model rubric, structural similarity | done |
| Runnable tasks | **2 development tasks** (`arxiv-1407.6402`, `arxiv-1411.5949`) |
| 300-paper corpus | readable via the manifest; tasks need curation first ([docs/ADDING_TASKS.md](docs/ADDING_TASKS.md)) |
| Sandbox | `bwrap` profile when bubblewrap works; otherwise an unprivileged subprocess (see Limitations) |
| Chemistry, materials, protein domains | not started |

## Quickstart

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
cp .env.example .env              # set CLAUDE_HACKATHON_API for live runs

uv run a2m tasks                  # runnable tasks
uv run a2m check-vault arxiv-1407.6402   # reference passes its own claim on hidden tests

# Offline, no key: full loop with the scripted mock LLM
uv run a2m run --system swarm --task arxiv-1407.6402 --llm mock --judge

# Live
uv run a2m run --system swarm --task arxiv-1407.6402 --judge
uv run a2m run --system single_agent --task arxiv-1407.6402 --judge

# Systems x tasks x seeds, judged and summarised in reports/summary.md
uv run a2m bench --systems swarm,single_agent,single_agent_small,central_planner --seeds 3
```

The dataset is read from `data/circuit_dataset_300_v1/` in this repository, falling back to
the shared mount `/mnt/zgx1-shared/Algo-Discovery-Sim/data/circuit_dataset_300_v1`. Override it
with `A2M_DATASET_DIR`. Run commands from the repository root.

## Data

`data/circuit_dataset_300_v1/` holds 300 arXiv quantum-algorithm papers (abstracts, full text,
extracted equations), Qiskit textbook chapters, and a `manifest.jsonl` catalog. See its
[README](data/circuit_dataset_300_v1/README.md). Original build paths in the provenance fields
have been replaced with the `<QRAG_ROOT>/` placeholder.

`data/tasks/` (visible claim cards) and `data/vaults/` (sealed judge material) are this
benchmark's curated layer on top of that corpus.

## What each side sees

| Reconstruction systems see | Only the judge sees |
|---|---|
| abstract (`data/tasks/<id>.json`) | paper text, equations (dataset) |
| claim, numeric success criteria, scope notes | rubric written from the paper before any run |
| code interface + visible test systems | hidden test systems |
| runner metrics and errors for their own code | reference implementation, reported numbers |

Agents have no file, web, or paper tools. Their only inputs are prompts built from the claim
card and the runner's diagnostics.

## How a task is checked

Candidate code never reports its own numbers. For an oracle task such as `arxiv-1407.6402`
(identify an affine Boolean function), the candidate builds circuits that contain an **opaque
placeholder** `oracle(k)`. The trusted runner substitutes the real oracle for each hidden
instance, simulates, and passes only raw counts back to the candidate's `postprocess`. It then
scores the answers. For a unitary task such as `arxiv-1411.5949` (modular adder), the runner
computes the circuit's unitary and checks every basis input.

A candidate's **gap** is its mean normalised distance to the success criteria across test
systems (0 = claim met). The gap is the swarm's only reward signal.

## The swarm

Roles are activities, not assignments. Each round, every agent picks an open need from the
**shared index** by pressure:

```
pressure = urgency(need) · (1 + 0.15·age) · (0.3 + promise) / (1 + claimants) · affinity(agent, role)
```

| Need | Action | Opened when |
|---|---|---|
| `needs_hypothesis` | propose a method family + sketch | start; too few families; a family stalls |
| `needs_implementation` | write or repair code from runner diagnostics | new sketch; failing or broken candidate |
| `needs_simulation` | run the trusted runner | new code |
| `needs_critique` | stress-test a passing candidate; a break counts only if the runner confirms it | candidate meets the claim |

**Survival economy** ([src/a2m/swarm/economy.py](src/a2m/swarm/economy.py), tuned in
[configs/systems/swarm.yaml](configs/systems/swarm.yaml)):

- Every action costs energy (implement 2, hypothesize 1, critique 1, simulate 0.5, idle 0.25).
- Payouts come only from measured progress: `4·(parent_gap − gap) + 2·max(0, best_gap − gap)`,
  plus 8 when a candidate survives critique. Credit flows back along the handover chain:
  implementer 45%, hypothesizer 35%, simulator 20%, critics 15% of the ready bonus.
- A confirmed break pays the critic 3 and costs the implementer 1.5.
- Energy ≤ 0 means death. Energy ≥ 14 lets an agent spawn a child with mutated role affinities.

**Lineage feedback** ([src/a2m/swarm/lineage.py](src/a2m/swarm/lineage.py)): every death
leaves a record (families backed, roles played, cause). Every payout leaves a success record.
Respawned and child agents inherit:

- a prompt block listing families that made progress (prefer) and families whose backers died
  or stalled (avoid), plus recent causes of death
- role affinities weighted toward the roles that earned the most

With `diversity_first`, a hypothesis that duplicates an active family is rejected, and its
author still pays for it. A family can be re-proposed as a fresh variant once its lineage
stalls. The swarm stops when two distinct families are ready, when the budget runs out, when
the population goes extinct, or after five rounds without progress.

## Survival pressure: individual, collective, both

The economy can apply selection at two levels. Collective survival runs several **colonies**,
each a swarm, on the same shared dollar budget ([src/a2m/swarm/colonies.py](src/a2m/swarm/colonies.py)).

| Mode | Who pays for actions | Who earns | Who dies | Config |
|---|---|---|---|---|
| individual | the agent | the agent | agents at energy ≤ 0; respawns are free | `swarm` |
| collective | the colony treasury | the treasury | colonies: treasury ≤ 0, extinct, or 5 rounds without progress; agents are immortal | `swarm_collective` |
| both | the agent | the agent, minus a 30% tax to the treasury | agents at energy ≤ 0; colonies when the treasury runs out (it pays 3 per respawn and 0.1 upkeep per agent per round) | `swarm_both` |
| control | the agent | the agent | agents only; colonies never die, reproduce, or get replaced | `swarm_colonies_independent` |

**Colony selection.** Each colony carries a **genome** that its agents inherit:

- role biases (e.g. more critics, fewer hypothesizers)
- `min_families`, `max_attempts`, `critiques_required`

Starting colonies get varied genomes. When a colony dies, it leaves a colony death record:
cause, families tried, best gap, and genome. A replacement is then founded from the fittest
living colony (most ready families, then lowest gap, then richest treasury). The replacement
gets a mutated copy of that colony's genome, a starting grant, and notes for its agents. The
notes combine recent colony deaths with the parent colony's own agent-level lessons. A colony
whose treasury reaches 48 founds a daughter and pays it 24. If every colony dies, the best
dead genome is refounded. Foundings are capped (`max_foundings`), and the shared dollar budget
caps everything.

Compare `swarm_colonies_independent` against `swarm_collective` and `swarm_both`. The control
has the same colonies and genome variation but no colony-level selection, so it separates the
effect of selection from the effect of extra parallel attempts.

All of this happens within one run. Nothing carries over to the next task yet; see the Roadmap.

## Systems compared

All systems use the same prompts, actions, runner, tasks, and **dollar budget**
(`configs/default.yaml`, `$2` per run by default).

| Config | Question it answers |
|---|---|
| `swarm` | many small agents (Haiku 5.5) + economy + lineage; individual survival |
| `swarm_collective` / `swarm_both` | does colony-level selection, alone or stacked on individual selection, find methods more often? |
| `swarm_colonies_independent` | control: several colonies with no colony selection |
| `single_agent` | one strong agent (Fable 5.1), same spend |
| `single_agent_small` | one agent on the swarm's model: separates "more agents" from "bigger model" |
| `central_planner` | Opus 5.5 planner assigns Haiku workers: does decentralisation beat control? |
| `swarm_no_economy` / `swarm_no_critics` / `swarm_no_diversity` | value of each mechanism |
| `swarm_mixed` | heterogeneous swarm (Haiku + Sonnet) |

Equal dollars, not equal tokens: Haiku 5.5 costs about 1/100 of Fable 5.1 per token. In a live
smoke test, one Fable hypothesis call cost $0.18, while a Haiku hypothesis, implementation, and
passing simulation together cost $0.002. `max_tokens` in the budget adds an equal-tokens
condition.

## Scores (sealed judge)

| Score | Definition |
|---|---|
| `claim_reproduced` | the system's first-ranked candidate meets every criterion on visible **and hidden** tests, with no loopholes |
| `method_match` | weighted rubric score (0 / 0.5 / 1 per item), mean of two model judges (`A2M_JUDGE_MODELS`) |
| `method_recovered` | `claim_reproduced` and `method_match ≥ 0.7` |
| `any_method_recovered` | the same, for any of the ≤ 3 submitted candidates |
| `valid_alternative` | `claim_reproduced` and `method_match < 0.5`, flagged for human review |
| `structural_similarity` | oracle queries, qubits, two-qubit gates, depth vs the reference |
| loopholes | static-check violations, opaque `unitary`/`initialize`-style gates (score forced to 0) |

Judge disagreements of ≥ 0.5 on any rubric item are listed under `human_review`.

Example: in `arxiv-1407.6402` the paper applies its second query **coherently** to the same
register (A₁ = U_f H U_f H, reading b from the extra qubit and the parity of a). Querying
f(0ⁿ) in a separate circuit also meets the claim, but it misses the two paper-specific rubric
items (`r4`, `r5`), so it should count as a valid alternative rather than a recovered method.

## Run artifacts

Each run writes `runs/<task>/<system>/<run_id>/` (`runs/latest` points at the newest):

- `events.jsonl`: every hypothesis, implementation, simulation, critique, death, spawn, and respawn
- `candidates/*.py`: every implementation the runner executed
- `submission.json`: ranked submission, usage, isolation profile, agents, ledger, lineage
- `all_candidates.json`, `judge.json`, `judge.md`
- colony variants also write `colonies/<k>/`: each colony's own events, candidates, and
  `stats.json` (agents, ledger, lineage). `submission.json` carries the colony summaries and
  colony death records.

`a2m report` aggregates every `judge.json` into `reports/summary.md` and `reports/runs.csv`.

## Repository layout

```
configs/            default budget/judge settings; one YAML per system variant
data/tasks/         visible claim cards (curated)
data/vaults/<id>/   sealed: vault.json (rubric, hidden tests, paper numbers), reference.py
src/a2m/
  llm/              Claude client (budget, structured output, refusal fallback), prompts, mock
  sandbox/          subprocess harness, static pre-filter, circuit transport
  evaluators/       trusted task evaluators (affine_boolean_id, modular_adder)
  swarm/            index, matching, economy (survival modes), lineage, runtime, colonies
  baselines/        single_agent, central_planner
  judge/            sealed judge
  curation/         LLM-drafted claim cards and recall (contamination) checks for curators
  workspace.py actions.py run.py report.py cli.py
tests/              evaluator correctness, economy, LLM request shape, end-to-end mock runs
docs/               ARCHITECTURE.md, TASK_FORMAT.md, ADDING_TASKS.md
```

## Limitations

- **Two development tasks, both contaminated.** Both papers predate every model's training
  data, and the 1407.6402 abstract names its starting algorithm. They validate the harness and
  cannot serve as held-out evidence. Run `a2m curate recall --task <id>` before trusting any
  task.
- **Isolation.** The `bwrap` profile hides `/home`, `/mnt`, and `/srv` (including vaults and
  papers) and removes network access. When bubblewrap cannot create namespaces, the runner
  falls back to `none`: a scrubbed subprocess with rlimits and an AST pre-filter. That is not a
  security boundary. Candidate code could read files the user can read, including the vault.
  Each run records its profile. Use `--require-isolation` for scored runs.
- **The black box is opaque only at the circuit level.** Gate placeholders cannot be inspected,
  but in-process Python tricks are blocked only by the static filter (and by `bwrap`).
- The mock LLM is a scripted test double for the two development tasks. It is not a baseline.
- Budget enforcement is checked before each call. A round of parallel calls can overshoot by
  one round's spend.
- Rubric grading uses LLM judges. Disagreements go to human review; nothing replaces a curator
  spot-check.

## Roadmap

1. Curate held-out tasks from the 160 direct-circuit candidates (claim card, evaluator,
   reference, vault), starting with tasks newer than model cutoffs.
2. Scored runs: all systems × tasks × ≥ 3 seeds under `--require-isolation`.
3. Information ladder: abstract only → + textbooks → + methods section.
4. Open problems: claim cards with no paper behind them, scored against a known baseline.
5. Further dry-lab domains (chemistry, materials, protein) as new evaluators.
6. Cross-task self-improvement: keep an archive of surviving colony genomes and lessons, found
   new colonies from it on later tasks, and measure the gain on held-out tasks only. Selection
   keeps using visible-test metrics; the judge never feeds back.
