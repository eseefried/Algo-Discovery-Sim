# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Distinguish a pair of cospectral non-isomorphic graphs G and G' (e.g. G4(n;n+2), G5(n;n+2)) using a continuous-time quantum walk of two noninteracting fermions, whose Hamiltonian is the adjacency matrix acting on the antisymmetric two-particle subspace. Distinguishing is by a difference in output distributions or return amplitudes at a chosen time t.

Scope: One tiny explicit instance: N<=8 vertices (3 qubits per position register, 6 qubits plus 1 optional Hadamard-test ancilla). The two adjacency matrices are given explicitly and are not hidden in a black box. Covers building H2 on the antisymmetric subspace, a fixed antisymmetric initial state, evolution by exp(-i H2 t), and readout by position-basis distribution or return amplitude, compared by total variation distance. Outside scope: the entanglement-entropy calculation for harmonic-oscillator networks, the analytic derivations for general n, the T4/T5 graph construction, and any specific edge lists of G4/G5, which the abstract does not give.

## Symbols

- $N$: number of graph vertices; domain: positive integer, N<=8 in scope
- $A, A'$: adjacency matrices of G and G'; domain: symmetric 0/1 N x N matrices
- $H_2$: two-particle Hamiltonian A⊗I+I⊗A; domain: N^2 x N^2 Hermitian matrix
- $|ij\rangle_-$: normalized antisymmetric basis state (|ij>-|ji>)/sqrt2, i<j; domain: vectors in C^{N^2}, dimension N(N-1)/2 subspace
- $t$: evolution time; domain: real, t>0
- $P_G(ij,t)$: probability of measuring |ij> in the position registers; domain: [0,1]
- $d_{TV}$: total variation distance between output distributions; domain: [0,1]

## eq_1: Antisymmetric matrix elements

$$
\langle kl|_- H_2 |ij\rangle_- = A_{ik}\delta_{jl}+A_{jl}\delta_{ik}-A_{il}\delta_{jk}-A_{jk}\delta_{il}
$$

Matrix elements of H2 in the antisymmetric fermionic basis, for i<j and k<l.

Provenance: `abstract_inferred`. The abstract says the adjacency matrices are rewritten in the antisymmetric fermionic basis. The explicit formula is standard noninteracting two-fermion algebra, not quoted from the paper.

Abstract evidence: we rewrite the adjacency matrices of graphs in the antisymmetric fermionic basis

Equation assumptions:

- Noninteracting fermions
- Index ordering i<j and k<l

## eq_2: Two-particle Hamiltonian

$$
H_2 = A\otimes I + I\otimes A
$$

Sum of single-particle terms. It commutes with SWAP, so it preserves the antisymmetric subspace.

Provenance: `standard_background`. Standard construction for noninteracting multiparticle walks.

Equation assumptions:

- Noninteracting fermions

## eq_3: Evolution and readout probability

$$
|\psi(t)\rangle=e^{-iH_2 t}|\psi_0\rangle,\quad P_G(kl,t)=|\langle kl|\psi(t)\rangle|^2,\quad |\psi_0\rangle=\tfrac{1}{\sqrt2}(|ij\rangle-|ji\rangle)
$$

Walk from a fixed antisymmetric initial state. Probabilities are read in the position basis.

Provenance: `assumption`. Proposed concrete instance. The abstract does not specify the initial state or the observable.

Equation assumptions:

- The same (i,j) is used for G and G'
- Time t is chosen so that the distributions differ

## eq_4: Distinguishing criterion

$$
d_{TV}=\tfrac12\sum_{kl}|P_G(kl,t)-P_{G'}(kl,t)|>0
$$

Non-isomorphism is certified if the distributions differ at some t. Equal distributions certify nothing.

Provenance: `assumption`. The abstract says the walk distinguishes the pairs, but the statistic is chosen here.

Equation assumptions:

- Exact statevector simulation, with no sampling noise

## eq_5: Moment criterion

$$
\mathrm{tr}(H_2^k|_-)=\tfrac12\left[\mathrm{tr}(A^k\otimes I+I\otimes A)^k\right]-\ldots\ne \mathrm{tr}(H_2'^k|_-)
$$

The antisymmetric-sector spectra differ for some k even though the single-particle spectra coincide. The exact formula is omitted. Only the inequality is the claim.

Provenance: `abstract_inferred`. The abstract claims the antisymmetric representations differ, so the spectra or traces differ for some k. This is an inference.

Abstract evidence: show that they are different for these pairs of graphs

Equation assumptions:

- The explicit trace formula is not claimed

## Registers

- r1: 3 qubits; position of particle 1, little-endian binary vertex index
- r2: 3 qubits; position of particle 2, little-endian binary vertex index
- anc: 1 qubits; optional Hadamard-test ancilla, used only for the return-amplitude variant

## Initial state

Directly prepare the antisymmetric state (|i>|j>-|j>|i>)/sqrt2 with standard gates: for example, X gates to set |i>|j>, then H on a control and CNOT-based exchange, or a controlled-SWAP construction. Avoid initialize. The abstract does not specify the state.

## Measurement

Computational-basis measurement of both position registers (6 bits). Remember Qiskit's little-endian counts keys. Alternatively read the statevector directly for exact probabilities.

## Classical postprocessing

Compute d_TV between the G and G' distributions at each t. Declare non-isomorphic if d_TV exceeds a tolerance. Optionally compare tr(H2^k) restricted to the antisymmetric subspace classically.

## Algorithm steps

1. Fix the explicit adjacency matrices A and A' for a tiny cospectral non-isomorphic pair with N<=8. Embed them into 2^3-dimensional registers, padding unused vertices with zero rows and columns. (eq_2)
2. Prepare the fixed antisymmetric initial state on r1 and r2, identically for both graphs. (eq_3)
3. Apply exp(-i H2 t), as exp(-iAt) on r1 and exp(-iAt) on r2 since the two terms commute. Implement with a Pauli decomposition of A and Trotterization using PauliEvolutionGate or standard gates. The evolution preserves the antisymmetric subspace. (eq_1, eq_2, eq_3)
4. Measure r1 and r2 in the computational basis for a few chosen t. Compute the distributions for G and G' and their total variation distance. (eq_3, eq_4)

## Assumptions

- Small N so qubits fit under the cap
- Adjacency matrices supplied explicitly
- Evolution by Trotterization or Pauli decomposition
- Fixed antisymmetric initial state, the same for both graphs
- Noninteracting fermions
- Distinguishing is by a difference in distributions at a chosen t
- Exact edge lists of G4 and G5 are not given in the abstract and must be supplied by the task or by the next researcher

## Missing information

- Explicit edge lists of G4(n;n+2) and G5(n;n+2) and of T4/T5
- The paper's initial state and observable
- The paper's time values
- Details of the harmonic-oscillator entanglement entropy calculation, which is excluded from the circuit
