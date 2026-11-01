# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Triangle finding in an unweighted n-vertex graph in the quantum query model: decide whether the graph contains a triangle and output one if so. The abstract claims query complexity O~(n^{5/4}).

Scope: Only the stated query-complexity bounds, plus a standard-background Grover search primitive over vertex triples on a tiny instance (n=4). The paper's actual combinatorial algorithm is not reconstructed, and no circuit-level details are given.

## Symbols

- $n$: number of vertices of the graph; domain: positive integer
- $G=(V,E)$: unweighted graph with |V|=n, accessed via adjacency-matrix queries; domain: simple undirected graph
- $x_{uv}$: edge indicator oracle bit; domain: {0,1}
- $T(G)$: triangle indicator function over vertex triples; domain: {0,1}
- $Q(n)$: quantum query complexity of triangle finding; domain: positive real function
- $N$: number of vertex triples, binom(n,3); domain: positive integer

## eq_1: Claimed upper bound

$$
Q_{\mathrm{unweighted}}(n)=\tilde{O}(n^{5/4})
$$

Query complexity of the new algorithm for unweighted triangle finding.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: query complexity $\tilde{O}(n^{5/4})$

## eq_2: Previous upper bound

$$
Q(n)=O(n^{9/7})=O(n^{1.285\ldots})
$$

Previous bound by Lee, Magniez and Santha, which is improved.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: $O(n^{9/7})=O(n^{1.285...})$

## eq_3: Edge-weighted lower bound

$$
Q_{\mathrm{weighted}}(n)=\Omega\left(n^{9/7}/\sqrt{\log n}\right)
$$

Lower bound for edge-weighted triangle finding, attributed to Belovs and Rosmanis. It is also the bound for the non-adaptive learning graph approach.

Provenance: `abstract_explicit`. Stated in the abstract. Because 5/4 < 9/7, the new upper bound is below this weighted lower bound.

Abstract evidence: $\Omega(n^{9/7}/\sqrt{\log n})$

## eq_4: Triangle indicator

$$
T(a,b,c)=x_{ab}\wedge x_{bc}\wedge x_{ac},\quad \exists\,\{a,b,c\}: T=1 \iff G \text{ has a triangle}
$$

Predicate defining a triangle in terms of edge queries.

Provenance: `standard_background`. Definition of a triangle; the abstract does not give it.

Equation assumptions:

- Undirected simple graph

## eq_5: Grover baseline (not the paper's method)

$$
|\psi\rangle=\frac{1}{\sqrt N}\sum_{t}|t\rangle,\quad O_T|t\rangle=(-1)^{T(t)}|t\rangle,\quad k=O(\sqrt{N})
$$

Generic Grover search over triples with 3 edge queries per oracle call. It gives O(n^{3/2}) queries, worse than the claimed bound.

Provenance: `assumption`. A simple baseline construction chosen for the tiny instance; it is not the abstract's algorithm.

Equation assumptions:

- At most one marked triple, or known number of marked triples
- Oracle evaluates T with 3 edge queries

## Registers

- triple: ceil(log2 N) qubits (n=4: N=4, 2 qubits) qubits; index of the candidate vertex triple
- edge_ancilla: 3 qubits (assumed) qubits; holds the queried edge bits for the oracle, then uncomputed
- phase: 1 qubit qubits; phase-kickback target

## Initial state

Uniform superposition over triple indices (assumed baseline); ancillas in |0>, phase qubit in |->.

## Measurement

Measure the triple register in the computational basis, then classically verify the triple with 3 edge queries (baseline only).

## Classical postprocessing

Verify the candidate triangle; repeat if verification fails.

## Algorithm steps

1. Prepare the uniform superposition over the N candidate triples. (eq_5)
2. Apply the oracle O_T, which queries the three edges of each triple and flips the phase if all are present. (eq_4, eq_5)
3. Apply the Grover diffusion operator and repeat O(sqrt(N)) times. (eq_5)
4. Compare the baseline cost with the claimed algorithm's cost. (eq_1, eq_2, eq_3)

## Assumptions

- No experiment_scope was provided; the smallest useful construction is a Grover baseline on n=4 vertices.
- The Grover baseline is not the paper's algorithm and does not achieve O~(n^{5/4}).
- The adjacency-matrix query model is assumed.

## Missing information

- The paper's combinatorial algorithm, including its subroutines, parameters and data structures.
- Its query-complexity analysis and any quantum walk or learning-graph details.
- Failure probability and the logarithmic factors hidden in the tilde notation.
- The lower-bound proofs, which are only cited.
