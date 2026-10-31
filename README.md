# Abstract2Method

Can agents infer a correct, testable method from a paper's claim alone?

A paper's abstract states a claim: *a method exists that achieves a measurable result*.
Abstract2Method gives a reconstruction system **only that abstract and a claim card**. The
system must build a working method, run it in simulation, and hit the claimed numbers. A
**sealed judge** then reruns it on hidden tests and compares it with the paper's own method.

That is the same skill discovery needs. An open problem is a claim with no paper behind it
yet, so once the workflow works on published abstracts it can be pointed at open problems,
where success means beating a known baseline in simulation.

The main system is a **decentralised swarm** under an economic survival game, benchmarked
against a single strong agent and a central planner on the same dollar budget.

```
 abstract + claim card ──▶ reconstruction system ──▶ submitted code (≤ 3 candidates)
        (visible)          swarm | colonies | single agent | planner      │
                                │  ▲                                       ▼
                                ▼  │ measured metrics only        ┌──────────────────┐
                         trusted runner (Qiskit, RDKit,           │   sealed judge   │
                         ViennaRNA, SciPy, ALCHEMI)               │ hidden tests,    │
                         owns instances, oracles, scoring         │ rubric, reference│
                                                                  └────────┬─────────┘
 paper, rubric, reference ── vault (judge only) ──────────────────▶        │
                                                                           ▼
                              claim_reproduced · method_match · valid_alternative
                                                                           │
                                             skills/<domain>/learnings/ ◀──┘
```

Full design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Status

MVP. **Quantum circuits and algorithms are the primary target** and the deepest domain; four
other dry-lab fields are included to show the design generalises. The loop runs end to end
offline with a scripted mock LLM and live with Claude. **No benchmark results exist yet** —
mock runs test the harness only.

| Component | State |
|---|---|
| Swarm: shared index, pressure matching, economy, deaths, respawns, lineage | done |
| Survival pressure: individual, collective (colony treasury + selection), both, control | done |
| Baselines: single agent, central planner; ablations (no economy / critics / diversity) | done |
| Trusted runner: circuit flow + call flow, 6 evaluators | done |
| Sealed judge: hidden tests, loophole checks, two-model rubric, structural similarity | done |
| Skill tree: 5 fields as editable directories, learnings artifacts | done |
| Runnable tasks | **7** (3 quantum, 1 each chemistry / materials / biology / dynamics) |
| Sandbox | `bwrap` when available, otherwise an unprivileged subprocess (see Limitations) |

## Quickstart

Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
cp .env.example .env              # set CLAUDE_HACKATHON_API for live runs

uv run a2m tasks                           # runnable tasks
uv run a2m check-vault arxiv-1409.3305     # reference passes its own claim on hidden tests

# Offline, no key: the full loop on the scripted mock LLM
uv run a2m run --system swarm --task arxiv-1407.6402 --llm mock --judge

# Live
uv run a2m run --system swarm --task arxiv-1409.3305 --judge
uv run a2m run --system single_agent --task arxiv-1409.3305 --judge

