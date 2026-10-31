# Single-agent baseline: abstract to verified quantum experiment

Implementation status: the abstract-to-equation block is available through the CLI
and API in `src/algo_discovery/`. Qiskit generation, simulation, and independent
mathematical evaluation remain pending. The sections below describe the full baseline plan.

## Objective and scope

Accept a scientific abstract through an API. One agent produces an explicit mathematical model and a parameterized Qiskit implementation, uses local execution feedback to repair it within a fixed budget, and returns artifacts with independently measured correctness.

The initial claim is **reconstruction of a small, explicitly scoped experiment**, not automatic reproduction of every claim in a paper. An abstract often omits essential definitions, oracle constructions, phase schedules, and experimental settings. The agent must identify missing details and may return `insufficient_information` instead of inventing a paper-specific method.

“Single agent” means one model, one instruction set, and one conversation with tool access. Multiple model calls in that conversation are allowed. Math, coding, and repair are stages of that agent's work. The API controller, simulator, and deterministic evaluator are ordinary software, not additional agents.

## What is available

The canonical project dataset is `data/circuit_dataset_300_v1/`:

- 300 abstracts, 300 full-text exports, and 300 equation JSONL exports.
- 10 approved seed candidates, 160 direct circuit/algorithm candidates, and 130 candidates requiring additional encoding or protocol design.
- 110 archival textbook text exports, plus their index. Code has not been migrated to current Qiskit.
- No independently verified reference code, equation sets, or simulation outputs. Approved seeds are experiment candidates, not correctness ground truth.

The repository currently contains dataset material and a short README, with no application implementation.

## Experimental conditions and access

Start with **B0: abstract only**. The agent receives the abstract, a frozen API usage guide, resource constraints, and any explicitly supplied experiment inputs. It cannot read full papers, equation exports, catalog targets, screening evidence, evaluator implementations, or expected outputs.

Use separate conditions later:

- **B1: abstract plus textbooks.** Same agent and budgets, with retrieval over a frozen textbook corpus. Log retrieved sections; textbooks can directly describe algorithms in the evaluation set.
- **B2: full-paper assisted.** Same architecture with paper text and extracted equations available. Report separately from abstract-only reconstruction.

Enforce access with separate filesystem mounts and tool permissions. Keeping evaluator data out of the prompt while exposing the repository through a file tool would not provide an abstract-only condition. Evaluation metadata can select cases without being passed to the agent. No live web search in B0.

## Execution flow

```text
POST /experiments
    -> validate request and assign run ID
    -> one agent: assess abstract and produce math specification
    -> one agent: produce parameterized Qiskit source
    -> isolated worker: import, construct, simulate, run public checks
    -> same agent: repair using diagnostics, at most twice
    -> evaluator: run frozen checks on final source
    -> persist artifacts and return report
```

The controller owns budgets and stopping rules. It passes structured artifacts between stages and rejects malformed outputs. Hidden evaluation results do not feed back into repairs.

## Contracts

**Request:** `abstract`, optional `experiment_inputs`, and optional limits bounded by server policy. A request can contain only an abstract; chosen defaults must then appear in the response. Dataset IDs remain evaluator-side identifiers, rather than retrieval handles exposed to the agent.

**Math specification:** problem and claim being attempted; inputs and constraints; registers including ancillas; initial state; equations with defined symbols; ordered algorithm steps; measurement and classical postprocessing; predicted properties; assumptions; missing information; and chosen finite instance. Each substantive equation or construction records whether it is supported by the abstract, standard background knowledge, or an additional assumption. Preserve this as a structured JSON artifact plus readable LaTeX, without claiming an equation was extracted when it was inferred.

**Code:** a Python module exposing `build_circuit(instance) -> QuantumCircuit` and, when required, a restricted `postprocess(result, instance)` function. The interface must support multiple test inputs rather than hardcoding the agent's demonstration. The trusted runner owns simulation settings, result extraction, and resource measurement. Keep a measurement-free circuit available for exact-state checks; add final measurement in the runner where appropriate. Dynamic circuits and adaptive protocols are outside the first version.

**Response:** `run_id`, terminal status, scope and assumptions, math artifact, code artifact, selected inputs, simulation results, independent verification results, resource metrics, execution trace, and artifact locations. Distinguish `verified`, `executed_unverified`, `insufficient_information`, `unsupported`, `failed`, and `budget_exceeded`. Successful execution alone never yields `verified`. For a novel abstract with no independent reference, return execution and consistency findings as `executed_unverified`.

## Simulation and verification

Use Python, FastAPI, Pydantic, one model provider SDK, Qiskit, Qiskit Aer, NumPy, and SciPy. Begin with a plain Python orchestration loop; an agent framework and vector database are unnecessary for B0. Resolve compatible dependency versions, smoke-test them, then commit a lockfile.

Use exact statevector checks for small ideal unitary circuits and Aer sampling for measurement demonstrations. Proposed defaults: 6-qubit demonstration instances, a hard cap of 12 total qubits including ancillas, 1,024 shots, fixed simulator/transpiler seeds, 30 seconds per simulation, at most two repair attempts, and explicit token and total wall-time budgets. Enforce memory, process, circuit-size, and output limits as well as qubit count. Keep noise, hardware, training loops, and large-scale simulation out of the initial milestone.

