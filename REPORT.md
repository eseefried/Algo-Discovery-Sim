# Qatalyst: goals, agent configurations, and results

**Results snapshot:** November 1, 2026, 11:21:52 a.m. EST (America/New_York).  
**Scope:** Sonnet single-agent and swarm benchmarks, native Nemotron experiments, and the Nemotron–Sonnet hybrid. Fable results are excluded. The historical Sonnet comparison is complete; the newer native and hybrid batches are partial. All figures below describe saved artifacts at this snapshot.

## 1. Goal

Determine how much of a published quantum algorithm an AI system can reconstruct **from the paper's abstract alone**: mathematical equations, a concrete circuit specification, executable Qiskit code, and simulation results. Compare a single specification-writing agent with cooperating agents, and test whether method diversity, execution feedback, independent-agent review, and an energy economy improve the outcome.

The corpus contains 300 quantum-computing papers; the main historical comparison uses 96 paper IDs. Agents receive abstracts, while full texts and labelled main equations are reserved for evaluation. Reconstruction can use model background knowledge and explicit assumptions, so success does not establish discovery of previously unknown mathematics.

The pipeline is:

```text
Abstract → mathematical specification → Qiskit generation → Docker build → Aer simulation
                    ↓                                           ↓
          paper-equation comparison                  execution and scoped functional checks
```

Sources: [project overview](README.md), [pipeline](docs/pipeline.md), [labelled main equations](evaluation/main_equations.json).

## 2. What each result measures

| Measure | Meaning | Limit |
|---|---|---|
| Math score | Chance-adjusted equation similarity: `(F1 − control F1) / (1 − control F1)`; control compares against 20 other papers. | Lexical and structural matching, not mathematical equivalence. |
| Main equations recovered | One-to-one matches to labelled main paper equations at similarity ≥ 0.70. | Matching an equation does not reconstruct the whole method. |
| Reached simulation | Generated circuit passed the build stage and was simulated. | Execution alone does not establish correctness. |
| Hybrid `ready` | Candidate executed successfully and another agent outside its implementation chain approved it. | Model review is not an independent functional test. |
| Functional check | Explicit numerical checks against a stated small-instance contract. | Applies only to that contract and tested instances. |

Pairwise equation similarity combines IDF-weighted token Dice and variable-masked sequence similarity equally. The large paper benchmark has no general ground-truth circuits or outputs; exact algorithm correctness was not scored. Sources: [single-agent evaluation metadata](baseline_sonnet/eval/summary.json), [swarm evaluation metadata](a2m_full/results/eval/summary.json).

## 3. Agent configurations

These are the settings used by the experiments, distinguished from newer CLI defaults. Recorded model IDs are reproduced as stored in the repository.

| System | Models and effort | Agent organization | Resources and selection |
|---|---|---|---|
| Single-agent Sonnet | `claude-sonnet-5-5`, medium for specification; high for code. | One abstract-to-specification call, followed by the shared code stage. | 16,384 output-token cap per stage; 96-paper cohort. |
| Ledger swarm | Sonnet 5.5, medium for reconstruction; Sonnet/high for code. | Three initial worker processes bid on dependent contracts in a shared SQLite ledger: problem, equations, circuit plan, measurement, audit. A supervisor can replace workers. | Batch reconstruction call limit defaults to 6; each contribution owns up to two requirements. Final spec goes through the shared code stage. |
| Abstract2Method (a2m) | Sonnet 5.5/medium for swarm actions; Sonnet/high for build feedback and final code. | Six initial agents, up to ten active agents; shared candidates and task index; hypothesis, implementation, simulation, and critique roles. Individual energy and lineage. | $0.50 nominal search budget per paper, 25 maximum ticks, at least three method families, one required critique, stop target of two ready candidates. Final code stage adds cost. Seed 0. |
| Native Nemotron baseline | Local `nemotron-quantum` numbered-LaTeX generator; Sonnet/high for code. | One local generator proposes equations. A conservative converter stores them as unverified assumptions without inventing registers or algorithm steps. | Greedy decoding, repetition penalty 1.12, one block, 2,048 output tokens. Sonnet code cap 16,384 tokens. Planned 96 papers. |
| Native hybrid swarm | Local Nemotron for equations; Sonnet/medium for plans, assembly and review; Sonnet/high for code. | Three logical agents share services on one host. Two can participate in implementation chains; one remains available for independent review. | 300-second nominal paper limit, $0.50 estimated paid limit, 24 total model calls, seed 0. Planned 65 papers. First reviewed success ends the run. |