# Systems x tasks x seeds, judged, distilled and summarised
uv run a2m bench --systems swarm,single_agent,central_planner --seeds 3
uv run a2m learn runs --all       # research artifacts per domain
```

Run from the repository root. Optional accelerated backends: `uv sync --extra alchemi`.

## Tasks

Every task is one paper, scoped to what a bounded simulation can check.

| Task | Field | Claim being rebuilt | Reference |
|---|---|---|---|
| `arxiv-1407.6402` | quantum | identify an affine Boolean function with certainty in two oracle queries | coherent two-query sequence |
| `arxiv-1411.5949` | quantum | add two registers in place, exactly, with no ancillas | QFT phase adder |
| `arxiv-1409.3305` | quantum | amplify to ≥ 1−δ² for *every* marked fraction above a bound, keeping the speedup | Chebyshev phase sequence |
| `arxiv-cond-mat-9803344` | materials | find the lowest-energy Lennard-Jones cluster from random starts | minimize-then-Metropolis |
| `arxiv-1909.11655` | chemistry | improve penalized logP while staying chemically similar | SELFIES GA + discriminator |
| `arxiv-2010.02141` | biology | design RNA binders to a hidden target on a fixed measurement budget | threshold-greedy rollouts |
| `arxiv-cond-mat-0205527` | dynamics | recover the transition path and its barrier between two stable states | normal-force string |

Each is verified two ways: the reference must meet its own claim on visible **and hidden**
tests (`a2m check-vault`), and an obvious wrong substitute must fail. For fixed-point search
the reference is additionally checked against the paper's closed-form success probability,
and plain Grover — same query budget — collapses to 0.00005 at some marked fractions.

## What each side sees

| Reconstruction systems see | Only the judge sees |
|---|---|
| the abstract, with the method's coined name blanked | the paper and its equations |
| the claim, numeric criteria, scope notes | the rubric, written from the paper before any run |
| the code interface and visible test systems | hidden test systems |
| their field's `SKILL.md` conventions and helpers | the reference implementation and reported numbers |
| the runner's metrics and errors **for their own code** | everything in `data/vaults/` |

Agents have no file, web or paper tools. Candidate code never reports a score: it returns an
answer, and the runner measures it.

## Survival pressure

| Mode | Who pays | Who dies | Config |
|---|---|---|---|
| individual | the agent | agents at zero energy; respawns are free | `swarm` |
| collective | the colony treasury | colonies, when the treasury empties or progress stops | `swarm_collective` |
| both | the agent, taxed 30% to the treasury | agents **and** colonies | `swarm_both` |
| control | the agent | agents only; colonies never die or reproduce | `swarm_colonies_independent` |

The control exists so colony-level selection can be told apart from simply running more
colonies in parallel.

## Scores

| Score | Definition |
|---|---|
| `claim_reproduced` | the first-ranked candidate meets every criterion on visible **and hidden** tests, with no loopholes |
| `method_match` | weighted rubric score, mean of two independent model judges |
| `method_recovered` | `claim_reproduced` and `method_match ≥ 0.7` |
| `valid_alternative` | `claim_reproduced` and `method_match < 0.5` — a different method that works |
| `structural_similarity` | queries, qubits, two-qubit gates, depth against the reference |

Judge disagreements of ≥ 0.5 on any rubric item are listed for human review.

## Skills and learnings

A field is a directory — see [skills/README.md](skills/README.md):

```
skills/<domain>/SKILL.md      roles, role bias, colony genome, conventions, libraries
skills/<domain>/tools/*.py    helpers; sandbox: true are shipped to candidates, false stay in
skills/<domain>/learnings/    one artifact per judged run + INDEX.md
```

`a2m learn` distils judged runs into Markdown: the outcome, which rubric components came
back, which method families the swarm explored and how they died, and what survival pressure
did. `INDEX.md` aggregates recovery rates across runs — *which parts of a paper's method
agents consistently fail to infer* is the finding this benchmark exists to produce. Artifacts
are evaluator-side and never shown to agents.

## Repository layout

```
configs/            budget and judge settings; one YAML per system variant
data/tasks/         visible claim cards          data/vaults/  sealed rubrics and references
data/circuit_dataset_300_v1/   300 arXiv quantum papers (abstracts, text, equations)
skills/<domain>/    SKILL.md, tools/, learnings/
src/a2m/
  domains/          skill-tree loader -> DomainProfile
  evaluators/       trusted evaluators, one per task kind
  sandbox/          subprocess harness, static pre-filter, circuit transport
  swarm/            index, matching, economy, lineage, runtime, colonies
  baselines/        single_agent, central_planner        judge/  sealed judge
  backends/         optional NVIDIA ALCHEMI backend
  skills.py learnings.py workspace.py actions.py run.py report.py cli.py
tests/              evaluators, economy, skills, learnings, end-to-end mock runs
```

## Limitations

- **Isolation.** `bwrap` hides `/home`, `/mnt` and `/srv` and drops the network. Where
  bubblewrap cannot create namespaces the runner falls back to a scrubbed subprocess with
  rlimits and an AST filter, which is not a security boundary. Each run records its profile;
  use `--require-isolation` for scored runs.
- **Hidden oracles are genuinely hidden only in quantum and biology.** Materials, chemistry
  and dynamics use public objectives, where what is measured is search quality, verified by
  the runner re-scoring the returned answer.
- **The materials task is easier than the paper.** At 7–17 atoms, repeated local optimization
  from random starts also finds the global minimum, so reproducing that claim does not by
  itself imply the paper's method — the rubric is what separates them. The sizes where the
  distinction bites (38, 75–77, 98) need far more compute than a bounded run.
- **The development tasks are contaminated.** All seven papers predate current models. They
  validate the harness; they are not held-out evidence. Run `a2m curate recall --task <id>`
  before trusting a task.
- The mock LLM is a scripted test double, not a baseline.
- Rubric grading uses model judges; disagreements go to human review.
- Budget is checked before each call, so a round of parallel calls can overshoot by one round.

## Roadmap

1. Curate held-out tasks newer than model cutoffs, starting from the 160 direct-circuit
   candidates in the corpus.
2. Scored runs: all systems × tasks × ≥ 3 seeds under `--require-isolation`.
3. Information ladder: abstract only → + textbooks → + methods section.
4. Cross-task self-improvement: seed colonies from the learnings archive, measured on
   held-out tasks only, with the judge never feeding back.
5. Open problems: claim cards with no paper behind them, scored against a known baseline.
