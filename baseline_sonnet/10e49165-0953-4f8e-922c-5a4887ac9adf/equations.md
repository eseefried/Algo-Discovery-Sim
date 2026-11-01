# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Continuous-time quantum walk search on a graph of N vertices with a marked vertex, analyzed via degenerate perturbation theory on a small weighted graph with self-loops. The abstract gives only the method outline, not the specific graph family or the explicit effective Hamiltonian.

Scope: Background formulation of CTQW search with H = -gamma L - |w><w| (or adjacency form) and a generic degenerate perturbation theory effective Hamiltonian, illustrated on a tiny assumed instance (complete graph, N=4). The paper's specific diagrammatic rules, graph family, and the subspace of dimension growing with N remain outside the scope.

## Symbols

- $N$: number of vertices; domain: positive integer
- $G$: graph with adjacency matrix A; domain: undirected graph
- $\gamma$: hopping rate; domain: positive real
- $w$: marked vertex; domain: vertex index in {0,...,N-1}
- $H$: search Hamiltonian; domain: N x N Hermitian matrix
- $H_0$: unperturbed part with degenerate eigenspace; domain: Hermitian
- $V$: perturbation; domain: Hermitian
- $P$: projector onto degenerate eigenspace of H_0; domain: projector
- $H_{\mathrm{eff}}$: effective Hamiltonian in the degenerate subspace; domain: operator on range of P
- $T$: search time; domain: positive real

## eq_1: Search Hamiltonian

$$
H=-\gamma A-|w\rangle\langle w|
$$

Standard CTQW search Hamiltonian with oracle term on the marked vertex; the paper's exact form (e.g. Laplacian) is not stated in the abstract.

Provenance: `standard_background`. Common form of CTQW search; the abstract mentions only continuous-time search on a graph.

Equation assumptions:

- Adjacency-matrix form used rather than the Laplacian
- Single marked vertex

## eq_2: Evolution

$$
|\psi(t)\rangle=e^{-iHt}|s\rangle,\quad |s\rangle=\frac{1}{\sqrt N}\sum_{x}|x\rangle
$$

Evolution from the uniform superposition.

Provenance: `standard_background`. Usual initial state for spatial search by CTQW.

Equation assumptions:

- Uniform initial state

## eq_3: Splitting for perturbation theory

$$
H=H_0+V,\quad H_0P=E_0P
$$

Split of H into a part with a degenerate eigenspace and a perturbation.

Provenance: `standard_background`. The abstract says the method uses degenerate perturbation theory; the specific H_0, V are not given.

Equation assumptions:

- The choice of H_0 and V is graph-specific and not given

## eq_4: Effective Hamiltonian to second order

$$
H_{\mathrm{eff}}=E_0P+PVP+PVQ\,(E_0-H_0)^{-1}QVP,\quad Q=I-P
$$

Standard second-order degenerate perturbation theory effective Hamiltonian. The paper's weighted self-loop graph would encode the entries of this operator, but the mapping rules are not given.

Provenance: `standard_background`. Generic background for the named technique.

Equation assumptions:

- Second-order truncation
- Valid when ||V|| is small compared with the gap

## eq_5: Reduced weighted graph with self-loops

$$
(H_{\mathrm{eff}})_{ab}=\begin{cases}\text{self-loop weight}&a=b\\ \text{edge weight}&a\neq b\end{cases}
$$

Interpretation of H_eff as a small weighted graph with self-loops, with matrix entries as weights.

Provenance: `abstract_inferred`. The abstract links small weighted graphs with self-loops to degenerate perturbation theory; the entries are inferred, not given.

Abstract evidence: sketching small weighted graphs with self-loops and considering degenerate perturbation theory’s effects on them

Equation assumptions:

- Weights correspond to matrix entries of an effective Hamiltonian

## Registers

- vertex: ceil(log2 N) qubits (assumed N=4: 2 qubits) qubits; Basis state |x> labels the graph vertex; computational-basis integer encoding x -> |x>

## Initial state

Uniform superposition |s> over all vertices (assumed).

## Measurement

Computational-basis measurement of the vertex register; success probability |<w|psi(T)>|^2 (assumed).

## Algorithm steps

1. Choose a tiny instance (assumed complete graph K_4, w=0) and build H. (eq_1)
2. Prepare |s>. (eq_2)
3. Identify the degenerate subspace and perturbation, and compute H_eff to the chosen order, representing it as a weighted self-loop graph. (eq_3, eq_4, eq_5)
4. Evolve under H for time T and read out the vertex register. (eq_2)

## Assumptions

- Scope is the generic CTQW search framework with a tiny assumed instance, not the paper's graph family.
- Adjacency Hamiltonian with a single marked vertex.

## Missing information

- Specific graph family and the subspace whose dimension grows with N
- Exact Hamiltonian form and the value of gamma
- Diagrammatic rules mapping graphs to H_eff
- Perturbation order and the resulting search time scaling
- Success probability results
