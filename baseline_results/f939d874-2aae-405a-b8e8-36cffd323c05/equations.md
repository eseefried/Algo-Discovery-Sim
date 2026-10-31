# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Spatial search by continuous-time quantum walk (CTQW) on the simplex of K_M complete graphs with multiple marked vertices, where the required jumping rate gamma depends on the configuration (locations) of the marked vertices, so that using the critical gamma of the wrong configuration causes the search to fail.

Scope: One smallest useful construction: CTQW search Hamiltonian H = -gamma A - sum_w |w><w| on the simplex of K_M complete graphs for a tiny explicit instance M = 3 (4 copies of K_3, N = 12 vertices, 4-qubit vertex register) with two marked vertices; two marked-vertex configurations are specified (same clique vs. different, non-adjacent cliques) so that configuration dependence of the optimal gamma can be probed numerically by scanning gamma and the evolution time. Outside scope: the paper's analytic derivation of the critical jumping rates and runtimes for all two-vertex configurations, the two configurations of M+1 and of 2(M+1) marked vertices, the general-M asymptotics, and the comparison with discrete-time quantum walks.

## Symbols

- $M$: Size of each complete graph K_M; the simplex contains M+1 copies; domain: integer, M >= 2 (instance: M = 3)
- $N$: Total number of vertices, N = M(M+1); domain: positive integer (instance: N = 12)
- $(i,j)$: Vertex label: vertex in clique i whose single external edge goes to clique j; domain: i, j in {0,...,M}, j != i
- $A$: Adjacency matrix of the simplex of K_M complete graphs (M-regular); domain: N x N symmetric 0/1 matrix
- $\gamma$: Jumping rate of the continuous-time quantum walk; domain: real, gamma > 0
- $W$: Set of marked vertices; domain: subset of V with |W| = 2 in scoped instance
- $H$: Search Hamiltonian; domain: N x N Hermitian matrix
- $|s\rangle$: Uniform superposition over all vertices (initial state); domain: unit vector in C^N
- $t$: Evolution time; domain: real, t >= 0
- $p_W(t)$: Success probability of measuring a marked vertex at time t; domain: [0,1]
- $\gamma_c(W)$: Configuration-dependent critical (optimal) jumping rate; domain: real, > 0; value not given in abstract

## eq_1: Simplex of K_M complete graphs (vertex and edge set)

