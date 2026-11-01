# Equation to Qiskit

Implements eq_1: a first-order Trotter product formula, (prod_j exp(-i c_j P_j t/r))^r, for a user-supplied Pauli-sum Hamiltonian H = sum_j c_j P_j on n <= 12 qubits. Each Pauli rotation uses basis change, CNOT parity ladder and RZ. The circuit has no state preparation, measurement or error analysis. The bound in eq_2 and the ground-state error in eq_3 are classical post-analysis and are out of scope.

Source equation run: `459efc7f-8ca4-4879-82cc-400f2a72300d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'sys' has num_qubits qubits (max 12); qubit i is spin orbital i under an assumed Jordan-Wigner encoding, with qubit 0 the least significant bit.
- Pauli strings use Qiskit ordering: the rightmost character acts on qubit 0, the leftmost on qubit n-1.
- Example: 4 qubits, sys[0..3]. No ancillas. Input state is prepared by the runner.

## Assumptions

- Hamiltonian terms are Hermitian Pauli strings with real coefficients, and the user supplies them.
- First-order (Lie-Trotter) formula with the term order as given.
- Rightmost Pauli character acts on qubit 0 (Qiskit convention).
- Jordan-Wigner mapping, if any, is applied by the caller when building the terms.
- Time t is real and may be negative or zero.

## Unresolved issues

- The paper's actual error bounds, chemistry-dependent scaling and step-size selection are not recoverable from the abstract.
- The improved state-preparation method is not implemented.
- No molecular Hamiltonian is generated. The example coefficients are illustrative only.
- Ground-state error evaluation (eq_3) must be done outside this circuit.

## Equation mapping

- `eq_1`: implemented; build_circuit (outer loop over r steps) and _pauli_rotation (each factor exp(-i c_j P_j t/r)). Implements U_r(t) = (prod_j exp(-i H_j t/r))^r with H_j = c_j P_j, applied in the listed term order within each step. Each exponential uses basis change, CNOT parity ladder and RZ(2 c_j t/r). Identity terms contribute only a global phase.
- `eq_2`: out_of_scope; no code location. The norm bound delta(t,r,H) is a classical analytical quantity and is left unspecified in the specification. It does not correspond to any circuit operation.
- `eq_3`: out_of_scope; no code location. The ground-state energy error needs state preparation, an evolved-state expectation value and classical post-processing. Those steps are excluded from this operation-only circuit.

## Specification changes

- eq_1: Scoped H_j to real-coefficient Pauli strings c_j P_j on n <= 12 qubits, supplied explicitly in the instance. The circuit applies the factors in the supplied order. Reason: The abstract gives no molecular Hamiltonian or term decomposition, so a generic Pauli-sum Trotter operation is the only implementable construction.
- eq_2, eq_3: Excluded the error bound and ground-state error analysis from the circuit. Reason: They are classical analysis quantities, not unitary operations. Their explicit forms are unspecified, and eq_3 needs state preparation and measurement, which the runner handles.
- eq_1: Capped steps at 1000 and terms at 200. Reason: Bounds circuit size for safe generation.
