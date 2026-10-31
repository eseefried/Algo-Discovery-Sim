# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Triangle finding in an unweighted, undirected n-vertex graph G=(V,E) accessed through an adjacency-matrix query oracle: decide whether there exist three distinct vertices u,v,w with {u,v},{v,w},{u,w} all in E (and output such a triple if it exists). The abstract claims a quantum algorithm with query complexity \tilde{O}(n^{5/4}), improving the O(n^{9/7}) learning-graph bound of Lee, Magniez and Santha, and separating unweighted from edge-weighted triangle finding (for which an \Omega(n^{9/7}/\sqrt{\log n}) lower bound is known).

Scope: The abstract states only the problem, the query model implicitly, and the complexity bounds; it does not describe the algorithm's construction (its combinatorial decomposition, use of random vertex subsets, sparsification, or nested quantum-walk subroutines). Therefore the scoped reconstruction is: (i) a precise statement of the query model, the triangle predicate, and the claimed/comparison bounds; and (ii) ONE smallest useful concrete construction, chosen as an assumption: a textbook Grover search over vertex triples on a tiny explicit instance (n=4, vertices {0,1,2,3}, edges {01,02,12,23}, exactly one triangle {0,1,2}), which uses O(n^{3/2}) queries and is NOT the paper's \tilde{O}(n^{5/4}) algorithm. Outside scope: the paper's actual combinatorial algorithm, its analysis achieving n^{5/4}, the learning-graph lower bound argument, and the edge-weighted lower bound of Belovs and Rosmanis.

## Symbols

- $n$: number of vertices of the input graph; domain: positive integer
- $V$: vertex set, identified with \{0,\dots,n-1\}; domain: finite set of size n
- $E$: edge set of the undirected unweighted graph G=(V,E); domain: subset of unordered pairs of V
- $A$: adjacency matrix of G, A[u,v]=1 iff \{u,v\}\in E, symmetric with zero diagonal; domain: \{0,1\}^{n\times n}
- $O_G$: quantum query oracle giving access to entries of A; domain: unitary on \mathbb{C}^{n}\otimes\mathbb{C}^{n}\otimes\mathbb{C}^{2}
- $f(u,v,w)$: triangle predicate: 1 iff \{u,v,w\} is a triangle of G; domain: \{0,1\}, for distinct u,v,w\in V
- $Q(\mathrm{Tri}_n)$: bounded-error quantum query complexity of triangle finding on n-vertex graphs; domain: nonnegative real function of n
- $\tilde{O}(\cdot)$: big-O notation suppressing polylogarithmic factors in n; domain: asymptotic notation
- $N$: number of candidate vertex triples searched by the baseline construction, N=\binom{n}{3}; domain: positive integer
- $M$: number of triangles (marked triples) in the instance; domain: nonnegative integer, M\le N
- $k$: number of Grover iterations in the baseline construction; domain: nonnegative integer
- $|\psi_0\rangle$: uniform superposition over the N candidate triples; domain: unit vector in \mathbb{C}^{N}

## eq_1: Adjacency-matrix query oracle

$$
O_G\,|u\rangle|v\rangle|b\rangle = |u\rangle|v\rangle|b\oplus A[u,v]\rangle,\qquad u,v\in V,\; b\in\{0,1\}
$$

Standard quantum query oracle for graph problems in the adjacency-matrix model; one application counts as one query. Query complexity in the abstract is counted with respect to such an oracle.

Provenance: `standard_background`. Triangle finding query complexity results of this line of work (including the cited O(n^{9/7}) bound) are stated in the adjacency-matrix query model; the abstract mentions query complexity but does not define the oracle, so this is recalled background.

Equation assumptions:

- Adjacency-matrix (edge-query) model rather than adjacency-list model.

## eq_2: Triangle predicate

$$
f(u,v,w) = A[u,v]\wedge A[v,w]\wedge A[u,w],\qquad u,v,w\in V \text{ pairwise distinct}
$$

Exact Boolean definition of when a triple of vertices forms a triangle; the triangle finding problem asks whether some triple has f=1 (and to output it). Evaluating f on one triple costs exactly 3 queries to O_G.