$$
V=\{(i,j): i,j\in\{0,\dots,M\},\ j\neq i\},\quad |V|=N=M(M+1),\qquad (i,j)\sim(i,j')\ \text{for } j\neq j',\qquad (i,j)\sim(j,i)
$$

M+1 cliques K_M; vertex (i,j) lies in clique i and its unique inter-clique edge connects it to vertex (j,i) of clique j, so the cliques are joined in the pattern of a complete graph K_{M+1} (a simplex). Every vertex has degree M (M-1 intra-clique edges plus 1 external edge).

Provenance: `assumption`. The abstract names the graph but does not define it; this explicit labeling is the natural construction consistent with the name 'simplex of K_M complete graphs' and with the usual usage in the CTQW search literature. The exact definition in the paper is not verified here.

Equation assumptions:

- Each pair of cliques is joined by exactly one edge and each vertex has exactly one external edge

## eq_2: CTQW search Hamiltonian

$$
H=-\gamma A-\sum_{w\in W}|w\rangle\langle w|
$$

Standard continuous-time quantum walk search Hamiltonian with jumping rate gamma and a marking oracle term for each marked vertex. On a regular graph the Laplacian form -gamma L differs only by a multiple of the identity (global phase).

Provenance: `standard_background`. Standard Childs-Goldstone form of CTQW spatial search; the abstract refers to 'continuous-time quantum walk', 'jumping rate', and 'marked vertices' but does not write the Hamiltonian.

Equation assumptions:

- Paper uses the adjacency (or equivalently, for a regular graph, Laplacian) form with unit-strength oracle

## eq_3: Initial state

$$
|s\rangle=\frac{1}{\sqrt{N}}\sum_{v\in V}|v\rangle
$$

Uniform superposition over all N vertices, the standard CTQW search starting state.

Provenance: `standard_background`. Standard starting state for spatial search by quantum walk.

## eq_4: Time evolution and success probability

$$
|\psi(t)\rangle=e^{-iHt}|s\rangle,\qquad p_W(t)=\sum_{w\in W}|\langle w|\psi(t)\rangle|^{2}
$$

Exact Schrodinger evolution under H followed by the probability of a computational-basis measurement returning any marked vertex.

Provenance: `standard_background`. Definition of CTQW search success probability.

## eq_5: Configuration-dependent critical jumping rate

$$
\gamma_c = \gamma_c(W),\qquad \max_t p_W(t)\big|_{\gamma=\gamma_c(W')}\ll \max_t p_W(t)\big|_{\gamma=\gamma_c(W)}\ \text{for suitable } W'\neq W
$$

The jumping rate at which the search succeeds depends on the location (configuration) of the marked vertices, not only on their number; using the critical gamma of another configuration W' can make the search fail. The explicit values of gamma_c(W) are a paper result not available from the abstract.

Provenance: `abstract_inferred`. Inferred directly from the abstract's claim; the inequality is qualitative and the actual analytic gamma_c values are missing.

Abstract evidence: the location of the marked vertices can dramatically influence the required jumping rate of the quantum walk, such that using the wrong configuration’s value can cause the search to fail

Equation assumptions:

- 'Fail' interpreted as the maximal success probability over time not approaching a constant/1

## eq_6: Scoped marked-vertex configurations (M = 3 instance)

$$
W_{\rm same}=\{(0,1),(0,2)\},\qquad W_{\rm diff}=\{(0,1),(2,3)\}
$$

Two of the two-marked-vertex configurations on the N = 12 instance: both marked vertices in the same clique (clique 0), and marked vertices in different cliques that are not joined by an edge. A third configuration, marked vertices joined by the external edge, e.g. {(0,1),(1,0)}, is also possible but not treated here.

Provenance: `assumption`. The abstract says all two-vertex configurations are solved; these are the concrete representatives chosen for a tiny instance.

Equation assumptions:

- M = 3 instance
- Configuration classes for two marked vertices are determined by whether the marked vertices share a clique and whether they are adjacent

## Registers

- vertex: ceil(log2 N) = 4 qubits for N = 12 qubits; Encodes the walker position; vertex (i,j) is mapped to an integer index v in {0,...,N-1} by lexicographic enumeration of the pairs (i,j) with j != i, stored in binary (qubit 0 = least significant bit). Basis states |12>..|15> are unused and receive zero amplitude; H is padded with zeros on them.

## Initial state

|s> = (1/sqrt(12)) sum_{v=0}^{11} |v> on the 4-qubit vertex register (not a plain Hadamard product state because N = 12 is not a power of 2; requires an amplitude-encoding preparation).

## Measurement

Computational-basis measurement of the 4-qubit vertex register; outcome index v is decoded to (i,j) and compared with the marked set W. Success probability p_W(t) is estimated from repeated shots.

## Classical postprocessing

For each configuration W, scan gamma and t, estimate p_W(t), and identify gamma_c(W) and the time of peak success probability; then evaluate configuration W under gamma_c(W') of the other configuration to check whether the success probability collapses, as claimed in the abstract. Note that the paper's analytic gamma_c values are not reproduced here and must be obtained numerically or from the full paper.

## Algorithm steps

1. Build the 12 x 12 adjacency matrix A of the simplex of K_3 complete graphs from the vertex/edge definition and embed it in the 16-dimensional 4-qubit space. (eq_1)
2. Choose a marked configuration W (W_same or W_diff) and a jumping rate gamma; form H = -gamma A - sum_{w in W} |w><w|. (eq_2, eq_6)
3. Prepare the uniform superposition |s> over the 12 vertex basis states. (eq_3)
4. Apply the unitary e^{-iHt} (exact matrix exponential or a Trotter/Hamiltonian-simulation approximation) for a chosen time t. (eq_4)
5. Measure the vertex register and record whether the outcome index lies in W; repeat over a grid of gamma and t to locate the configuration-dependent peak and test the search with the other configuration's gamma. (eq_4, eq_5)

## Assumptions

- Graph definition (eq_1) is the standard simplex-of-complete-graphs construction; not verified against the paper
- Adjacency-matrix form of the search Hamiltonian with unit oracle strength (equivalent to Laplacian form up to global phase on this regular graph)
- Tiny instance M = 3 (N = 12) chosen by the reconstruction agent since no experiment_scope was supplied
- Only two of the two-marked-vertex configurations are instantiated; M+1 and 2(M+1) marked-vertex configurations are out of scope
- Nothing in this specification has been simulated or verified

## Missing information

- The paper's analytic critical jumping rates gamma_c for each two-vertex configuration and for the M+1 and 2(M+1) configurations
- The precise definition of the two M+1 and two 2(M+1) marked-vertex configurations
- Runtime scaling and asymptotic success probabilities derived in the paper
- Whether the paper uses the adjacency or Laplacian Hamiltonian and any normalization of gamma
- Details of the discrete-time quantum walk comparison
