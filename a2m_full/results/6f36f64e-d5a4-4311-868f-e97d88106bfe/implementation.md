# Equation to Qiskit

Scoped to a deterministic, ancilla-free, unitary single-qubit construction. A group-commutator sequence of Z and Y rotations approximates exp(-i a b X) up to third-order error, and an optional exact X-rotation shift implements additive composition. This is NOT the paper's RUS gadget: the RUS sequences, ancilla measurements and corrections are not in the specification, so none are implemented.

Source equation run: `b654293b-3507-4494-9ac2-f8989116a24e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: target t (computational basis, little-endian; input state prepared by the runner)
- no ancilla qubits; total qubits = 1

## Assumptions

- Small-angle regime: |a|,|b| <= 1 enforced, with accuracy expected only for |a|,|b| << 1
- The input state is prepared by the runner (e.g. target |0>)
- The commutator construction is an acceptable stand-in for the product primitive's ideal action
- Qiskit rx(t)=exp(-i t X/2), ry and rz similarly

## Unresolved issues

- The actual RUS circuits, ancilla count (3) and success probabilities are not reproduced
- Reciprocal gadget function (arctan(c/theta) vs theta/(theta^2+c^2)) is unresolved
- Error is only leading-order; no amplification or correction is included

## Equation mapping

- `eq_1`: implemented; build_circuit (overall target exp(-i f X) with f = a*b + shift). The circuit approximates U_f for the specific function f(a,b,shift)=a*b+shift.
- `eq_2`: implemented; build_circuit: ry(b), rz(-2a), ry(-b), rz(2a) block. Product primitive realised by a unitary group-commutator, not a RUS gadget; the error is third order in the angles.
- `eq_3`: out_of_scope; no code location. The reciprocal function is a guess in the specification and its gadget is unknown; not implemented.
- `eq_4`: implemented; build_circuit: optional rx(2*shift) term. Only the additive composition rule is implemented, as an exact commuting X rotation. Nesting of multiplication and inversion is out of scope.
- `eq_5`: background; no code location. RUS success-branch post-selection and the readout <Z>=cos(2f) are experiment-side analysis; the circuit has no measurement or post-selection.

## Specification changes

- eq_2, eq_5: Replaced the RUS product gadget (ancillas, mid-circuit measurement, post-selection) with a deterministic ancilla-free unitary commutator construction. Reason: The RUS gate sequences and Kraus operators are not specified, and dynamic circuits and measurements are disallowed.
- eq_2: The effective angle ab is obtained from Z-rotation angle a and Y-rotation angle -b/2 (in the exponent), with the sign and factor fixed by [Z,Y]=-2iX. Reason: The commutator identity gives exp(-i(-2 a b')X); choosing b'=-b/2 yields exactly exp(-i a b X) at leading order.
- eq_1, eq_3, eq_4: Scope narrowed to f = a*b + shift; the reciprocal and general nesting are not implemented. Reason: The reciprocal function and error behaviour are unresolved in the specification.
