# The skill tree

One directory per scientific field. A field is data, not code: adding one needs no change to
the swarm, the judge or the runner.

```
skills/<domain>/
  SKILL.md       what agents in this field are told, and how their colonies start
  tools/*.py     helper modules the runner provides
  learnings/     research artifacts distilled from judged runs, plus INDEX.md
```

## SKILL.md

YAML frontmatter plus two prose sections. Loaded by `a2m/domains/profiles.py` into the
`DomainProfile` every prompt and every new colony reads.

| Key | Effect |
|---|---|
| `roles` | what `hypothesize`, `implement`, `simulate`, `critique` mean in this field; prepended to the matching agent's prompt |
| `role_bias` | starting role affinities for newly born agents — more critics where a wrong answer is expensive, more implementers where the code is fiddly |
| `colony_genome` | a colony's starting `min_families`, `max_attempts`, `critiques_required`; colony-level selection mutates these |
| `libraries` | what candidate code may import, copied into each task's `allowed_imports` |
| `tools` | helper modules, each `sandbox: true` (shipped to candidates) or `sandbox: false` (runner-only) |
| `skills` | helper signatures described to agents, including ones with no module behind them |
| `eval_timeout_s` | sandbox wall clock for one evaluation |
| `backends` | optional accelerated backends, named only when they are genuinely available |
| `## Summary`, `## Conventions` | the field's prose briefing: units, idioms, pitfalls |

**No method hints.** A profile may describe the field; it may never describe the algorithm a
task asks the swarm to rebuild. `tests/test_skills.py` greps every rendered profile against a
per-domain ban list and fails on a leak — it has already caught one.

## tools/

A `sandbox: true` module is shipped into the sandbox as `a2m_task` *and* imported by the
trusted runner for scoring, so the objective a candidate queries is exactly the one it is
judged by. A `sandbox: false` module is runner-only: that is how biology's binding oracle
stays hidden, and `skills.tool_source` raises rather than hand it out.

## learnings/

One Markdown artifact per judged run (`a2m learn <run>`), plus an `INDEX.md` aggregating
across runs. The useful column is which components of a paper's method came back and which
are consistently missed — that is the finding the benchmark exists to produce, readable
without rerunning anything.

**Artifacts are evaluator-side.** They quote the sealed rubric and name the paper's method, so
they must never be shown to agents. Only `SKILL.md` is read when briefing; a test pins it.
