# Equation to Qiskit

Trotterized time-evolution operator exp(-i H_P t) for the reduced BCS pairing Hamiltonian in a pair-occupation (hard-core boson / pseudospin-1/2) qubit mapping. Each qubit is one pair level (|1> is an occupied pair). The circuit uses single-qubit RZ gates for the level energies and RXX/RYY gates for the all-to-all pair-hopping terms, in first- or second-order product-formula steps. No state preparation or measurement is included.

Source equation run: `e948ab4b-9686-4c7c-91db-e11714fa16fb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit j (0..n_levels-1) = pair level j; qubit 0 is the least significant bit
- |0> = pair-empty level, |1> = pair-occupied level; n_pair=(1-Z)/2, b_j^dagger=sigma^+_j
- no ancilla qubits

## Assumptions

- Reduced BCS pairing Hamiltonian with level-independent coupling G
- One qubit per pair level, with pairs treated as hard-core bosons (seniority-zero subspace)
- The Trotter order is 1 or 2 and the number of steps is a user parameter, so the circuit is only an approximation to exact evolution
- The global phase is tracked on the circuit

## Unresolved issues

- The paper's actual algorithms, native Hamiltonian types (Ising/XY/Heisenberg), and gate sequences are unknown
- Nearest-neighbor connectivity constraints are not modeled
- The energy spectrum measurement scheme and complexity analysis are not implemented
- Trotter error and the fidelity study are left to downstream evaluation

## Equation mapping

- `eq_1`: implemented; build_circuit with helpers _local (level-energy terms) and _pairs (pair-hopping terms). H_P is mapped to H = sum_j (2 eps_j - G)(1-Z_j)/2 - (G/2) sum_{j<k}(X_jX_k+Y_jY_k). The j=k part of the double sum gives -G n_j. The circuit implements a Trotter product formula of exp(-iHt).
- `eq_2`: out_of_scope; no code location. Fidelity is a classical post-analysis metric of a prepared state against a target state. It is not part of the unitary operation.

## Specification changes

- eq_1: Scoped to Trotterized real-time evolution under the reduced BCS Hamiltonian, which is a generic abstract-level construction. The paper's actual algorithms, gate sequences, and native-interaction decompositions are not reproduced. Reason: The abstract gives no explicit algorithm. This is the only well-defined operation derivable from the specification.
- eq_1: The abstract's nearest-neighbor interaction constraint is not enforced. The circuit uses all-to-all RXX/RYY gates rather than a nearest-neighbor decomposition. Reason: Platform-specific decompositions are missing from the specification.
- eq_1: Made the qubit mapping and constants explicit: hard-core pair bosons with n_pair=(1-Z)/2, fermion-count energy 2*eps_j per pair, and the j=k term of the double sum folded into an effective level energy 2*eps_j - G. Reason: eq_1 left the mapping unspecified, and the j=k term must be handled for a consistent Hamiltonian.
- eq_2: No circuit is produced for fidelity, and no spectrum-measurement circuit is produced. Reason: The operation is measurement-free, and the measurement scheme is unspecified.
