# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantum time complexity of all pairs shortest paths (APSP) and variants on structured inputs (geometrically weighted graphs, small integer weights, few distinct weights per vertex, all pairs earliest arrivals): obtain quantum algorithms faster than the trivial O~(n^2.5) Grover-based bound, i.e. O(n^{2.5-epsilon}).

Scope: Complexity-level reconstruction only: problem statement and time bounds from the abstract. The abstract gives no circuits, registers, or measurement details, so the circuit plan and measurement are generic baseline assumptions, not the paper's algorithm.

## Symbols

- $n$: number of vertices in the graph; domain: positive integer
- $\varepsilon$: constant improvement exponent in the running time; domain: real number greater than 0

## eq_1: Trivial classical APSP time

$$
O(n^{3})
$$

Running time of the trivial classical algorithm for APSP and most all-pairs path problems.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: The trivial classical algorithm for APSP and most all pairs path problems runs in $O(n^{3})$ time

## eq_2: Trivial quantum APSP time

$$
\tilde{O}(n^{2.5})
$$

Running time of the trivial quantum algorithm using Grover search.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: the trivial algorithm in the quantum setting runs in $\tilde{O}(n^{2.5})$ time

## eq_3: Nontrivial quantum target

$$
O(n^{2.5-\varepsilon})
$$

Nontrivial quantum time bound achieved for the structured variants.

Provenance: `abstract_explicit`. The abstract defines nontrivial as this bound.

Abstract evidence: (i.e. $O(n^{2.5-\varepsilon})$ time)

## Registers

- pair_index: 2 log n qubits; Assumed register indexing a source-target pair (u,v) or a candidate intermediate vertex in a Grover search
- search: O(log n) qubits; Assumed register for Grover search over candidate intermediate vertices/neighbors, queried via an adjacency/weight oracle
- work: unknown qubits; Assumed ancilla for oracle evaluation of weights and comparisons

## Initial state

Assumed uniform superposition over the search register (Hadamard on |0...0>), with graph access through a quantum adjacency-list or matrix oracle.

## Measurement

Assumed baseline: measure the search register after Grover minimum-finding for each pair (u,v) to obtain the argmin intermediate vertex, repeating for success probability 1-1/poly(n). The paper's measurement procedure is not given in the abstract.

## Classical postprocessing

Assumed: record the minimum path weight per pair in an n x n distance matrix, using a union bound over n^2 pairs with O(log n) repetitions, which is absorbed by the tilde in the running time.

## Algorithm steps

1. For each source-target pair, prepare the uniform superposition over candidate intermediate vertices (baseline, assumed). (eq_2)
2. Apply Grover/minimum-finding with an oracle for path weights, taking about sqrt(n) iterations per pair, giving n^2 pairs times sqrt(n) = O~(n^2.5) total. (eq_2)
3. Structured-input algorithms (the paper's methods) would exploit weight structure to reduce total time to O(n^{2.5-epsilon}); details not in the abstract. (eq_3)

## Assumptions

- Circuit plan is a generic Grover-based baseline skeleton, not the paper's algorithm.
- Graph accessed via quantum adjacency-list/matrix oracle; baseline uses Grover minimum finding per pair.
- Measurement and postprocessing are generic baseline assumptions.
- Measurement and postprocessing follow the generic Grover minimum-finding baseline with repetition for error reduction.

## Missing information

- Concrete quantum algorithms, subroutines and the values of epsilon for each variant
- Circuit registers, oracle model, and measurement procedure
- Actual structure-exploiting quantum subroutines are not specified in the abstract.
- Paper's actual measurement and postprocessing for the structured variants are unspecified in the abstract.
