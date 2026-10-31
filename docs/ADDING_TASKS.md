# Adding a task

The 300-paper corpus is a candidate pool, not a set of ready experiments. Each task needs a
curator. Budget about an hour per task for a paper with a direct circuit construction.

1. **Pick a paper.** Prefer `screening` route "direct circuit or algorithm candidates", and
   papers newer than the models you will test.
2. **Probe contamination.** `uv run a2m curate recall --task <id>` asks several models to
   identify the paper and its method from the abstract. If a model describes the method,
   either drop the task or report it as contaminated.
3. **Draft (optional).** `uv run a2m curate draft --task <id>` asks Claude Fable 5.1 to propose a
   claim, criteria, test systems, rubric, hidden tests, and reported numbers from the abstract
   and paper. It writes `data/drafts/<id>.json`. Treat every field as a suggestion.
4. **Choose or write an evaluator.** Reuse `affine_boolean_id`-style black-box oracle tasks or
   `modular_adder`-style unitary tasks where the interface fits. Otherwise add a class in
   `src/a2m/evaluators/`, register it in `__init__.py`, and write its `interface` text.
   Instance data the method must discover (oracles, hidden functions, target states) stays in
   the parent process.
5. **Write the claim card** in `data/tasks/<id>.json` from the abstract only. Keep the claim
   inside what a small simulation can check, and write scope cuts in `notes`.
6. **Write the vault** in `data/vaults/<id>/`: implement `reference.py` from the paper, add hidden
   tests, and write the rubric from the paper before running any system.
7. **Validate.** `uv run a2m check-vault <id>`, then add tests in `tests/test_evaluators.py`
   showing that deliberately wrong variants fail (bit order, phase sign, missing step, too many
   queries or ancillas).
8. Set `curation_status` to `curated`. The task now appears in `a2m tasks` and `a2m bench`.
