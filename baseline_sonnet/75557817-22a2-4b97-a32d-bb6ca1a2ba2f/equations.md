# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Distinguish non-isomorphic cospectral regular graphs (G_4(n;n+2) vs G_5(n;n+2), and T_4, T_5) using a multiparticle (fermionic) continuous-time quantum walk, whose adjacency matrix restricted to the antisymmetric subspace differs between the graphs, and using entanglement entropy of coupled harmonic oscillators placed on the nodes.

Scope: Generic background construction: the two-fermion antisymmetric-subspace adjacency matrix for a graph A, plus the comparison criterion of spectra and the Gaussian-state entanglement entropy for a harmonic-oscillator network. Explicit G_4/G_5 adjacency matrices, T_4/T_5 constructions, and analytic entropy results are outside scope. No circuit instance is fixed.

## Symbols

- $A$: adjacency matrix of a graph on N vertices; domain: {0,1}^{N\times N}, symmetric
- $N$: number of vertices; domain: positive integer
- $A^{(2)}$: adjacency matrix restricted to the antisymmetric two-fermion subspace; domain: real symmetric, dimension N(N-1)/2
- $|i,j\rangle_-$: antisymmetrized basis state with i<j; domain: vectors in the antisymmetric subspace
- $K$: coupling (spring) matrix of the oscillator network; domain: real symmetric positive definite
- $S$: von Neumann entanglement entropy between a subset of oscillators and the rest; domain: nonnegative real
- $\nu_k$: symplectic eigenvalues of the reduced covariance matrix; domain: real, \ge 1/2 (with \hbar=1)

## eq_1: Antisymmetric basis state

$$
|i,j\rangle_-=\tfrac{1}{\sqrt2}\left(|i\rangle|j\rangle-|j\rangle|i\rangle\right),\ i<j
$$

Basis of the two-fermion subspace.

Provenance: `standard_background`. Standard fermionic antisymmetric basis; the abstract only mentions an antisymmetric fermionic basis.

Equation assumptions:

- Two walkers (particles)

## eq_2: Two-particle Hamiltonian

$$
A^{(2)}=\left(A\otimes I+I\otimes A\right)\big|_{\text{antisym}},\quad \langle k,l|A^{(2)}|i,j\rangle_-=A_{ki}\delta_{lj}+A_{lj}\delta_{ki}-A_{kj}\delta_{li}-A_{li}\delta_{kj}
$$

Non-interacting fermion walk generator restricted to the antisymmetric subspace.

Provenance: `standard_background`. Standard construction for non-interacting multiparticle walks; the paper's exact form is not given in the abstract.

Equation assumptions:

- Non-interacting particles
- Two particles

## eq_3: Distinguishing criterion

$$
A_{G_4}^{(2)}\neq A_{G_5}^{(2)}\ \text{(up to permutation), e.g. } \mathrm{spec}(A^{(2)}_{G_4})\neq \mathrm{spec}(A^{(2)}_{G_5})\ \text{although}\ \mathrm{spec}(A_{G_4})=\mathrm{spec}(A_{G_5})
$$

Cospectral graphs are distinguished if their antisymmetric-subspace matrices differ.

Provenance: `abstract_inferred`. The abstract says the rewritten matrices differ. A spectral comparison is my choice, and the spectrum of A^{(2)} is the pairwise sums of eigenvalues, so it is identical for cospectral graphs. Differences must therefore appear in the matrix structure rather than its spectrum, and the criterion is stated as a matrix difference, with the spectrum clause likely failing for non-interacting fermions.

Abstract evidence: we rewrite the adjacency matrices of graphs in the antisymmetric fermionic basis and show that they are different for these pairs of graphs

Equation assumptions:

- Non-interacting case: spectra of A^{(2)} coincide for cospectral graphs, so a distinction needs matrix-level or graph-structure-dependent invariants such as return probabilities from specific states

## eq_4: Oscillator network Hamiltonian

$$
H=\tfrac12\sum_i p_i^2+\tfrac12\sum_{i,j}x_iK_{ij}x_j,\quad K=\omega_0^2 I+ \kappa\,(D-A)\ \text{(assumed)}
$$

Identical harmonic oscillators on the nodes, coupled through the graph.

Provenance: `assumption`. The abstract says nodes are identical quantum harmonic oscillators; the coupling form is assumed.

Equation assumptions:

- Coupling via graph Laplacian D-A
- Ground state

## eq_5: Entanglement entropy of a Gaussian state

$$
S=\sum_k\left[(\nu_k+\tfrac12)\ln(\nu_k+\tfrac12)-(\nu_k-\tfrac12)\ln(\nu_k-\tfrac12)\right]
$$

Entropy of the reduced Gaussian state of a subset of oscillators.

Provenance: `standard_background`. Standard result for Gaussian states; the paper's analytic expressions are not available.

Equation assumptions:

- Gaussian (ground) state
- \hbar=1

## Registers

- walker_positions: unknown qubits; Two-fermion position space of dimension N(N-1)/2 in the antisymmetric subspace; no circuit encoding is given

## Classical postprocessing

Compare A^{(2)} matrices (or derived walk quantities) and the entropy values S between G_4 and G_5; different values indicate non-isomorphism.

## Algorithm steps

1. Build the adjacency matrices of the two cospectral graphs (explicit G_4, G_5 not available from the abstract). (no equation reference)
2. Form the antisymmetric two-particle basis and matrices A^{(2)}. (eq_1, eq_2)
3. Compare A^{(2)} for the two graphs. (eq_3)
4. For the entropy approach, place oscillators on the nodes, compute the ground-state covariance, reduce to a subset, and compute S for both graphs. (eq_4, eq_5)

## Assumptions

- Two non-interacting fermionic walkers
- Laplacian-type oscillator coupling
- Ground-state Gaussian entropy
- No specific n chosen

## Missing information

- Explicit adjacency structure of G_4(n;n+2), G_5(n;n+2), T_4, T_5
- Number of walkers used
- Which two parts of the network are used for entropy
- Oscillator coupling and state definition
- Analytic results
- Any circuit encoding or measurement
