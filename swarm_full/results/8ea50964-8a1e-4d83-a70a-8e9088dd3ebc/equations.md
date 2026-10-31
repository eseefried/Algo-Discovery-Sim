# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Estimate the gate-count complexity of Trotter-based quantum simulation of molecular electronic Hamiltonians as a function of the number of spin orbitals N. Revisit the earlier N^8 scaling claim, which relied on random artificial molecules, and compare it with real model molecules (worst case about N^6). Also compare an alternative simulation scheme and a coalescing scheme that uses different Trotter steps for different terms, with an efficient classical bounding method.

Scope: Abstract-level reconstruction of the complexity-scaling analysis only. No explicit circuit, molecule data, Trotter error bounds, or numerical results are specified. Equations are limited to the two scaling relations stated in the abstract plus one standard background Hamiltonian form. The abstract describes a resource-scaling study, not a state-preparation or measurement algorithm.

## Symbols

- $N$: number of spin orbitals; domain: positive integer, N~100 as an example
- $G(N)$: gate count of the molecular simulation; domain: positive integer-valued function of N
- $H$: molecular electronic Hamiltonian expressed as a sum of terms; domain: Hermitian operator on N qubits (after fermion-to-qubit mapping)

## eq_1: Prior scaling claim

$$
G(N)\sim N^{8}
$$

Earlier reported gate-count scaling with the number of spin orbitals.

Provenance: `abstract_explicit`. Stated in the abstract as the earlier result.

Abstract evidence: the complexity in gate count of such simulations increases with the number of spin orbitals $N$ as $N^{8}$

## eq_2: Revised worst-case scaling

$$
G(N)\sim N^{6}
$$

Worst-case scaling found for the real model molecules studied.

Provenance: `abstract_explicit`. Stated in the abstract as the revised result.

Abstract evidence: the scaling is closer to $N^{6}$ in worst case for real model molecules we have studied

## eq_3: Second-quantized Hamiltonian

$$
H=\sum_{pq}h_{pq}a_p^\dagger a_q+\tfrac12\sum_{pqrs}h_{pqrs}a_p^\dagger a_q^\dagger a_r a_s
$$

Standard molecular Hamiltonian whose terms are Trotterized.

Provenance: `standard_background`. Standard background form for molecular simulation, not given in the abstract.

Equation assumptions:

- Standard second-quantized electronic structure Hamiltonian in a spin-orbital basis

## Registers

- system: N qubits qubits; One qubit per spin orbital after a fermion-to-qubit mapping (assumed)

## Initial state

Assumed: a reference state such as Hartree-Fock on the system register; not specified in the abstract.

## Algorithm steps

1. Map fermionic H to qubit operators and group it into terms (assumed Jordan-Wigner or similar). (eq_3)
2. Apply a Trotter step: product of exponentials of the terms. Gate cost per step is analyzed as a function of N. (eq_3, eq_1, eq_2)
3. Optionally use coalescing, with different Trotter steps for different terms, or the alternative scheme; compare the resulting gate counts. (eq_2)

## Assumptions

- The Hamiltonian form in eq_3 is background, not taken from the abstract.
- Register layout, initial state and mapping are assumed, not from the abstract.
- Qubit-per-spin-orbital encoding and a reference initial state are assumed.
- No measurement is specified because the abstract concerns gate-count bounds; none is invented.
- Measurement and postprocessing are left null because the abstract describes resource-scaling analysis only.

## Missing information

- Trotter step size and error bounds
- Specific molecules and basis sets
- Details of the alternative scheme and the coalescing scheme
- The efficient bounding method
- Circuit, measurement, and postprocessing details
- Quantitative comparison of the schemes
