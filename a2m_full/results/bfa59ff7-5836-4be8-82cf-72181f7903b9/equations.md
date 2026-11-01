# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Trotterized time evolution of a second-quantized molecular Hamiltonian under Jordan-Wigner, with Hartree-Fock or fixed-particle-number state preparation, and classical estimation of Trotter error and step count restricted to the eta-electron subspace.

Scope: One tiny instance: H2 in a minimal basis (n=4 spin orbitals, eta=2), second-order Trotter, statevector simulation, no ancilla. Compare ground-state energy error of the Trotter unitary against r. Excluded: phase estimation/Hadamard test, the paper's actual error bounds, Z and filling-fraction scaling analysis, and larger molecules. Integrals h_pq and h_pqrs must be supplied externally.

## Symbols

- $n$: number of spin orbitals = qubits; domain: integer, 4 for the H2 instance
- $\eta$: number of electrons; domain: integer, 0<=eta<=n
- $h_{pq},h_{pqrs}$: one- and two-electron integrals; domain: real, precomputed
- $H_j$: Pauli-string terms of H after Jordan-Wigner, with coefficients absorbed; domain: Hermitian operators
- $t$: total evolution time; domain: positive real
- $r$: number of Trotter steps; domain: positive integer
- $U_r$: Trotterized evolution; domain: unitary on n qubits
- $\Pi_\eta$: projector onto the eta-electron subspace; domain: projector
- $\epsilon$: ground-state energy error; domain: nonnegative real

## eq_1: Second-quantized Hamiltonian

$$
H=\sum_{pq}h_{pq}a_p^\dagger a_q+\tfrac12\sum_{pqrs}h_{pqrs}a_p^\dagger a_q^\dagger a_r a_s=\sum_j H_j
$$

Electronic Hamiltonian, decomposed into Pauli strings via Jordan-Wigner.

Provenance: `standard_background`. Standard quantum chemistry form; the abstract only mentions quantum chemistry simulation.

Equation assumptions:

- Jordan-Wigner mapping
- integrals supplied externally

## eq_2: Second-order product formula

$$
U_r=\left(\prod_{j=1}^{L}e^{-iH_j t/2r}\prod_{j=L}^{1}e^{-iH_j t/2r}\right)^r
$$

Symmetric second-order Trotter-Suzuki evolution; each Pauli exponential is a CNOT ladder, RZ, and the reverse ladder.

Provenance: `assumption`. The abstract refers to Trotterization; the order is chosen per the sketch default.

Equation assumptions:

- second order is the default

## eq_3: Hartree-Fock state

$$
|\mathrm{HF}\rangle=\prod_{p\in\mathrm{occ}}X_p|0\rangle^{\otimes n}
$$

Slater determinant under Jordan-Wigner, with qubit p set to 1 if orbital p is occupied (qubit 0 is the least-significant bit).

Provenance: `standard_background`. Standard JW preparation; it stands in for the paper's improved state preparation, which is not specified.

Equation assumptions:

- occupied set known, e.g. orbitals 0 and 1 for H2

## eq_4: Effective Hamiltonian error in subspace

$$
\epsilon(r)=\left|\langle\psi_0|\tilde H_r|\psi_0\rangle-E_0\right|,\quad U_r=e^{-i\tilde H_r t},\ \epsilon\sim C\,(t/r)^2\ \text{for second order}
$$

Ground-state error from the Trotter unitary, where tilde H_r is the effective Hamiltonian, computed in the eta-electron subspace via Pi_eta. The scaling constant C is fitted numerically.

Provenance: `abstract_inferred`. The abstract discusses ground-state error from Trotterization; the (t/r)^2 form is standard background for second-order formulas, and C is not given.

Abstract evidence: numerical results for small systems fail to reveal any clear correlation between ground state error and number of spin orbitals

Equation assumptions:

- error measured in the fixed-particle subspace
- t/r small enough for the asymptotic regime

## eq_5: Step count from classical extrapolation

$$
r\ge t\sqrt{C/\epsilon_{\mathrm{target}}},\quad C\approx\epsilon(r_k)\,r_k^2/t^2
$$

Choose r from the error measured at several small step sizes, without extra quantum resources.

Provenance: `abstract_inferred`. This is one concrete reading of the classical estimation strategy; the paper's actual method is unknown.

Abstract evidence: to use classical processing to further reduce the required Trotter step size and to estimate the necessary number of steps, without requiring additional quantum resources

Equation assumptions:

- second-order scaling holds at the sampled r_k

## Registers

- q: n (4 for H2) qubits; JW spin-orbital qubits; qubit i is orbital i

## Initial state

HF determinant with X on the occupied qubits (eq_3).

## Measurement

Statevector simulation with no measurements: read the energy expectation or the overlap with the exact ground state.

## Classical postprocessing

Restrict to the eta-electron subspace, fit epsilon versus (t/r)^2, and choose r from eq_5.

## Algorithm steps

1. Load or compute the H2 integrals, build the JW Pauli terms, and verify with exact diagonalization in the eta=2 sector for E_0 and psi_0. (eq_1)
2. Prepare the HF state with X gates. (eq_3)
3. Build U_r with Pauli-exponential gadgets (or PauliEvolutionGate with SuzukiTrotter order 2) for several r. (eq_2)
4. Classically compute the effective-Hamiltonian ground-state error restricted to the eta-electron subspace for several r, fit C, and choose r. (eq_4, eq_5)

## Assumptions

- H2, minimal basis, n=4, eta=2, no ancilla
- second-order Trotter
- integrals precomputed externally
- Qiskit little-endian ordering

## Missing information

- the paper's actual error bounds and commutator expressions
- how Z and eta/n enter quantitatively
- the improved state preparation circuit details (Givens ladder angles)
- Hamiltonian term ordering used
- actual integral values
