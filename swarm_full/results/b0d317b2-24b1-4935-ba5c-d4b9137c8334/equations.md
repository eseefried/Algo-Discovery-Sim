# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on the simplex of K_M complete graphs, where the location of marked vertices changes the search problem; analyze configurations of two, M+1 and 2(M+1) marked vertices and how the optimal jumping rate depends on the configuration.

Scope: Assumed standard CTQW search setup and the qualitative dependence of the critical jumping rate on the marked-vertex configuration; the explicit analytic results are not in the abstract and are not reconstructed.

## Symbols

- $\gamma$: jumping rate of the continuous-time quantum walk; domain: positive real
- $M$: number of complete graphs K_M in the simplex (and size of each); domain: integer >= 2
- $H$: search Hamiltonian; domain: Hermitian operator
- $A$: adjacency matrix of the graph; domain: real symmetric matrix
- $w$: marked vertex; domain: vertex of the graph
- $\mathcal{M}$: set of marked vertices; domain: subset of vertices

## eq_1: Search Hamiltonian

$$
H=-\gamma A-\sum_{w\in\mathcal{M}}|w\rangle\langle w|
$$

Standard CTQW search Hamiltonian with oracle term over marked vertices. Its form is an assumption since the abstract does not state it.

Provenance: `standard_background`. Common convention for CTQW spatial search; not given in the abstract.

Equation assumptions:

- Oracle strength normalized to 1
- Sign convention assumed

## eq_2: Evolution

$$
|\psi(t)\rangle=e^{-iHt}|s\rangle
$$

Evolution from the uniform superposition initial state under H.

Provenance: `standard_background`. Standard CTQW search procedure.

Equation assumptions:

- Initial state is the uniform superposition |s>

## Registers

- vertex: N = number of vertices of the simplex of K_M (explicit count not given in abstract) qubits; Position register; computational basis states label graph vertices, evolved under H

## Initial state

Uniform superposition |s> = N^{-1/2} sum_v |v> over all vertices.

## Measurement

Measure the vertex register in the computational basis after evolution time t; success means obtaining a marked vertex (assumed).

## Classical postprocessing

Check whether the outcome is in the marked set; repeat if not. Using a gamma from the wrong configuration may make the search fail.

## Algorithm steps

1. Prepare the uniform superposition |s> over all vertices. (no equation reference)
2. Choose gamma (critical value depends on the marked-vertex configuration) and evolve under H for a time t. (eq_1, eq_2)

## Assumptions

- Standard CTQW search Hamiltonian form and oracle strength 1 assumed; not stated in the abstract.
- Uniform initial state assumed.
- Vertex register of dimension N is an assumed encoding.
- Computational-basis vertex measurement assumed.

## Missing information

- Explicit critical gamma values for each marked configuration
- Graph structure details (adjacency of the simplex of K_M)
- Vertex count N and runtime/success probability results
- Exact marked-vertex configurations beyond their counts