The a2m search configuration uses 6 initial energy units, a spawn threshold of 14, and spawn cost 6. Its saved 96 runs record **0 deaths, 0 respawns, and 12 additional spawns**; the configured survival mechanism was not exercised through deaths in that comparison.

The native hybrid uses **5 initial energy units**, up to **6 replacements**, 12 maximum ticks, two initial method plans, and validation/review priority before further expansion. Progress rewards are deferred until execution and review pass. A replacement clones a successful donor's role affinities and decoding strategy, mutating one decoding parameter; without a successful donor, it explores a fresh strategy. Energy depletion is distinct from a process crash and from API spending.

Initial native decoding profiles are:

| Profile | Temperature | Repetition penalty | Start equation |
|---|---:|---:|---:|
| 1 | 0.00 | 1.12 | 1 |
| 2 | 0.35 | 1.08 | 1 |
| 3 | 0.60 | 1.18 | 9 |

Nemotron uses the fine-tuned `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-BF16` base with reasoning disabled. The verified training task is abstract-to-numbered-LaTeX, not JSON specification or Qiskit generation. The documented preparation audit found no overlap between the adapter's 150 training/validation paper IDs and the 96 benchmark IDs; this does not establish absence of base-model pretraining exposure.

Limits are checked between actions, so in-flight calls can exceed time or spending caps. Local generation is serialized through a shared GPU service. Hybrid agents are logical workers on one host, not a distributed fault-tolerant service.

Configuration sources: [single-agent artifacts](baseline_sonnet/), [ledger runs](swarm_full/runs/), [ledger design](docs/ledger-swarm.md), [a2m configuration](configs/systems/swarm.yaml), [a2m run summaries](a2m_full/runs/), [native baseline plan](artifacts/nemotron_native_full/plan.json), [hybrid configuration](configs/systems/nemotron_native_swarm.yaml), [actual hybrid batch plan](artifacts/native_swarm_65/plan.json), [native implementation](src/algo_discovery/native_swarm.py), [Nemotron training and serving notes](docs/nemotron-swarm.md).

## 4. Completed Sonnet benchmark

Math comparisons below use the **same 84 papers**, containing **320 labelled main equations**, for all three systems. Simulation totals use the entire **96-paper attempted cohort**. Costs cover saved calls across the corresponding experiment, not just the common 84 papers.

| System | Mean math score, common 84 | Main equations recovered, common 84 | Simulated, entire 96 | Estimated API cost |
|---|---:|---:|---:|---:|
| Single-agent Sonnet | 0.1833 | 54 / 320 (16.9%) | 77 / 96 (80.2%) | $7.52 |
| Ledger swarm | 0.1074 | 26 / 320 (8.1%) | 48 / 96 (50.0%) | $13.67 |
| Abstract2Method swarm | 0.1701 | 46 / 320 (14.4%) | 93 / 96 (96.9%) | $61.97 |

**Finding:** single-agent Sonnet recovered the most matching mathematics at the lowest cost. A2m produced 16 more simulated circuits than the single agent, at approximately **8.2× the total cost**. Its use of build feedback during search favors executable candidates. Ledger decomposition performed worse on both equation recovery and simulation yield in this experiment.

On the common 84 papers alone, simulated counts were **69 single-agent, 47 ledger, and 81 a2m**. This keeps the denominator distinct from the full-cohort simulation column above.

The saved evaluation summaries also report their own available-score cohorts; these should not be substituted into the matched comparison:

