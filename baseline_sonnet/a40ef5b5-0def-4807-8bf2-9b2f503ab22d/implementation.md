# Equation to Qiskit

Builds a 3-qubit circuit for one ancilla-controlled Trotterized time-evolution operation controlled-exp(-i H tau), where H is a user-supplied 2-qubit Pauli-sum Hamiltonian (the HeH+ minimal-basis form). It contains no state preparation, measurement or phase-estimation readout. The identity term becomes a phase gate on the ancilla and each Pauli term becomes a controlled Pauli rotation. Trotter order 1 or 2 is selectable.

Source equation run: `d94573af-a0ff-4ee7-b7bd-ce120c860698`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: ancilla (control register 'anc'), used as the phase-kickback control
- qubit 1: system qubit 0 (least significant; rightmost character of a Pauli label)
- qubit 2: system qubit 1 (leftmost character of a Pauli label)
- Pauli label 'AB' = A on qubit 2, B on qubit 1 (Qiskit little-endian)
- Coefficients are ordinary real numbers in Hartree; the example values are illustrative placeholders, not actual HeH+ data

## Assumptions

- Register is 1 ancilla plus 2 system qubits, as assumed in the specification.
- Pauli labels follow Qiskit little-endian ordering: the rightmost character acts on system qubit 0, which is circuit qubit 1.
- tau must be positive, and tau is assumed small enough to avoid energy aliasing in downstream analysis.
- The Hamiltonian includes the nuclear repulsion constant in the II coefficient if desired; it only produces a relative phase on the ancilla.

## Unresolved issues

- Actual HeH+ minimal-basis Pauli coefficients g_i(R) are not provided.
- The NV-center native gate set and pulse compilation are not modeled.
- The actual algorithm used in the paper is not specified in the abstract.

## Equation mapping

- `eq_1`: implemented; _parse (reads Pauli coefficients g_i) and _apply_term (one P_i term). H = sum_i g_i P_i is supplied through instance['coefficients'] as a dictionary of 2-qubit Pauli labels. The circuit uses it directly; the coefficients g_i(R) are not computed.
- `eq_2`: out_of_scope; no code location. Ground-state minimization and the dissociation curve over R are classical or experimental tasks, not part of this operation.
- `eq_3`: implemented; build_circuit loop over Trotter steps with _apply_term. The ancilla-controlled U(tau)=exp(-iH tau) is approximated by a first- or second-order Trotter product, with the identity term as a phase gate p(-g*dt) on the ancilla and other terms as controlled Pauli rotations.
- `eq_4`: background; no code location. The phase-energy relation is used only in readout and postprocessing, which the runner handles. Initial-state preparation and ancilla measurement are excluded from this operation.
- `eq_5`: out_of_scope; no code location. The 1e-14 Hartree uncertainty is a reported experimental result with no derivation given, and it is not a circuit element.

## Specification changes

- eq_1, eq_3: Scope is narrowed to a single controlled-U(tau) block for a user-supplied 2-qubit Pauli Hamiltonian at one bond length. The HeH+ coefficients are not supplied; the example uses illustrative placeholder values. Reason: The abstract gives no Hamiltonian coefficients, qubit mapping or circuit details.
- eq_3: exp(-iH tau) is implemented approximately by Trotter-Suzuki decomposition (order 1 or 2, up to 50 steps) rather than exactly. Reason: Non-commuting Pauli terms cannot be exponentiated exactly with standard gates without building a dense unitary. The error is controlled by trotter_steps.
- eq_4: The full phase-estimation and iterative readout, state preparation and measurement are excluded. The module provides only the controlled evolution operation with a fixed ancilla qubit. Reason: The task requires an operation without input-state preparation or measurement; the runner prepares inputs.
