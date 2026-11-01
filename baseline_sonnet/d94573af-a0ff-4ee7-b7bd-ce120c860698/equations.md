# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Compute the ground-state energy of minimal-basis HeH+ as a function of bond length (dissociation curve) on a two-qubit solid-state NV-center register, via phase estimation-type energy extraction. The abstract gives no circuit details.

Scope: One smallest construction: a generic 2-qubit qubit-encoded Hamiltonian for minimal-basis HeH+ at a single bond length, with an iterative phase-estimation-style energy readout. The specific Hamiltonian coefficients, NV control sequences, the paper's actual algorithm, and the 1e-14 Hartree uncertainty analysis are outside scope.

## Symbols

- $R$: He-H internuclear distance; domain: positive real
- $H(R)$: qubit Hamiltonian of HeH+ in minimal basis at bond length R; domain: Hermitian operator on 2 qubits
- $g_i(R)$: real Pauli coefficients (not given in abstract); domain: real
- $P_i$: Pauli strings on 2 qubits; domain: {I,X,Y,Z}^{\otimes 2}
- $E_0(R)$: ground-state energy in Hartree; domain: real
- $\tau$: evolution time in phase estimation; domain: positive real
- $\phi$: estimated phase; domain: [0,1)
- $\epsilon$: energy uncertainty; domain: nonnegative real, in Hartree

## eq_1: Qubit Hamiltonian

$$
H(R)=\sum_i g_i(R)\,P_i
$$

Pauli decomposition of the molecular Hamiltonian after fermion-to-qubit mapping and reduction to 2 qubits.

Provenance: `assumption`. Abstract only says minimal basis HeH+; a 2-qubit Pauli form is a proposed standard construction and the register size is assumed.

Equation assumptions:

- 2-qubit reduced Hamiltonian
- coefficients g_i(R) from a classical electronic-structure calculation, not given

## eq_2: Ground-state energy

$$
E_0(R)=\min_{|\psi\rangle}\langle\psi|H(R)|\psi\rangle
$$

Target quantity at each R; the dissociation curve is E_0(R) over a grid of R (plus nuclear repulsion if not included in H).

Provenance: `abstract_inferred`. A dissociation curve is the ground-state energy versus bond length; the variational form is the standard definition.

Abstract evidence: we compute the bond dissociation curve of the minimal basis helium hydride cation, HeH+

Equation assumptions:

- nuclear repulsion energy included in H or added classically

## eq_3: Time evolution

$$
U(\tau)=e^{-iH(R)\tau}
$$

Unitary whose eigenphase encodes the energy.

Provenance: `standard_background`. Standard phase-estimation setup; the abstract does not state that this method was used.

Equation assumptions:

- Trotterization or exact compilation to NV gates not specified

## eq_4: Phase-energy relation

$$
U(\tau)|\psi_0\rangle=e^{-iE_0\tau}|\psi_0\rangle,\quad E_0=-2\pi\phi/\tau \pmod{2\pi/\tau}
$$

Energy read from the eigenphase, defined modulo 2π/τ, so τ must be chosen to avoid aliasing.

Provenance: `standard_background`. Standard phase estimation relation; the sign convention and the 2π factor depend on the definition of φ.

Equation assumptions:

- |ψ0> is an eigenstate (ground state) or has large overlap with it

## eq_5: Uncertainty statement

$$
\epsilon\sim10^{-14}\ \text{Hartree}
$$

Reported energy uncertainty within the model basis, far below chemical precision of about 1.6e-3 Hartree.

Provenance: `abstract_explicit`. Stated in the abstract; its derivation is not given.

Abstract evidence: we report an energy uncertainty (given our model basis) of the order of $10^{-14}$ Hartree

## Registers

- system: 2 (assumed) qubits; encodes the HeH+ minimal-basis electronic state
- ancilla: 1 (assumed) qubits; phase-estimation readout qubit; in an NV system this could be an electron or nuclear spin, but this is not stated

## Initial state

Assumed: Hartree-Fock-like reference product state on the system register, ancilla in |+>.

## Measurement

Assumed: ancilla measured in the X/Y basis to estimate the phase.

## Classical postprocessing

Convert the phase to energy, resolve aliasing, and assemble E_0(R) over R.

## Algorithm steps

1. Classically compute g_i(R) for the chosen R and build the 2-qubit Hamiltonian. (eq_1)
2. Prepare the reference state on the system register and the ancilla in superposition. (no equation reference)
3. Apply controlled-U(τ) for chosen τ values. (eq_3)
4. Measure the ancilla and estimate the phase. (eq_4)
5. Convert the phase to the energy and repeat over a grid of R to obtain the curve. (eq_2, eq_4)

## Assumptions

- The algorithm is assumed to be phase-estimation-like; the abstract does not specify it.
- The register is assumed to be 2 system qubits plus 1 ancilla.
- Coefficients, orbitals and basis details are not given.

## Missing information

- Actual algorithm and circuit used
- Hamiltonian coefficients and qubit mapping
- NV spin assignment and pulse sequences
- Origin and definition of the 1e-14 Hartree uncertainty
- Bond lengths sampled
- State preparation method