| System | Papers with math scores | Mean on that system's scored cohort | Main equations recovered on that cohort |
|---|---:|---:|---:|
| Single-agent Sonnet | 92 | 0.1889 | 60 / 354 |
| Ledger swarm | 87 | 0.1112 | 28 / 330 |
| Abstract2Method swarm | 96 | 0.1711 | 55 / 368 |

Estimated spending breaks down as follows:

| System | Specification or swarm search, including internal feedback | Final code generation | Total |
|---|---:|---:|---:|
| Single-agent Sonnet | $2.66 | $4.86 | $7.52 |
| Ledger swarm | $10.33 | $3.34 | $13.67 |
| Abstract2Method swarm | $55.37 | $6.60 | $61.97 |

Cost estimates use saved usage and the repository's Sonnet rates ($2 per million input tokens and $10 per million output tokens), plus recorded a2m search charges. They are not verified invoices. No cache-read usage is present in these saved final pipeline calls. Search and final-code spending are added once; external-spec import records carry zero model usage.

Sources: per-paper [single-agent scores](baseline_sonnet/eval/math_scores.csv), [ledger scores](swarm_full/results/eval/math_scores.csv), [a2m scores](a2m_full/results/eval/math_scores.csv); corresponding `result.json`, ledger `model_calls`, and a2m `summary.json` usage; [repository cost accounting](src/a2m/llm/client.py).

## 5. Native Nemotron baseline: partial batch

At the snapshot, **75 of 96 planned papers** had completed pipeline records.

| Outcome | Count |
|---|---:|
| Generated code and simulated | 23 / 75 (30.7%) |
| Code stage abstained with `insufficient_information` | 51 / 75 |
| Native equation stage failed contiguous-numbering validation | 1 / 75 |
| Accepted numbered equation predictions across saved native results | 205 |
| Native outputs ending with the completion marker | 56 / 75 |
| Estimated paid Sonnet code usage | $1.72 |

The 205 predictions are also 205 unique equations when duplicates are checked **within each paper**. This is a format statistic, not a scientific-quality score. No comparable paper-equation scoring summary was saved for this batch. Local inference records $0 API spending; hardware and serving costs are excluded.

Sources: [batch plan](artifacts/nemotron_native_full/plan.json), [completed-paper logs](artifacts/nemotron_native_full/logs/), [native outputs](artifacts/nemotron_native_full/native/), [code artifacts](artifacts/nemotron_native_full/results/).

## 6. Native hybrid swarm: partial batch

The directory name `native_swarm_65` describes the planned cohort. At this snapshot, **21 / 65 papers** were completed, with **15 reviewed-ready** and **6 without a reviewed candidate**. The other 44 papers have no completed outcome in this report and are excluded from the readiness rate.

| Measure | Completed-run result |
|---|---:|
| Reviewed-ready rate | 15 / 21 (71.4%) |
| Candidate methods retained in run snapshots | 67 |
| Candidate final states | 15 ready; 2 passing; 3 implemented; 14 sketch; 33 failing |
| Total recorded model calls | 217 |
| Agent records, including replacements | 72 |
| Energy-depletion deaths | 13 |
| Replacement agents | 9 |
| Median per-paper wall time | 156.33 seconds |
| Sum of per-paper wall times | 4,302.70 seconds (71.7 minutes) |
| Estimated paid Sonnet usage | $6.137112 |
| Mean estimated paid usage per completed paper | $0.2922 |

Deaths need not equal replacements: a budget or terminal condition can stop a run before population restoration. Summed per-paper times are not a controlled throughput comparison because local clients can share the GPU.

**Attribution:** the 53 saved native-evidence records contain 250 proposed equations and 256 assembled equations. The saved normalized textual comparison counts **0 native equations retained verbatim**. The 15 selected candidates contain 72 assembled equations, again with **0 retained verbatim**. Sonnet therefore supplied substantial reconstruction and repair. These data do not demonstrate a benefit from the Nemotron adapter; textual non-retention alone also cannot rule out indirect influence. A matched Sonnet-only ablation would be needed to measure that contribution.

