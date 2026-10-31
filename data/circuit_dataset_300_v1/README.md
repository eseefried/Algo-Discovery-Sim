# Quantum circuit dataset: 300-paper expansion

Prepared for an abstract → math → Qiskit code → local simulation MVP. This collection contains 300 unique paper IDs, including the original approved ten, with separate abstract, body-text, and mathematical-expression exports. The original `../mvp_circuit_dataset_v1/` collection remains intact. Its ten paper/abstract/equation exports are byte-identical in this expansion.

## Start here

- `PAPERS.md`: clickable catalog of all 300 papers.
- `catalog.csv`: compact spreadsheet-friendly catalog.
- `manifest.jsonl`: machine-readable paths, source hashes, selection evidence, topic, proposed experiment scope, and status.
- `provenance/validation.json`: structural and integrity results, plus known metadata differences.

## Contents

```text
abstracts/                 300 abstract-only text files
papers/                    300 body-text files, with available appendices/references
equations/                 300 JSONL files of displayed and inline math
qiskit_textbooks/           archival textbook prose/math and code-cell source
manifest.jsonl
catalog.csv
PAPERS.md
provenance/
  selection.json           frozen selected sources and original metadata
  screening.jsonl          per-paper text evidence, section headings, and route
  build.json               counts, source breakdown, hashes, build timestamp
  validation.json          integrity checks and limitations
  build_dataset.py         deterministic local-source export pipeline
  extraction.py            abstract/body alignment helpers
  validate_dataset.py      integrity validator
```

No PDF, figure image, notebook output, or model weights are copied into this dataset. Figure captions are removed; prose references to figures remain. Existing tables, pseudocode, code listings, and mathematical expressions are retained. Some gate sequences exist only in excluded circuit figures, so textual completeness must be assessed when implementing each paper.

The exports contain **16,474 displayed expressions** and **105,586 inline expressions**. These counts include mathematical expressions in appendices and references, not just equations essential to an algorithm. Code-fenced listings are excluded from math extraction for new exports; the original ten retain their approved extraction unchanged. Math remains in the paper text as well as in the separate records. The `latex` field preserves source-conversion content, including any Unicode symbols or pre-existing transcription errors; it is not guaranteed to compile or faithfully reproduce the PDF.

The textbook collection contains **110 text exports: 84 notebooks, 23 Markdown files, and 3 Python files**. All original code-cell source is retained, with cell labels; code has not been executed or migrated to current Qiskit APIs. The textbook index records its original source paths and hashes. This is the full textbook material available in the local source collection, not a newly downloaded textbook edition.

## Selection and simulation readiness

The selection targets papers containing an algorithm, constructive circuit procedure, or explicitly defined quantum-walk evolution that can be explored as a small finite circuit. Topics include circuit synthesis, arithmetic, Boolean oracles, search, variational learning, state preparation, channels, phase estimation, Hamiltonian simulation, and walk constructions. It includes algorithm-containing application/analysis papers and classical algorithms for constructing or simulating quantum circuits; not all 300 introduce an original quantum algorithm.

Screening combines editorial title/abstract screening with programmatic full-text evidence. `screening.algorithm_evidence` and `provenance/screening.jsonl` expose the supporting text. This is a research candidate collection, not 300 manually certified, simulator-ready experiments:

- **10 approved seed papers** preserve the initial selection and experiment targets.
- **160 direct circuit or algorithm candidates** have a plausible gate-level starting route.
- **130 require additional encoding or protocol design**, such as oracle/work-register synthesis, a finite walk boundary, qudit encoding, measurement/feed-forward, or a noise/channel model.

Every paper remains marked as unimplemented and simulation-unvalidated. Topic labels and added simulation targets are editorial templates; they are not extracted paper-specific experiment specifications. The three `quantum_algorithm_other` items need more specific task design before implementation. A direct-candidate label is not a claim that its circuit is already available or known to fit the resource cap.

For the 290 additions, **12 total qubits is a proposed design cap**, including ancillas and encoded registers, not a measured or inferred resource estimate. `total_qubit_budget` is null until a concrete circuit is designed. Start with tiny instances and short schedules; defer a method if its actual requirements exceed the cap. Density-matrix noise simulations and training loops may still be expensive below that cap. The approved seed records retain their earlier planning estimates.

Quantum-walk construction items are labeled `constructive_evolution_model`. They define step/evolution procedures that can be mapped to a finite circuit, but a gate decomposition may need to be derived. Infinite-line or asymptotic results cannot be claimed as reproduced by a bounded finite simulation. For hardware papers, the intended scope is their ideal algorithm/gate-level construction rather than hardware calibration or device dynamics.

## Source coverage and abstract versions

All content was read locally. The main arXiv corpus supplies 280 papers (including the ten seeds); the curated optimization collection supplies 20 newer papers. Availability of preserved math in the existing conversions biases the selection toward 2007–2016; the newer additions span 2017–2026. This is not a representative or comprehensive sample of current quantum algorithms.

The arXiv metadata archive was used to locate and cross-check abstracts. The exported abstract comes from the actual local converted paper, because metadata and PDF versions sometimes differ. Metadata abstracts and versions remain in provenance where available, and low textual agreement is reported. High textual similarity does not certify an exact arXiv version. Two selected papers have no matching metadata record in the archive; their abstracts were extracted from local front matter.

The old paper sources remain under `<QRAG_ROOT>/resources/corpora_build/arxiv/manifest_arxiv-bbde4e36/items/`. The newer sources are under the corresponding `manifest_qhpc_optimization_tiny-3daea705/items/` collection. Rebuilding depends on those shared source paths and the sibling ten-paper dataset. The standalone exports can be consumed without the original PDFs or vector index.

## Evaluation boundary

For an abstract-only reconstruction condition, provide only `abstracts/` and explicitly allowed textbook/reference resources to the reconstruction agent. Keep `papers/`, `equations/`, selection metadata, suggested targets, and screening evidence in evaluator-only storage. Full-paper-assisted runs should be a separate condition. Textbooks themselves can contain algorithms appearing in the selected papers, so record exactly what each condition may access.

Define paper-specific reference math, inputs, expected outputs, error tolerances, and independent classical baselines before scoring a reproduction. This export supplies no verified ground-truth code or simulation outputs. Small correctness experiments do not verify asymptotic advantage, theorem-level guarantees, or device performance.

## Validation and rebuild

```bash
python3 provenance/build_dataset.py
python3 provenance/validate_dataset.py
```

The build reads shared sources and writes only into this dataset. It uses no network, embedding model, generation model, notebook execution, or simulation. Validation checks 300 unique IDs/titles, export counts/hashes, abstract separation, math offsets/content/line numbers/context, figure/image markup removal, catalog counts, and preservation of the approved seed/textbook exports. It does not validate scientific or mathematical correctness. See `provenance/build.json` for exact statistics and `provenance/validation.json` for the final validation result.

Original source metadata and attribution are retained. These exports do not grant new redistribution permissions. The archival textbook source tree did not contain a root license file.