Provenance: `abstract_inferred`. Inferred from the problem name: a triangle in an unweighted graph is a 3-clique; the abstract does not spell out the predicate.

Abstract evidence: solving the triangle finding problem in unweighted graphs

Equation assumptions:

- Simple undirected graph (symmetric A, no self-loops).

## eq_3: Claimed upper bound and comparison bounds

$$
Q(\mathrm{Tri}_n) = \tilde{O}(n^{5/4}),\qquad n^{5/4} = o\!\left(n^{9/7}\right),\qquad Q(\mathrm{Tri}^{\mathrm{weighted}}_n) = \Omega\!\left(n^{9/7}/\sqrt{\log n}\right)
$$

The abstract's main claim (first relation), the fact that it improves the previous O(n^{9/7}) bound (second relation, since 5/4=1.25<9/7\approx1.2857), and the quoted lower bound for the edge-weighted variant and for non-adaptive learning-graph algorithms (third relation). These are asymptotic statements, not exact equalities.

Provenance: `abstract_explicit`. Directly stated in the abstract; the weighted lower bound is quoted from the abstract's attribution to Belovs and Rosmanis.

Abstract evidence: query complexity $\tilde{O}(n^{5/4})$, where $n$ denotes the number of vertices in the graph. This improves the previous upper bound $O(n^{9/7})=O(n^{1.285...})$

Equation assumptions:

- Bounded-error (e.g. success probability at least 2/3) query complexity, as is standard.

## eq_4: Baseline Grover search over triples (scoped construction, not the paper's algorithm)

$$
|\psi_0\rangle = \frac{1}{\sqrt{N}}\sum_{\{u,v,w\}} |u,v,w\rangle,\quad N=\binom{n}{3},\qquad U_f|u,v,w\rangle = (-1)^{f(u,v,w)}|u,v,w\rangle,\qquad \mathcal{G} = \left(2|\psi_0\rangle\langle\psi_0| - I\right)U_f
$$

Phase-oracle Grover iterate over all unordered vertex triples. Each U_f costs 3 queries to O_G (compute the three edge bits via eq_1 into ancillas, AND them into a phase, uncompute). This is the smallest useful construction consistent with the problem; it is a textbook baseline chosen because the abstract gives no construction details of the n^{5/4} algorithm.

Provenance: `assumption`. No experiment_scope was supplied, so one minimal construction is chosen and labelled as an assumption; it reproduces the problem semantics (eq_2) but not the paper's complexity.

Equation assumptions:

- Grover search over triples is used purely as a baseline; the paper's combinatorial algorithm is different and not reconstructable from the abstract.

## eq_5: Grover iteration count and baseline query cost

$$
k = \left\lfloor \frac{\pi}{4}\sqrt{\frac{N}{M}} \right\rfloor \;(M\ge 1),\qquad \Pr[\text{measure a triangle}] = \sin^2\!\big((2k+1)\theta\big),\; \sin\theta=\sqrt{M/N},\qquad \text{queries} = 3k = O\!\left(n^{3/2}\right)
$$

Standard Grover analysis for the baseline: with M unknown one uses exponential guessing of M or amplitude estimation, still O(\sqrt{N}) iterations. For the tiny instance N=4, M=1: \theta=\pi/6, k=1 and the success probability is \sin^2(\pi/2)=1 exactly. The resulting O(n^{3/2}) is strictly worse than the abstract's \tilde{O}(n^{5/4}).

Provenance: `standard_background`. Standard Grover/amplitude-amplification facts; included to make the baseline construction executable and to make explicit the gap to the claimed bound.

Equation assumptions:

- Floor in k is a rounding choice; success probability is exact only when (2k+1)\theta=\pi/2.

## eq_6: Tiny explicit instance

$$
n=4,\; V=\{0,1,2,3\},\; E=\{\{0,1\},\{0,2\},\{1,2\},\{2,3\}\},\qquad \text{triples indexed } t\in\{0,1,2,3\}:\; t_0=\{0,1,2\},\,t_1=\{0,1,3\},\,t_2=\{0,2,3\},\,t_3=\{1,2,3\},\qquad f(t)=[t=t_0]
$$

Concrete instance with exactly one triangle. The triple index t is stored in a 2-qubit register with big-endian binary encoding (|t\rangle=|t_1 t_0\rangle, t = 2t_1+t_0); the triple-to-vertices map is a fixed classical table used inside U_f.