On the **same 21 paper IDs**, the native single-generator baseline reached simulation on **6**, while the hybrid reached reviewed-ready on **15**. The endpoints, information added during assembly, and budgets differ, so this is descriptive rather than a controlled causal comparison. Neither native system has a saved math-score evaluation comparable to section 4.

Sources: [per-paper hybrid logs](artifacts/native_swarm_65/logs/), each run's `summary.json`, `all_candidates.json`, and `native_evidence.json` under [hybrid runs](artifacts/native_swarm_65/runs/). The aggregate batch summary may advance after this dated report.

### Completed-paper outcomes

`ready` means execution plus model review. Candidate IDs are local to each paper. Deaths and replacements describe virtual-energy lifecycle events.

| Paper | Outcome | Selected candidate | Seconds | Estimated API USD | Deaths / replacements |
|---|---|---|---:|---:|---:|
| 0704.0516 | no reviewed candidate | — | 302.95 | $0.4706 | 2 / 2 |
| 0704.3628 | no reviewed candidate | — | 366.44 | $0.5143 | 1 / 0 |
| 0705.0017 | ready | c001 | 91.59 | $0.1364 | 0 / 0 |
| 0710.2630 | no reviewed candidate | — | 337.31 | $0.4389 | 1 / 0 |
| 0710.3196 | ready | c003 | 156.33 | $0.2543 | 0 / 0 |
| 1105.3310 | no reviewed candidate | — | 313.47 | $0.4200 | 1 / 0 |
| 1105.5485 | ready | c003 | 277.89 | $0.4329 | 1 / 1 |
| 1105.5831 | ready | c003 | 135.95 | $0.2513 | 0 / 0 |
| 1106.4267 | ready | c001 | 119.84 | $0.1576 | 0 / 0 |
| 1204.5937 | ready | c001 | 119.01 | $0.1569 | 0 / 0 |
| 1204.6021 | ready | c001 | 93.50 | $0.1360 | 0 / 0 |
| 1205.0036 | ready | c005 | 297.15 | $0.4551 | 1 / 1 |
| 1205.0217 | ready | c002 | 115.00 | $0.1599 | 0 / 0 |
| 1404.4509 | ready | c003 | 208.96 | $0.3094 | 0 / 0 |
| 1404.5320 | no reviewed candidate | — | 343.75 | $0.3067 | 2 / 2 |
| 1404.6206 | ready | c005 | 299.86 | $0.4147 | 2 / 2 |
| 1405.2696 | no reviewed candidate | — | 309.03 | $0.4305 | 2 / 1 |
| 1405.2749 | ready | c001 | 110.50 | $0.1872 | 0 / 0 |
| 1405.5205 | ready | c001 | 79.81 | $0.1383 | 0 / 0 |
| 1405.5897 | ready | c003 | 132.94 | $0.2252 | 0 / 0 |
| 1405.6049 | ready | c001 | 91.42 | $0.1407 | 0 / 0 |

## 7. Concrete examples and independent checks

### Grover search: visualization example

Paper **0710.3196**, selected candidate **c003**, built and simulated a four-qubit Grover circuit with `n=4`, marked value `w=5`, three iterations, and zero optional error angle (`phi=0`). The saved probability of **`0101` is 0.9613189697**; each of the other 15 states has probability approximately 0.0025787354. The run reached `ready` in **156.33 seconds**, with estimated paid usage **$0.254344** and no agent deaths.

This is a useful demonstration of a complete proposal–repair–execution–review path. The saved histogram is a simulation result for one instance; it does not establish the paper's full gate-error claims. Evidence: [paper run record](artifacts/native_swarm_65/logs/0710.3196.json), [visualization candidate data](artifacts/swarm_viz_export/candidates.csv), [probabilities](artifacts/swarm_viz_export/probabilities.csv).

### Affine identification: scoped functional success

The corrected hybrid pilot for **1407.6402**, candidate **c002**, recovered both coefficients in `f(x)=a·x ⊕ b` for **28 / 28 parameter instances** across one to three data qubits. For `n=2`, `a=1`, `b=1`, the saved Aer rerun returned **`101` in all 1,024 shots**. The paper run took **263.02 seconds** and estimated paid usage **$0.307616**.

