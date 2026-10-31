# Architecture

Abstract2Method turns a paper's abstract into a scored reconstruction attempt. Everything in
the design follows from one rule: **a candidate proposes, the runner measures.** No number a
candidate reports about its own work is ever used.

## The whole pipeline

```
                     VISIBLE SIDE                          SEALED SIDE
                     ────────────                          ───────────
  skills/<domain>/SKILL.md
   roles · role bias · colony genome
   conventions · libraries · skill list
            │
            │ briefs
            ▼
  ┌───────────────────────┐   claim card    ┌──────────────────────────┐
  │ RECONSTRUCTION SYSTEM │◀────────────────│  data/tasks/<id>.json     │
  │                       │  abstract only  │  abstract, claim,         │
  │  swarm  ·  colonies   │                 │  criteria, interface,     │
  │  single agent         │                 │  visible tests, limits    │
  │  central planner      │                 └──────────────────────────┘
  └───────────┬───────────┘
              │ candidate code
              ▼
  ┌───────────────────────────────────────────────┐
  │ TRUSTED RUNNER            (src/a2m/evaluators)│
  │                                               │
  │  static pre-filter ─▶ sandboxed subprocess    │
  │                        skills/<d>/tools/*.py  │
  │                        shipped as a2m_task    │
  │                              │                │
  │  candidate returns an ANSWER │                │
  │   circuits · coordinates · molecules ·        │
  │   sequences · paths                           │
  │                              ▼                │
  │  runner substitutes the hidden instance,      │
  │  simulates, and computes every metric         │
  └───────────────────┬───────────────────────────┘
                      │ gap to the claim (0 = met)
                      ▼
              submission.json
                      │
                      ▼
  ┌───────────────────────────────────┐        ┌──────────────────────────────┐
  │ SEALED JUDGE   (src/a2m/judge)    │◀───────│ data/vaults/<id>/            │
  │  reruns on hidden tests           │        │  rubric (from the paper)     │
  │  checks loopholes                 │        │  hidden tests                │
  │  two model judges score the rubric│        │  reference.py                │
  │  compares with the reference      │        │  reported numbers            │
  └───────────────┬───────────────────┘        └──────────────────────────────┘
                  │ judge.json
                  ▼
      skills/<domain>/learnings/*.md   ← research artifacts, evaluator-side
      reports/summary.md               ← cross-system comparison
```

## Trust boundaries

| Boundary | Enforced by | What it buys |
|---|---|---|
| Candidate code cannot report its own score | evaluators compute every metric from the returned answer | a lying or self-grading candidate gains nothing |
| Candidate cannot see a hidden instance | quantum: opaque placeholder gate substituted after the build; biology: the oracle never leaves the runner (`sandbox: false`) | query budgets and hidden tests are real |
| Candidate cannot read the vault | sandbox profile (`bwrap` hides `/home`, `/mnt`, `/srv`, drops the network) plus an AST pre-filter | the rubric and reference stay sealed |
| Agents cannot read the paper | prompts are built only from the claim card and the runner's diagnostics; no file, web or retrieval tools | the task stays "infer from the claim" |
| Profiles cannot leak the method | `tests/test_skills.py` greps each rendered profile against a per-domain ban list | cross-domain scores stay comparable |
| Learnings cannot reach a prompt | only `SKILL.md` is read when briefing; pinned by a test | sealed rubric wording never returns to agents |

## How a candidate is run

Two flows share one sandbox:

**Circuit flow** (quantum, `CircuitEvaluator`). The candidate builds Qiskit circuits that
contain an opaque `oracle` placeholder. The circuit crosses the process boundary as JSON of
standard gates — composite gates are recursively expanded inside the sandbox, so nothing
opaque survives except the placeholder itself. The parent substitutes the real black box per
hidden instance, simulates, and scores. Resource counts come from unrolling to `{u, cx}` with
the black box excluded.

**Call flow** (everything else, `CallEvaluator`). The parent ships a skill tool's source into
the sandbox as `a2m_task` and calls one entry function. The *same module* is imported in the
parent to score, so the objective a candidate optimises and the one it is judged by cannot
drift apart. Where the oracle must stay hidden (biology), nothing is shipped and the runner
drives the rounds instead.

## The swarm

Agents hold no assignment. Each round every living agent picks an open need off a shared
index by pressure:

```
pressure = urgency(need) · (1 + 0.15·age) · (0.3 + promise) / (1 + claimants)
           · affinity(agent, role)
```

Role affinities start from the field's `role_bias` in `SKILL.md` and drift as the economy pays
out. Needs cycle `hypothesis → implementation → simulation → critique`, and a critique only
counts as a break if the runner reproduces it on a stress test the critic proposes.

### Survival pressure, at two levels

All energy movement goes through one function (`Economy._move`), so the three modes cannot
drift apart:

```
individual   cost → agent      payout → agent                    agent dies at 0
collective   cost → treasury   payout → treasury                 colony dies at 0
both         cost → agent      payout → agent (70%) + treasury   both can die
                               respawn and upkeep → treasury
```

Payouts come only from measured progress: `4·(parent_gap − gap) + 2·max(0, best_gap − gap)`,
plus a bonus for surviving critique, split back along the handover chain.

A colony carries a **genome** (role bias, how many method families to keep alive, repair
attempts, critiques required) seeded from its field's `SKILL.md`. Dead colonies leave a record
of cause, families tried and best gap; replacements are founded from the fittest survivor with
a mutated genome and inherited notes. The `swarm_colonies_independent` control runs the same
colonies with selection switched off, which is what separates selection from simply having
more parallel attempts.

## Domains and the skill tree

A field is a directory. Adding one needs no change to the swarm:

```
skills/<domain>/
  SKILL.md       roles, role bias, colony genome, conventions, libraries, skill list
  tools/*.py     helper modules; `sandbox: true` ones are shipped to candidates AND
                 imported by the runner, `sandbox: false` ones stay in the runner
  learnings/     judged-run artifacts + INDEX.md (evaluator-side)
```

`a2m/domains/profiles.py` loads these into a `DomainProfile`; `a2m/skills.py` owns the paths
and the shipping rule. Five domains ship: quantum (the primary target, three tasks), chemistry,
materials, biology, dynamics.

## Determinism

Simulator seeds, instance sampling and the swarm's choices are seeded per run. Model output is
not deterministic, so systems are compared over several seeds on an equal **dollar** budget
rather than equal tokens.
