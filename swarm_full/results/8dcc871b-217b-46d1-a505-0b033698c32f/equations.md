# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize continuous-time quantum walk search on graphs and test whether graph connectivity (vertex, edge, algebraic, normalized algebraic) predicts fast search. The abstract claims two counterexamples: a low-connectivity graph with fast search, and a high-connectivity graph with slow search, the latter using a novel two-stage walk in which the walking rate must be adjusted.

Scope: Abstract-level reconstruction of the search model only: Schrödinger evolution under a walk Hamiltonian with a marked-vertex oracle. The specific graphs, the two-stage algorithm details, and the runtimes are not given in the abstract and are not reconstructed.

## Symbols

- $N$: number of vertices (search space size); domain: positive integer
- $d$: lattice dimension; domain: positive integer
- $\gamma$: walking rate (hopping amplitude); domain: positive real
- $H$: search Hamiltonian; domain: Hermitian operator on N-dimensional space
- $L$: graph Laplacian; domain: N x N real symmetric matrix
- $w$: marked vertex; domain: vertex label in {1..N}

## eq_1: Schrödinger evolution

$$
|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle
$$

Continuous-time quantum walk evolution generating the search.

Provenance: `standard_background`. The abstract mentions evolution by Schrödinger's equation; this explicit form is standard background.

## eq_2: Search Hamiltonian

$$
H = -\gamma L - |w\rangle\langle w|
$$

Walk Hamiltonian with oracle term for marked vertex w; the standard form is assumed, not given in the abstract.

Provenance: `assumption`. Standard continuous-time quantum walk search form, assumed because the abstract gives no Hamiltonian.

Equation assumptions:

- The paper uses this standard form, possibly with variations.

## eq_3: Cubic lattice runtime claim

$$
T = O(\sqrt{N}) \text{ for } d\geq 5
$$

Fast search time on cubic lattices of dimension at least 5.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: searches on $d$-dimensional cubic lattices in $O(\sqrt{N})$ time when $d\geq 5$

## Registers

- vertex: N basis states (about log2 N qubits if encoded) qubits; Position register of the walker on graph vertices

## Initial state

Assumed uniform superposition over all vertices, |s> = N^{-1/2} sum_v |v>.

## Measurement

Assumed: measure the vertex register in the computational (vertex) basis at the end of evolution; success means obtaining the marked vertex w, with probability |<w|psi(T)>|^2. The abstract refers to high search probability but gives no explicit protocol.

## Classical postprocessing

Assumed: check whether the measured vertex is w via the oracle; if not, repeat the run (and for the two-stage walk, the gamma schedule) until success. Expected repetitions are about 1/p_success.

## Algorithm steps

1. Prepare the walker in the uniform superposition over vertices (assumed). (no equation reference)
2. Evolve under the search Hamiltonian H for time t, with gamma tuned near its critical value. (eq_1, eq_2)
3. For the two-stage counterexample, evolve in a first stage with one gamma, then adjust gamma and evolve in a second stage (details not given in the abstract). (eq_1, eq_2)
4. Target runtime of order sqrt(N) for fast-search cases such as cubic lattices with d>=5. (eq_3)

## Assumptions

- Standard continuous-time quantum walk search model assumed.
- Standard Hamiltonian H=-γL-|w><w| assumed.
- Uniform superposition initial state assumed.
- Vertex-basis measurement at the end of the evolution assumed.
- Repeat-until-success classical postprocessing assumed.

## Missing information

- Definitions of the two example graphs
- Details of the two-stage algorithm and the walking-rate schedule
- Runtimes for the counterexamples
- Stage durations and gamma values for the two-stage walk
- Actual measurement protocol and success probabilities in the paper
