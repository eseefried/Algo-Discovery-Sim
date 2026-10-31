# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Physical mapping of fault-tolerant quantum circuits: jointly handle operation scheduling, placement and qubit routing to minimize circuit latency, and select the single best Universal Logic Block (ULB) size for a target circuit by weighting per-operation latencies by their critical-path frequency.

Scope: Classical CAD-style mapping flow (loose force-directed scheduling, timing-driven placement, dynamic routing latency) plus ULB size selection. Not a quantum algorithm with a state-preparation or measurement circuit; only a tiny finite weighted-latency illustration is reconstructed. Specific force formulas, cost functions and benchmarks are not in the abstract.

## Symbols

- $s$: Candidate ULB size; domain: positive integer
- $L_{o,s}$: Latency of FT operation type o mapped onto ULB size s; domain: positive real
- $f_{o}$: Critical-path occurrence frequency of operation type o; domain: [0,1]
- $L_{s}$: Frequency-weighted latency of ULB size s; domain: positive real

## eq_1: Weighted ULB latency

$$
L_{s}=\sum_{o} f_{o}\,L_{o,s}
$$

Critical-path-frequency-weighted latency of ULB size s.

Provenance: `abstract_inferred`. Abstract describes weighting per-operation latencies by critical-path frequency; the linear weighted-sum form is an inference.

Abstract evidence: using information about the occurrence frequency of operations on critical paths of the target quantum algorithm to weigh these latencies

Equation assumptions:

- Linear weighted sum is assumed

## eq_2: Best ULB size

$$
s^{*}=\arg\min_{s} L_{s}
$$

Select the ULB size with minimum weighted latency.

Provenance: `abstract_inferred`. Choosing the single best size by minimizing weighted latency is implied.

Abstract evidence: determine the single best ULB size for a target quantum circuit

Equation assumptions:

- Minimization over a finite candidate set

## Registers

- QDFG: number of logical qubits and operations, unknown qubits; Quantum data flow graph with explicit no-cloning edges, processed classically
- ULB grid: unknown qubits; Candidate physical blocks for placement and routing

## Initial state

No quantum state; input is a quantum data flow graph of a target FT circuit and a set of candidate ULB sizes.

## Classical postprocessing

Compute weighted latency L_s per candidate size and pick the argmin; the 40% latency reduction is a reported result, not a derived formula.

## Algorithm steps

1. Loose scheduling: transform the initial QDFG into one that explicitly captures no-cloning, then run modified force-directed scheduling to reduce resource contention and latency. (no equation reference)
2. Placement: timing-driven placement minimizing approximate routing latencies, iteratively calling the force-directed scheduler to correct scheduling levels. (no equation reference)
3. Routing: compute dynamic routing latencies for qubits given the placement. (no equation reference)
4. ULB sizing: map FT operations onto each candidate ULB size, weight latencies by critical-path frequency, and choose the minimizing size. (eq_1, eq_2)

## Assumptions

- Weighted-sum latency model is an assumed instance
- Registers describe classical data structures, not qubit registers
- The mapping flow is classical, so there is no quantum measurement

## Missing information

- Force-directed scheduling force definitions
- Placement cost function and routing model
- ULB candidate sizes, benchmarks and baseline details
- Quantitative latency model of the ULB and FT operations
