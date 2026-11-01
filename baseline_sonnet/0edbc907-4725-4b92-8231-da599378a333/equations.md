# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantum time complexity of all pairs shortest paths (APSP) and variants. Only the trivial Grover-search baseline and the complexity targets are stated in the abstract. The actual nontrivial quantum algorithms are not described.

Scope: Scoped to the trivial Grover-based quantum baseline for one primitive: finding a minimizing intermediate vertex w for a single pair (u,v) in a tiny n-vertex weighted graph, via Grover/quantum minimum finding. The paper's nontrivial O(n^{2.5-eps}) algorithms for geometric weights, small integer weights, few weights per vertex, and earliest arrivals are out of scope.

## Symbols

- $n$: number of vertices; domain: positive integer
- $w(u,v)$: edge weight, infinity if no edge; domain: nonnegative reals or infinity
- $d(u,v)$: shortest path distance; domain: nonnegative reals or infinity
- $\varepsilon$: constant improvement exponent; domain: positive real
- $k$: candidate intermediate vertex index; domain: {0,...,n-1}

## eq_1: Classical trivial and quantum trivial runtimes

$$
T_{\text{classical}}=O(n^{3}),\quad T_{\text{quantum,trivial}}=\tilde{O}(n^{2.5})
$$

Runtime of the trivial algorithms stated in the abstract.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: runs in $O(n^{3})$ time, while the trivial algorithm in the quantum setting runs in $\tilde{O}(n^{2.5})$ time

## eq_2: Target subcubic and nontrivial quantum bounds

$$
T=O(n^{3-\varepsilon})\ \text{(classical goal)},\quad T=O(n^{2.5-\varepsilon})\ \text{(quantum result)}
$$

Goals and claimed regime for improved algorithms.

Provenance: `abstract_explicit`. The classical goal is quoted. The quantum bound is also stated as nontrivial, i.e. O(n^{2.5-eps}); the quote covers the classical form only.

Abstract evidence: an algorithm running in $O(n^{3-\varepsilon})$ time for constant $\varepsilon>0$

## eq_3: Pairwise distance as a minimum over intermediates (one-step relaxation)

$$
d_{2}(u,v)=\min_{k\in\{0,\dots,n-1\}}\left[d_{1}(u,k)+w(k,v)\right]
$$

Min-plus step that APSP repeatedly uses. Grover-type minimum finding evaluates it with O(sqrt(n)) queries per pair.

Provenance: `standard_background`. Standard min-plus product formulation. Not stated in the abstract.

Equation assumptions:

- Nonnegative weights
- d_1 is the current distance estimate

## eq_4: Grover/Durr-Hoyer query cost for minimum over n items

$$
Q_{\min}=O(\sqrt{n}),\quad n^{2}\cdot\sqrt{n}=n^{2.5}
$$

Doing quantum minimum finding for each of n^2 pairs gives the n^{2.5} (up to polylog) trivial bound.

Provenance: `abstract_inferred`. The n^{2.5} count is consistent with n^2 pairs times sqrt(n) Grover cost. The per-pair decomposition is my inference, not stated.

Abstract evidence: the trivial algorithm in the quantum setting runs in $\tilde{O}(n^{2.5})$ time, using Grover search

Equation assumptions:

- Per-pair independent search
- Polylog factors hidden by tilde-O
- The trivial algorithm is read as one Grover search per pair

## Registers

- k: ceil(log2 n) qubits qubits; index of candidate intermediate vertex for a fixed pair (u,v)
- val: unknown (precision-dependent) qubits; workspace holding d(u,k)+w(k,v) for comparison

## Initial state

Uniform superposition over k: (1/sqrt(n)) sum_k |k>|0>

## Measurement

Measure the k register after minimum finding to obtain the argmin (assumed).

## Classical postprocessing

Store the minimum value for each pair (u,v) and combine into the distance matrix.

## Algorithm steps

1. Prepare the uniform superposition over candidate intermediates k for a fixed pair (u,v). (no equation reference)
2. Compute d_1(u,k)+w(k,v) into the workspace via a data oracle (assumed). (eq_3)
3. Apply Grover/Durr-Hoyer minimum finding with O(sqrt(n)) iterations. (eq_4)
4. Repeat for all n^2 pairs to obtain the trivial total cost. (eq_1, eq_4)

## Assumptions

- No scope was given, so the trivial Grover baseline for one pair was chosen as the smallest useful construction.
- Quantum access to the weight matrix is assumed to be a standard query oracle.
- The abstract does not describe the improved algorithms.

## Missing information

- The actual nontrivial quantum algorithms for geometric weights, small integer weights, few weights per vertex, and earliest arrivals
- Their exact exponents
- The data model and oracle details
- Any circuit-level constructions
