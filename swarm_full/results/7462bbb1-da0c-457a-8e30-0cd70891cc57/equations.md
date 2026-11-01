# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Triangle finding in unweighted n-vertex graphs in the quantum query model: find a triangle (or decide none exists) using few adjacency-matrix queries. The abstract claims a quantum algorithm with query complexity O~(n^{5/4}), improving the prior O(n^{9/7}) bound of Lee, Magniez and Santha.

Scope: Query-complexity statement only. The abstract gives no circuit, registers, or measurement details, so only the problem and the stated complexity bounds are reconstructed.

## Symbols

- $n$: number of vertices in the graph; domain: positive integers
- $Q$: quantum query complexity of triangle finding; domain: nonnegative reals as a function of n

## eq_1: New upper bound

$$
Q_{\mathrm{unweighted}}(n)=\tilde{O}(n^{5/4})
$$

Query complexity of the new quantum algorithm for unweighted triangle finding.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: query complexity $\tilde{O}(n^{5/4})$

## eq_2: Previous upper bound

$$
Q_{\mathrm{prev}}(n)=O(n^{9/7})
$$

Earlier learning-graph upper bound by Lee, Magniez and Santha.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: $O(n^{9/7})=O(n^{1.285...})$

## eq_3: Edge-weighted lower bound

$$
Q_{\mathrm{weighted}}(n)=\Omega\!\left(n^{9/7}/\sqrt{\log n}\right)
$$

Belovs-Rosmanis lower bound for finding an edge-weighted triangle, which separates weighted from unweighted triangle finding.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: $\Omega(n^{9/7}/\sqrt{\log n})$ queries

## Registers

- vertex/query registers: unknown (assumed O(log n) qubits per vertex index) qubits; Assumed: hold vertex indices for adjacency-matrix oracle queries
- answer/work register: unknown qubits; Assumed: store candidate edges or a triangle found and the oracle output bit

## Initial state

Assumed: uniform superposition over vertex indices with the work register in the all-zero state; the abstract does not specify this.

## Measurement

Not specified in the abstract. Assumed: measure the output register at the end to obtain a candidate triple of vertices, or a 'no triangle' flag.

## Classical postprocessing

Assumed: classically check the three candidate edges with adjacency queries to confirm a triangle; repeat on failure to boost success probability. Not given in the abstract.

## Algorithm steps

1. Use combinatorial graph-theoretic ideas (unspecified in abstract) to reduce the search space and choose candidate vertex sets or edges, with adjacency queries to the oracle. (eq_1)
2. Run quantum query subroutines (details not given in the abstract) to find a triangle or conclude none exists, within about n^{5/4} queries up to polylog factors. (eq_1, eq_2)

## Assumptions

- Registers, initial state and steps are generic placeholders, not from the abstract
- Generic query-model registers and initial state assumed; not from the paper
- Measurement and verification of a candidate triangle are assumed generic, not from the abstract

## Missing information

- Algorithm construction is not in the abstract
- Registers, oracle and circuit details
- Actual measurement and classical postprocessing of the paper
- Abstract does not describe the combinatorial ideas or the quantum subroutines used
