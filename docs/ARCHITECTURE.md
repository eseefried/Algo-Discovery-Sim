# Architecture

## Trust boundaries

```
untrusted                     trusted (parent process)                  sealed
─────────                     ────────────────────────                  ──────
LLM output ──▶ candidate.py ─▶ static pre-filter (sandbox/static.py)
                               sandbox subprocess: harness.py
                                 build:  build_circuits(spec) ─▶ flattened JSON circuits
                               circuits.load(): rebuild, substitute real oracle
                               Aer / Operator simulation (evaluators/)
                                 post:   postprocess(counts, spec) ─▶ answers
                               evaluator scores answers ─▶ metrics ─▶ gap
                                                                         vault/<id>/
                               sealed judge ◀──────────────────────────  rubric, hidden tests,
                                                                         reference.py
```

- Candidate code runs in a separate process (`sandbox/runner.py`) with a scrubbed environment,
  a temp working directory, CPU, memory and file-size rlimits, and, where bubblewrap works, no
  network and no view of `/home`, `/mnt`, or `/srv`.
- Circuits cross the boundary as JSON lists of standard Qiskit gates. Composite gates are
  recursively expanded inside the sandbox. `oracle` stays an opaque placeholder; the parent
  substitutes the real oracle per hidden instance, so a candidate cannot inspect it.
- Every metric is computed by the parent. A candidate that prints or returns its own score
  gains nothing.

## Components

| Module | Role |
|---|---|
| `workspace.py` | candidates, simulation via the evaluator, diagnostics, ranking, event log |
| `actions.py` | hypothesize, implement, simulate, critique; shared by every system |
| `swarm/index.py` | open needs (the swarm's only coordination surface) |
| `swarm/matching.py` | pressure scoring + softmax choice per agent |
| `swarm/economy.py` | costs, progress payouts, chain credit, bounties, spawning |
| `swarm/lineage.py` | death, success and stall records; prefer/avoid feedback; role affinities |
| `swarm/runtime.py` | rounds: choose (sequential) → execute (thread pool) → apply (sequential) → lifecycle |
| `baselines/` | single agent and central planner on the same actions |
| `judge/sealed.py` | reference check, hidden tests, loopholes, rubric, structural similarity |
| `llm/client.py` | Claude Messages API with structured JSON output, effort, refusal fallback, dollar budget |

## A swarm round

1. Keep a `needs_hypothesis` open while there are fewer than `min_families` families.
2. Each living agent, in random order, samples a need weighted by pressure × its role affinity.
   Implementation, simulation, and critique needs are exclusive within a round.
3. All chosen actions run in parallel. LLM calls and sandbox runs are thread-safe.
4. Outcomes apply in order: charge costs, open follow-up needs, pay progress along the chain,
   record lineage.
5. Lifecycle: agents at energy ≤ 0 die; rich agents spawn children; the population is refilled
   to `n_agents` with agents seeded from lineage.

## Colonies (collective survival)

`swarm/colonies.py` runs several `Swarm` instances. Each has its own workspace (candidate
and agent ids are prefixed `k<n>-`), its own index, and its own lineage. All of them share the
sandbox and the dollar budget. All energy movements go through `Economy._move`, which routes
them by survival mode:

```
individual  cost -> agent        payout -> agent                     agent dies at 0
collective  cost -> treasury     payout -> treasury                  colony dies at 0
both        cost -> agent        payout -> agent (70%) + treasury    both can die;
                                 respawn and upkeep -> treasury      respawn needs funds
```

Each round, every active colony plays one swarm round (in parallel), then:

1. Colonies whose `stop_reason()` is a failure die (treasury exhausted, extinct, stagnated).
   They leave a `ColonyDeath` record. Without selection, they go dormant instead.
2. Each death is replaced from the fittest living colony: mutated genome, starting grant, and
   inherited notes. After a total extinction, the best dead genome is refounded.
3. Rich colonies pay `found_cost` to found a daughter.

At the end, every colony's candidates are merged and ranked together for the submission.

## Determinism

Simulator seeds, instance sampling, and the swarm's random choices are seeded per run. Model
output is not deterministic, so compare systems over several seeds.
