# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on the simplex of M+1 complete graphs K_M (N=M(M+1) vertices), H=-gamma*A-sum_{w in marked}|w><w|, starting from |s>. Success probability depends on the marked-vertex configuration through the critical gamma*. Goal: a small simulable circuit that evolves for time t and reads the probability on the marked set, scanned over gamma.

Scope: Tiny instance M=2 (N=6, 3 qubits, 2 padding states) or M=3 (N=12, 4 qubits, 4 padding states) with two marked vertices in a chosen configuration (same clique vs different cliques; connector vs non-connector). Evolution is done by a Trotterized or exactly compiled exp(-iHt) from standard gates. Out of scope: the analytic perturbative gamma* expressions, the M+1 and 2(M+1) marked-vertex configurations, the asymptotic proofs, and the discrete-time comparison.

## Symbols

- $M$: clique size; also the number of cliques minus one; domain: integer >=2
- $N$: number of vertices, M(M+1); domain: integer
- $A$: adjacency matrix of the simplex of K_M; domain: N x N symmetric 0/1 matrix
- $\gamma$: jumping rate; domain: real >0
- $W$: set of marked vertices; domain: subset of {0..N-1}
- $|s\rangle$: uniform superposition over the N graph vertices; domain: unit vector
- $t$: evolution time; domain: real >=0
- $P(\gamma,t)$: success probability on the marked set; domain: [0,1]
- $E_{pad}$: penalty energy on padding basis states; domain: large positive real

## eq_1: Search Hamiltonian

$$
H=-\gamma A-\sum_{w\in W}|w\rangle\langle w|+E_{pad}\sum_{j\ge N}|j\rangle\langle j|
$$

CTQW search Hamiltonian on the padded 2^n-dimensional space. The padding term applies only when N is not a power of 2.

Provenance: `assumption`. The sketch fixes the form of H; the padding penalty is a proposed construction for the qubit encoding.

Equation assumptions:

- Adjacency matrix is used, not the Laplacian
- Oracle strength is 1

## eq_2: Graph adjacency

$$
A=\sum_{i}(J-I)_{\text{clique }i}+\sum_{i<j}\left(|c_{ij}\rangle\langle c_{ji}|+|c_{ji}\rangle\langle c_{ij}|\right)
$$

Each of the M+1 cliques is complete on M vertices. Each pair of cliques is joined by one edge between connector vertices c_{ij} in clique i and c_{ji} in clique j. This requires M=(M+1)-1 connectors per clique, so every vertex is a connector.

Provenance: `assumption`. The simplex of K_M is interpreted from the sketch. Each clique has M vertices and M other cliques, so the vertex-to-connector assignment is a bijection.

Equation assumptions:

- Vertex labeling: index = clique*M + local position, with the connector to clique j at a fixed local position

## eq_3: Evolution and success probability

$$
|\psi(t)\rangle=e^{-iHt}|s\rangle,\quad P(\gamma,t)=\sum_{w\in W}|\langle w|\psi(t)\rangle|^2
$$

State evolved from the uniform start and the probability read out on the marked set.

Provenance: `standard_background`. Standard CTQW search readout.

## eq_4: Critical rate and timing

$$
\gamma^*=\gamma^*(\text{config},M),\quad t^*\approx\frac{\pi}{2}\sqrt{N},\quad P(\gamma^*,t^*)\approx1
$$

Success at the avoided crossing; the gap is about 1/sqrt(N). The explicit gamma* per configuration is not reconstructed. Instead, find it numerically by scanning gamma.

Provenance: `abstract_inferred`. The abstract says the required rate depends on the configuration. The t scaling comes from the sketch and is standard for optimal CTQW search.

Abstract evidence: showing that the location of the marked vertices can dramatically influence the required jumping rate of the quantum walk, such that using the wrong configuration’s value can cause the search to fail

Equation assumptions:

- P~1 holds only asymptotically; small M may give lower peaks

## eq_5: Trotter step

$$
e^{-iHt}\approx\left(e^{i\gamma A\,t/r}\,e^{i D t/r}\right)^r,\quad D=\sum_{w\in W}|w\rangle\langle w|-E_{pad}\sum_{j\ge N}|j\rangle\langle j|
$$

First-order Trotterization with r steps. The diagonal factor is a phase on marked and padding basis states, implemented with multi-controlled phase gates. The A factor is exactly diagonalized or compiled from commuting groups of two-level rotations.

Provenance: `assumption`. Proposed circuit realization from the sketch.

Equation assumptions:

- r large enough for small error, or exact compilation by standard gates, not a dense unitary gate

## Registers

- v: ceil(log2 N) (3 for M=2, 4 for M=3) qubits; vertex index, little-endian integer encoding

## Initial state

H gates on all vertex qubits give the uniform state over 2^n basis states. This equals |s> only if N is a power of 2. Otherwise the padding states are suppressed by the penalty during evolution, but a clean start needs the amplitude on them removed, which is not exact. Alternative: use the padded uniform state and treat padding as a small leakage.

## Measurement

Measure all vertex qubits in the computational basis; the marked-set probability is the sum over marked indices.

## Classical postprocessing

For each configuration, compute max over t of P(gamma,t) against gamma. Locate gamma* as the argmax. Show that using another configuration's gamma* gives a low P.

## Algorithm steps

1. Choose M, the marked set W for one configuration, and a grid of gamma and t values. (eq_1, eq_2)
2. Build one circuit per (gamma,t): H on all qubits, then r Trotter steps of the A-term and the marked/padding phase term. (eq_5)
3. Measure all vertex qubits, with no ancilla. Index = sum of bit_i 2^i, with i the qiskit classical bit and the last character of the key being bit 0. (eq_3)
4. Compute P as the counts on the marked indices divided by the shots. Scan gamma and t, and compare the peak position across configurations. (eq_3, eq_4)

## Assumptions

- Smallest instance chosen by me: M=2 or 3, with two marked vertices
- Adjacency-matrix Hamiltonian with oracle strength 1
- No black-box queries: the oracle is explicit, so the query budget is unused
- Padding handled by a large penalty

## Missing information

- Explicit gamma* formulas for each configuration
- Exact definition of the connector structure in the paper, such as the Laplacian convention
- Exact reduced-matrix entries
- Results for M+1 and 2(M+1) marked vertices
