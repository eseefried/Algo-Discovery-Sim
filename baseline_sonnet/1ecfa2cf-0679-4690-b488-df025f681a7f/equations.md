# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Compare quantum search by discrete-time and continuous-time quantum walks on a graph with marked vertices, where oracle query cost is counted separately from walk-step cost; the abstract claims that allowing multiple walk steps per query gives a discrete-time walk that matches the continuous-time runtime, a cubic speedup over the classical random walk.

Scope: Only generic background definitions are provided: a tiny 4-vertex complete-graph search instance with standard continuous-time search Hamiltonian H=-gamma L-|w><w| and a discrete-time walk step W with oracle O, plus the abstract's speedup-exponent relations stated symbolically. The paper's specific graphs, walk-step counts, runtime formulas, and proofs are outside scope and not reconstructed.

## Symbols

- $T_{cl}$: classical random walk hitting/search time; domain: positive real
- $T_q$: quantum walk query time (counting only oracle queries/time); domain: positive real
- $|w\rangle$: marked vertex state; domain: computational basis state of C^N
- $N$: number of vertices; domain: positive integer (N=4 in the toy instance)
- $\gamma$: walk hopping rate; domain: positive real
- $L$: graph Laplacian (or adjacency-based walk generator); domain: N x N real symmetric matrix
- $W$: discrete-time walk step unitary; domain: unitary on C^N (or an extended space)
- $O$: oracle reflection I-2|w><w|; domain: unitary on C^N
- $m$: number of walk steps per oracle query; domain: positive integer

## eq_1: Continuous-time search Hamiltonian

$$
H=-\gamma L-|w\rangle\langle w|,\quad |\psi(t)\rangle=e^{-iHt}|\psi(0)\rangle
$$

Standard continuous-time quantum walk search dynamics where the oracle term is applied continuously and only the evolution time counts as query cost.

Provenance: `standard_background`. Standard Childs-Goldstone style formulation; the abstract names continuous-time walks but gives no Hamiltonian.

Equation assumptions:

- Oracle is the projector onto the marked vertex
- Specific graph and gamma are not given in the abstract

## eq_2: Discrete-time walk with m steps per query

$$
U=\left(W^{m}O\right)^{k}
$$

Discrete-time search where m walk steps are interleaved between oracle calls; k queries are counted while the m walk steps per query are not charged.

Provenance: `abstract_inferred`. The abstract describes multiple walk steps per oracle query; the product form is a natural formalization but the actual schedule is not given.

Abstract evidence: we allow the discrete-time quantum walk to also take multiple walk steps per oracle query while only counting queries

Equation assumptions:

- O and W are fixed unitaries
- m may depend on the graph

## eq_3: Oracle reflection

$$
O=I-2|w\rangle\langle w|
$$

Phase oracle marking the vertex w.

Provenance: `standard_background`. Common discrete-time search oracle form; not stated in the abstract.

Equation assumptions:

- Single marked vertex

## eq_4: Quadratic speedup relation for each model with its classical walk

$$
T_q=\Theta\left(\sqrt{T_{cl}}\right)
$$

Both the discrete-time (one step per query) and continuous-time walks achieve a quadratic speedup over the corresponding classical random walk.

Provenance: `abstract_inferred`. Quadratic speedup is interpreted as square-root scaling; the abstract states no formula, and the continuous-time and discrete-time classical baselines may differ.

Abstract evidence: both achieve quadratic speedups over their corresponding classical random walks

Equation assumptions:

- Speedup interpreted asymptotically in the sense of Theta or O
- T_{cl} denotes the respective classical random walk time

## eq_5: Cubic speedup relation for multi-step discrete walk

$$
T_q=\Theta\left(T_{cl}^{1/3}\right)
$$

Cubic speedup of the discrete-time walk with multiple steps per query, counting only queries, over its classical random walk.

Provenance: `abstract_inferred`. Cubic speedup interpreted as cube-root scaling in query count; exact definition and the relation to the continuous-time runtime are not given.

Abstract evidence: such that it is a cubic speedup over its corresponding classical random walk

Equation assumptions:

- Only queries counted, not walk steps
- Cube-root scaling interpretation

## Registers

- vertex: ceil(log2 N) qubits (2 qubits for N=4) qubits; position register encoding vertex index in computational basis; basis state |v> for v in {0,...,N-1}

## Initial state

Uniform superposition |s> = N^{-1/2} sum_v |v> over vertices (assumed; for discrete walks on edges a coin register may be needed).

## Measurement

Measure the vertex register in the computational basis and check whether the outcome is the marked vertex w.

## Classical postprocessing

Verify the measured vertex with one oracle call; repeat on failure.

## Algorithm steps

1. Prepare the initial state |s> on the vertex register. (no equation reference)
2. Continuous-time variant: evolve under H for time t of order the search time and count only t as cost. (eq_1)
3. Discrete-time variant: repeat k times the sequence of one oracle call followed by m walk steps. (eq_2, eq_3)
4. Compare the resulting query scalings to the classical random walk time as stated in the abstract. (eq_4, eq_5)

## Assumptions

- No scope was provided; the smallest useful construction chosen is a generic search-by-walk template on a tiny N=4 instance.
- Equations eq_1 and eq_3 are textbook background and not claimed to be the paper's constructions.
- Speedup exponents are interpreted asymptotically from the abstract's wording.

## Missing information

- Graph families and structure for which the speedups hold
- Precise walk operator W (coin or Szegedy-type) and the value of m
- Explicit runtime expressions and classical hitting times
- Proofs, parameter schedules, and success probabilities
- Definition of how continuous-time cost counts multiple effective walk steps per query
