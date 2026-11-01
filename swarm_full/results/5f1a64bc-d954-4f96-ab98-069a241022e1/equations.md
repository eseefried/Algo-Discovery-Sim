# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Compute the ground-state energy of minimal-basis HeH+ as a function of bond distance (bond dissociation curve) on a solid-state NV-center quantum register in diamond, using a quantum algorithm for molecular energies.

Scope: Abstract-level reconstruction of a small quantum chemistry experiment on an NV-center register; the specific algorithm, Hamiltonian coefficients, circuits and measurement details are not given in the abstract and are only labeled background or assumption.

## Symbols

- $H(R)$: Qubit-encoded electronic Hamiltonian of minimal-basis HeH+ at bond distance R; domain: Hermitian operator on a few qubits
- $R$: He-H internuclear distance; domain: positive real
- $E_0(R)$: Ground-state energy giving the dissociation curve point; domain: real, Hartree
- $\Delta E$: Reported energy uncertainty; domain: real, Hartree

## eq_1: Ground-state energy

$$
E_0(R)=\min_{|\psi\rangle}\langle\psi|H(R)|\psi\rangle
$$

Ground-state energy of the molecular Hamiltonian at each bond distance, by the variational principle, as a basis for the dissociation curve.

Provenance: `standard_background`. Standard electronic structure and variational principle; the abstract states only that the bond dissociation curve is computed. It is not confirmed as the paper's method.

Equation assumptions:

- Energy is obtained via a variational or phase-estimation-type method; the abstract does not specify which.

## eq_2: Reported uncertainty scale

$$
\Delta E\sim10^{-14}\,\text{Hartree}
$$

Reported energy uncertainty given the model basis.

Provenance: `abstract_inferred`. Directly stated in the abstract.

Abstract evidence: energy uncertainty (given our model basis) of the order of $10^{-14}$ Hartree

## Registers

- system: 2 (assumed) qubits; Encodes the minimal-basis HeH+ electronic state, e.g. NV electron spin plus nuclear spin
- ancilla: unknown (possibly 0 or 1) qubits; Possible readout or phase-estimation qubit; not specified in the abstract

## Initial state

Assumed reference state |00> (or Hartree-Fock-like product state) on the system register.

## Measurement

Assumed: read out the NV register spin states (optical readout of the electron spin, with nuclear spin readout mapped to it). Expectation values of Hamiltonian terms or phase-estimation outcomes are estimated from repeated runs.

## Classical postprocessing

Assumed: combine measured expectation values with Hamiltonian coefficients (or convert phase to energy), then sweep R to form the dissociation curve and estimate the uncertainty \Delta E.

## Algorithm steps

1. For each bond distance R, build the qubit Hamiltonian H(R) for minimal-basis HeH+ (assumed precomputed classically). (eq_1)
2. Prepare the ground-state estimate on the NV register with assumed algorithm-specific control pulses (a variational ansatz or controlled time evolution under H(R)). (eq_1)
3. Extract the energy estimate E_0(R) at each R and trace out the dissociation curve, compared against the stated uncertainty scale. (eq_1, eq_2)

## Assumptions

- Minimal-basis HeH+ is mapped to a small qubit Hamiltonian.
- Register sizes, initial state, circuit steps and measurement scheme are assumed generic, not taken from the abstract.
- Two-qubit system register assumed; optional ancilla.
- Optical or spin readout assumed.

## Missing information

- Algorithm used (e.g., phase estimation vs variational)
- Hamiltonian coefficients and qubit mapping
- Number of qubits and circuit details
- Measurement and postprocessing details
- How the 10^-14 Hartree uncertainty is defined and obtained (statistical vs systematic, model-basis dependence)
