# Task format

A runnable task has two parts: a visible claim card and a sealed vault. The dataset manifest
(`manifest.jsonl` in `A2M_DATASET_DIR`) supplies the abstract and paper; `a2m.schema.TaskRecord`
reads it and keeps unknown fields verbatim.

## Claim card: `data/tasks/<id>.json` (visible)

| Field | Meaning |
|---|---|
| `task_id` | manifest id, e.g. `arxiv-1407.6402` |
| `domain` | `quantum` (later `chemistry`, `materials`, `protein`) |
| `evaluator` | name in `a2m.evaluators.REGISTRY` |
| `abstract` | abstract text shown to agents (redact method names here if needed) |
| `claim` | one measurable sentence, scoped to what a small simulation can check |
| `criteria` | list of `{metric, comparator (>=,<=,==), target, tolerance, scale}`; `scale` normalises the gap |
| `interface` | the evaluator's code contract (copied from `Evaluator.interface`) |
| `test_systems` | visible `{name, params}`; params go to the evaluator, which hides instance data |
| `qubit_cap` | hard cap including ancillas |
| `allowed_imports` | top-level modules candidate code may import |
| `curation_status` | `curated` (runnable) or `draft` |
| `notes` | scope decisions, e.g. which parts of the abstract are out of scope |

## Vault: `data/vaults/<id>/` (sealed)

`vault.json`:

| Field | Meaning |
|---|---|
| `rubric` | 4-8 `{id, text, weight, keywords}` method components, written from the paper **before** any scored run. Weight paper-specific steps above textbook background. `keywords` is a cheap lexical signal reported alongside judge scores. |
| `hidden_test_systems` | larger or different instances, never shown to agents |
| `reported_numbers` | what the paper reports, with section references |
| `reference_family` | short label for the paper's method |
| `reference_file` | normally `reference.py`, which implements the paper's method against the same interface |
| `provenance` | where the rubric came from |

`a2m check-vault <id>` must pass: the reference meets the claim on visible and hidden tests.
The judge refuses to score a task whose reference fails.

## Evaluator contract

`Evaluator.evaluate(code, params, sandbox, allowed_imports, qubit_cap)` returns
`{"ok": bool, "metrics": {...}, "stats": {...}}` or `{"ok": False, "error": str}`. It owns the
instance generation, the black box, the simulation, and the scoring. `public_spec(params)` is
the only part of a test system the candidate receives.