The oracle parameters are explicit gate-construction inputs, and controlled-phase-oracle access is assumed. The checks establish this finite functional contract, not black-box query complexity, equivalence to the original paper's method, or its incompletely defined-function claims. This pilot is separate from the 21-paper batch totals.

The earlier native single-generator circuit for the same paper passed coefficient-recovery checks on 28 instances and 168 basis columns, but **could not recover `b`**, which appeared only as global phase. It must not be described as complete affine identification.

Evidence: [full examples and artifact links](EXAMPLES.md), [selected hybrid checks](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/example_correctness.json), [native pilot evaluation](artifacts/nemotron-e2e-report/results.json).

### Order finding: execution without approval

For **0704.0516**, a small `N=15` candidate built and simulated, but review requested alignment of work-register initialization across the spec, circuit, and runner. The saved default-input preview concentrated on `00000000`. The run ended without a reviewed candidate after **302.95 seconds**, with **two deaths and two replacements**, costing an estimated **$0.470608**.

The reviewer objection was not independently reproduced as a valid-instance numerical counterexample. This remains an unresolved reconstruction, not a certified algorithmic failure. Evidence: [run record](artifacts/native_swarm_65/logs/0704.0516.json), [code and recorded review](EXAMPLES.md).

## 8. Visualization export and excluded experiments

The [visualization export](artifacts/swarm_viz_export/README.md) is an earlier fixed snapshot, exported November 1 at **11:10:40 a.m. EST**. It contains **16 completed papers, 11 ready outcomes, 56 agents, 471 events, 54 candidates, and 97 probability rows**. It therefore differs from the later 21-paper report snapshot. The CSV files support run selection, replay, lineage, method cards, code/review links, and probability histograms. Preserve the entire folder for relative artifact links. Join by global `agent_key` and `candidate_key`; replay by `elapsed_seconds`, using `sequence` to break ties.

The [first hybrid pilot](artifacts/native_swarm_pilot/INVALID_HARNESS.md) is excluded from quality results because it used incompatible opaque-oracle reviewer instructions for the actual Docker worker. Its recorded $0.504794 is also excluded from the corrected pilot and batch totals. Earlier JSON-spec Nemotron smoke tests requested a format outside the adapter's verified training task; they are not treated as native-task benchmark results. Scripted mock runs and the seven curated development tasks do not provide held-out evidence for the 96-paper reconstruction comparison.

## 9. Conclusions and remaining evidence gaps

1. **Single-agent Sonnet is the strongest measured cost–math tradeoff** in the completed same-model benchmark: 0.1833 common-cohort math score and 54 / 320 equations at $7.52.
2. **A2m improves execution yield**, reaching simulation on 93 / 96 papers, with lower equation recovery and higher cost than the single agent.
3. **The hybrid exposes an inspectable repair and review process**, including energy depletion and replacement. Its current 15 / 21 readiness result is a partial-batch engineering outcome.
4. **A small affine example has independent functional evidence**, while general correctness across the paper cohort remains unmeasured.
5. **Nemotron's incremental contribution is unestablished**: selected hybrid equations were rewritten or supplied by Sonnet, and a matched ablation has not been run.

These experiments use single runs and unequal budgets. The current evidence does not establish statistical significance, an evolutionary advantage, hardware-inclusive cost efficiency, or full-paper reproduction. Completing the planned batches, scoring the new systems on a common paper cohort, running independent functional contracts, and repeating budget-matched seeds would address those gaps.

### How the report was checked

Historical math statistics were recomputed from the intersection of the three non-Fable `math_scores.csv` files (84 IDs). Simulation totals were checked against saved evaluation summaries. Costs were summed from saved model usage, ledger calls, and a2m search charges. New-batch counts use only paper logs with completion markers; hybrid lifecycle, candidates, and attribution were aggregated from those runs. No new paid experiments were launched to prepare this report.
