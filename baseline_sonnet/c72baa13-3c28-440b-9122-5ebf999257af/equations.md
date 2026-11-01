# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on a graph with N vertices, using Schrödinger evolution under a walk Hamiltonian with walking rate gamma plus an oracle term for a marked vertex; the abstract's specific graph examples and two-stage algorithm are not defined.

Scope: Background single-stage continuous-time quantum walk search (Childs-Goldstone style) on a tiny explicit instance, the complete graph K_4 with one marked vertex. Out of scope: the paper's low-connectivity fast-search graph, its high-connectivity slow-search graph, the two-stage algorithm, its gamma adjustment schedule, and connectivity measures.

## Symbols

- $N$: number of vertices; domain: positive integer, N=4 in the toy instance
- $G$: graph with adjacency matrix A; domain: simple undirected graph
- $\gamma$: walking rate; domain: real, nonnegative
- $w$: marked vertex; domain: vertex label in {0,...,N-1}
- $H$: search Hamiltonian; domain: Hermitian N x N matrix
- $|s\rangle$: uniform superposition over vertices; domain: unit vector in C^N
- $T$: evolution time; domain: real, nonnegative

## eq_1: Schrödinger evolution

$$
i\frac{d}{dt}|\psi(t)\rangle = H|\psi(t)\rangle,\quad |\psi(T)\rangle=e^{-iHT}|\psi(0)\rangle
$$

Quantum particle evolves under Schrödinger's equation.

Provenance: `abstract_inferred`. The abstract names Schrödinger evolution for the walk; the explicit form is standard.

Abstract evidence: A randomly walking quantum particle evolving by Schrödinger’s equation

Equation assumptions:

- hbar=1
- time-independent H in a single stage

## eq_2: Search Hamiltonian

$$
H=-\gamma L-|w\rangle\langle w|,\quad L=D-A
$$

Walk term from the graph Laplacian plus an oracle term marking w.

Provenance: `standard_background`. Standard continuous-time quantum search form; the paper's exact Hamiltonian and any two-stage variant are not given.

Equation assumptions:

- Laplacian-based walk; adjacency-based variants differ for irregular graphs

## eq_3: Initial state

$$
|\psi(0)\rangle=|s\rangle=\frac{1}{\sqrt N}\sum_{v=0}^{N-1}|v\rangle
$$

Uniform superposition start.

Provenance: `standard_background`. Usual starting state for spatial search.

## eq_4: Success probability

$$
p(T)=|\langle w|e^{-iHT}|s\rangle|^2
$$

Probability of measuring the marked vertex.

Provenance: `standard_background`. Born rule applied to the vertex basis.

## eq_5: Fast-search scaling claim

$$
T=O(\sqrt N)\ \text{for}\ d\ge5\ \text{cubic lattices}
$$

Runtime scaling stated for d-dimensional cubic lattices.

Provenance: `abstract_explicit`. Directly stated asymptotic claim; not used to build the toy circuit.

Abstract evidence: searches on $d$-dimensional cubic lattices in $O(\sqrt{N})$ time when $d\geq 5$

## Registers

- vertex: ceil(log2 N) qubits (2 for K_4) qubits; Vertex basis |v>, with v encoded as a binary integer, most significant bit first

## Initial state

Uniform superposition |s> over all N vertex states on the vertex register.

## Measurement

Computational-basis measurement of the vertex register; success means obtaining w.

## Classical postprocessing

Check whether the outcome equals w; repeat if it does not.

## Algorithm steps

1. Prepare |s> on the vertex register. (eq_3)
2. Evolve under H for time T, with gamma tuned for the instance; the paper's two-stage algorithm would change gamma between stages, but that schedule is unspecified. (eq_1, eq_2)
3. Measure the vertex register in the computational basis and compare the success probability to the target. (eq_4)

## Assumptions

- Chose the smallest instance, K_4 with marked vertex w=0, as a toy example.
- Single-stage Laplacian-based Hamiltonian used as a generic baseline, not the paper's method.
- Optimal gamma and T are not specified; gamma=1/N is a known choice for the complete graph but is not from the abstract.

## Missing information

- Definitions of the two example graphs
- The two-stage algorithm's stages, Hamiltonians, and gamma adjustment rule
- Runtime and success probability results for the two examples
- Precise definitions of the connectivity measures
- Whether the walk uses the adjacency matrix or the Laplacian