Provenance: `assumption`. Chosen as the smallest nontrivial instance (N=4, M=1) for which one Grover iteration succeeds with probability exactly 1.

Equation assumptions:

- Instance and index encoding are arbitrary choices for the baseline.

## Registers

- triple_index: 2 (general: \lceil \log_2 \binom{n}{3} \rceil) qubits; Holds the index t of a candidate vertex triple {u,v,w}; the search register of the baseline Grover construction (eq_4, eq_6).
- edge_bits: 3 qubits; Ancillas receiving A[u,v], A[v,w], A[u,w] via three applications of O_G (eq_1); uncomputed after use.
- phase_ancilla: 1 qubits; Prepared in |-\rangle so that writing f=A[u,v]\wedge A[v,w]\wedge A[u,w] into it implements the phase oracle U_f of eq_4.

## Initial state

|0\rangle^{\otimes 2}_{\text{triple\_index}}\otimes|000\rangle_{\text{edge\_bits}}\otimes|1\rangle_{\text{phase\_ancilla}}; after H^{\otimes 2} on triple_index and H on phase_ancilla this becomes |\psi_0\rangle\otimes|000\rangle\otimes|-\rangle with |\psi_0\rangle=\frac12\sum_{t=0}^{3}|t\rangle.

## Measurement

Measure triple_index in the computational basis to obtain an index t; for the tiny instance the outcome is t=0 (triangle {0,1,2}) with probability exactly 1 after k=1 iteration.

## Classical postprocessing

Decode t into vertices {u,v,w} via the fixed triple table (eq_6) and verify with 3 classical queries that A[u,v]=A[v,w]=A[u,w]=1; output the triangle if verified, otherwise report 'no triangle' (repeat O(1) times to boost confidence when M is unknown).

## Algorithm steps

1. Prepare the uniform superposition |\psi_0\rangle over the N=\binom{n}{3} triple indices (N=4 for the tiny instance) and the phase ancilla in |-\rangle. (eq_4, eq_6)
2. Oracle step: controlled on the triple index, query O_G three times to load A[u,v], A[v,w], A[u,w] into edge_bits; apply a Toffoli-type AND of the three edge bits into the phase ancilla (giving phase (-1)^{f}); uncompute edge_bits with three further queries (or, counting as in eq_5, 3 queries per evaluation with uncomputation folded in). This realizes U_f. (eq_1, eq_2, eq_4)
3. Apply the diffusion operator 2|\psi_0\rangle\langle\psi_0|-I on triple_index, completing one Grover iterate \mathcal{G}. (eq_4)
4. Repeat the oracle and diffusion steps k times with k=\lfloor (\pi/4)\sqrt{N/M}\rfloor; for the tiny instance k=1. If M is unknown, use the standard exponentially-increasing-iteration schedule. (eq_5)

## Assumptions

- No experiment_scope was provided, so the smallest useful construction (Grover search over vertex triples on a 4-vertex instance) was chosen; this is explicitly a baseline, not a reconstruction of the paper's \tilde{O}(n^{5/4}) algorithm.
- Adjacency-matrix query model with bounded-error success criterion.
- Simple undirected unweighted graph; triple index register uses big-endian binary encoding with a fixed classical triple table.
- All statements about the paper's algorithm beyond its complexity bound are unknown; nothing about random vertex subsets, sparsification, or nested quantum walks has been asserted as sourced.

## Missing information

- The actual structure of the \tilde{O}(n^{5/4}) algorithm: the combinatorial decomposition of the vertex set, the subroutines (e.g. which quantum walks or searches are nested), their parameters, and how the n^{5/4} exponent arises.
- The precise 'graph-theoretic properties of triangle finding' exploited and why they fail for edge-weighted graphs and for non-adaptive learning graphs.
- The hidden polylogarithmic factors in \tilde{O} and the success-probability guarantee.
- Whether the algorithm outputs a triangle or only decides existence, and its time (as opposed to query) complexity.
- The proof that non-adaptive learning-graph algorithms require \Omega(n^{9/7}/\sqrt{\log n}) queries even on unweighted graphs.
