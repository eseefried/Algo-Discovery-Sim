# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Use Lanczos-generated invariant (Krylov) subspaces to reduce continuous-time quantum walk dynamics on symmetric graphs, illustrated by spatial search on a small graph.

Scope: Background Lanczos/Krylov reduction of a CTQW Hamiltonian from an initial state, plus a tiny assumed instance: spatial search with H = -gamma*L - |w><w| on the complete graph K_N, reduced to a 2D subspace. Out of scope: broken-link complete graphs, complete bipartite/star graphs, transport efficiencies, and the XY spin network fidelity bound.

## Symbols

- $H$: Hamiltonian of the continuous-time quantum walk; domain: Hermitian operator on C^N
- $|\psi_0\rangle$: initial state; domain: unit vector in C^N
- $|k_j\rangle$: Lanczos basis vectors spanning the invariant subspace; domain: orthonormal vectors in C^N
- $\alpha_j,\beta_j$: Lanczos diagonal and off-diagonal coefficients; domain: real, beta_j>=0
- $\gamma$: hopping rate; domain: positive real
- $|w\rangle$: marked vertex; domain: computational basis state
- $N$: number of vertices; domain: integer >=2

## eq_1: Lanczos recursion

$$
\beta_{j+1}|k_{j+1}\rangle = (H-\alpha_j)|k_j\rangle - \beta_j|k_{j-1}\rangle,\quad \alpha_j=\langle k_j|H|k_j\rangle,\ |k_0\rangle=|\psi_0\rangle,\ \beta_0=0
$$

Generates an orthonormal basis of the Krylov space span{H^m psi_0}; terminates when beta=0, giving an invariant subspace.

Provenance: `standard_background`. The abstract names the Lanczos algorithm for computing invariant subspaces; this is the standard recursion, not paper-specific detail.

Equation assumptions:

- Exact arithmetic

## eq_2: Reduced dynamics

$$
|\psi(t)\rangle=e^{-iHt}|\psi_0\rangle=\sum_{j=0}^{d-1}c_j(t)|k_j\rangle,\quad c(t)=e^{-iTt}e_0
$$

Dynamics restricted to d-dimensional subspace with tridiagonal T (diagonal alpha_j, off-diagonal beta_j).

Provenance: `standard_background`. Follows from the invariance of the Krylov space under H.

Equation assumptions:

- d is the Krylov dimension

## eq_3: Assumed search Hamiltonian

$$
H=-\gamma L-|w\rangle\langle w|,\quad L=N|s\rangle\langle s|\text{-complement: }L=N I-J,\ |s\rangle=N^{-1/2}\sum_x|x\rangle
$$

Spatial search Hamiltonian on K_N, with L the graph Laplacian and J the all-ones matrix, so L=N(I-|s><s|).

Provenance: `assumption`. Chosen as smallest instance of spatial search; the abstract only says search is optimal on complete graphs with broken links, not this exact form.

Equation assumptions:

- Standard Childs-Goldstone form
- Full complete graph without broken links

## eq_4: Reduced 2D basis

$$
\mathrm{span}\{|w\rangle,|s\rangle\},\quad H|_{2D}=\begin{pmatrix}-1-\gamma N(1-1/N)&\gamma N/\sqrt{N}\\ \gamma\sqrt{N}&-\gamma N\end{pmatrix}\text{ in basis }\{|w\rangle,|w^\perp\rangle\}
$$

Starting from |s>, the Krylov space is spanned by |s> and |w>. Matrix is given in a non-orthonormal-to-Lanczos but schematic basis and must be recomputed with Lanczos.

Provenance: `assumption`. Illustrative only; explicit matrix entries should be recomputed by eq_1 for the instance.

Equation assumptions:

- Initial state |s>
- Entries not verified

## Registers

- vertex: ceil(log2 N) qubits qubits; Encodes vertex label in computational basis (assumed)

## Initial state

Uniform superposition |s> over all vertices (assumed).

## Measurement

Computational basis measurement of the vertex register to estimate probability of w (assumed).

## Algorithm steps

1. Choose a small N, marked vertex w, and gamma; build H. (eq_3)
2. Run Lanczos from |s> to get the invariant subspace and tridiagonal T. (eq_1)
3. Evolve in the reduced subspace and track the overlap with |w>. (eq_2, eq_4)

## Assumptions

- Scope chosen by the reconstructor: complete-graph search as the tiny instance
- Hamiltonian form and gamma are not given in the abstract

## Missing information

- Explicit Hamiltonians and parameters for broken-link graphs, bipartite and star graphs
- Transport efficiency definitions and trapping model
- XY spin network Hamiltonian and fidelity bound derivation
- Optimal gamma and timing results