Run generated source in an isolated worker with no network, credentials, evaluator files, or unrelated filesystem access. A plain subprocess and import filtering alone are not a security boundary. Fail closed if the deployment cannot provide the required isolation.

Verification has separate layers:

1. **Build and execution:** source imports, parameters bind, registers fit limits, circuit transpiles and runs.
2. **Mathematical correctness:** compare against an independent classical calculation or reference operator. Use fidelity up to global phase, distribution distance, or observable error as appropriate. Fix tolerances before evaluation; sampled outputs need statistical criteria rather than exact float comparisons.
3. **Paper fidelity:** assess whether the implementation matches the selected paper-specific construction and declared scope. A generic textbook substitute or opaque dense-unitary shortcut may pass functional checks while failing this layer.

Agent-written checks are useful public diagnostics. They are never the sole correctness oracle. Freeze independent evaluators and hidden cases before scored runs, and store their versions and provenance. Public task contracts specify accepted scope and inputs; hidden checks exercise those contracts without demanding details absent from the abstract and declared task.

## First experiments

First validate the execution/evaluation infrastructure using a hand-written 2–3-qubit QFT fixture against the analytical Fourier matrix. Computational-basis measurement histograms alone cannot verify its relative phases. This fixture is an infrastructure check, not evidence of paper reconstruction.

Then build three development cases from the seed collection:

| Paper | Initial finite scope | Independent check |
| --- | --- | --- |
| `1407.6402`, affine Boolean identification | Fully specified affine functions on 2–3 input bits | Exhaust all coefficients and offsets against truth tables. Recover both the linear part and affine offset; ordinary Bernstein–Vazirani recovery alone is incomplete. |
| `1411.5949`, QFT arithmetic | Two 2-bit registers, modular addition | Check all 16 basis inputs against `(a, b) -> (a, (a+b) mod 4)` and compare coherent behavior with the reference permutation. This verifies the scoped adder, not every arithmetic extension in the paper. |
| `1411.4028`, QAOA | Fixed p=1 angles on a 4-node cycle | Compare amplitudes and expected cut with independent dense Hamiltonian evolution. Exhaustive MaxCut gives the optimum for comparison; a correct QAOA implementation need not attain it. |

Read the full papers on the evaluator side to establish references. The first two are natural tiny demonstrations; QAOA adds a different algorithm family. These three are development cases and must not be presented as untouched evaluation data.

Prepare independent references for the remaining seven seed candidates before calling them a held-out benchmark. Classify unsupported cases explicitly. Expand into the 160 direct candidates only after the harness works. The corpus is an evaluation resource, not automatically a training set; no fine-tuning is needed for the first baseline.

## Metrics and reproducibility

Report attempted cases and all terminal statuses, including abstentions. Record first-attempt execution and correctness, correctness after bounded repairs, paper-fidelity outcomes, reference coverage, tokens, actual model cost, latency, repair count, total qubits, and gate/depth metrics after transpiling to a fixed basis with fixed settings. Retain raw simulator outputs as well as interpreted results.

Use a frozen model identifier, prompt version, dependency lock, evaluator version, source/abstract hashes, and random seeds. Repeat scored generations where budget permits; a simulator seed alone does not make model output reproducible. For a later multi-agent comparison, hold cases, allowed references, tools, environment, and total model/compute budget constant.

## Build order and completion criteria

1. **Reference harness:** implement the QFT smoke fixture, classical references for the three development cases, result schemas, and resource-limited execution. Done when known-correct fixtures pass and deliberately wrong phase, bit-order, affine-offset, and arithmetic implementations fail.
2. **Agent core:** implement structured math output, source generation, execution feedback, bounded repair, artifact capture, and truthful statuses. Done when the core can process an abstract through the full flow and retain useful failure reports.
3. **API:** expose `POST /experiments` and `GET /experiments/{run_id}` over the tested core; persist run metadata and artifacts locally. Return a run ID immediately if execution is asynchronous. Keep provider credentials outside worker processes.
4. **Baseline report:** freeze development prompts, evaluate independently prepared held-out cases, and report correctness alongside coverage and cost. Preserve failures and missing-information cases.

Suggested modules: `api.py`, `schemas.py`, `agent.py`, `runner.py`, `evaluation/`, `prompts/`, and `artifacts/`. Add tests for boundaries and independent scientific checks; avoid tests that merely repeat the generated implementation.

The first hackathon demo is complete when one real abstract produces inspectable equations, executable Qiskit, simulation output, an independently checked scoped result, and a saved run report. Record broader success rates only after the evaluation set is prepared and run.

## Current Qiskit references

- [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html) documents statevector and other simulation methods.
- [QFT API](https://qiskit.qotlabs.org/docs/api/qiskit/qiskit.circuit.library.QFT) marks the old `QFT` class deprecated and directs users to `QFTGate` or `synth_qft_full`. Treat archival textbook code as reference material requiring migration.
- [StatevectorSampler](https://qiskit.qotlabs.org/docs/api/qiskit/qiskit.primitives.StatevectorSampler) is another ideal sampling option, but does not support mid-circuit measurement.
