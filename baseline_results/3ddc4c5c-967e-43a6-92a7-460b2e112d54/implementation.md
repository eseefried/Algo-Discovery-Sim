# Equation to Qiskit

Implements the single-attempt unitary of the one-ancilla RUS squaring/multiplication primitive (eq_2/eq_4): ancilla pre-rotation e^{-i phi1 X}, controlled-(-iX) from ancilla onto target (CX followed by Sdg on the control), ancilla post-rotation e^{+i phi2 X}. The runner prepares |0> on the ancilla and measures it; outcome 0 leaves e^{-i theta X} on the target with tan(theta)=tan(phi1)tan(phi2) (squaring when phi1=phi2). Measurement, failure correction and repetition (eq_3, eq_6) are classical-control aspects outside the returned unitary.

Source equation run: `7d2283dd-b549-4e3f-b4b9-8026b347a50c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: target t (1 qubit) - receives e^{-i theta X} on ancilla outcome 0, tan(theta)=tan(phi1)*tan(phi2); input state |psi> arbitrary (prepared by runner)
- qubit 1: ancilla a (1 qubit) - runner prepares |0>, circuit applies rx(2 phi1), CX(a->t), Sdg(a), rx(-2 phi2); runner measures a in Z basis: 0 = success, 1 = failure
- example: phi = pi/8 -> success probability 3/4, theta = arctan(3 - 2 sqrt 2) ~ 0.1699 rad; failure branch applies e^{+i pi X/4} to t

## Assumptions

- Angles phi, phi1, phi2 are classically known real numbers; no range restriction is enforced beyond finiteness, though the arithmetic interpretation (theta ~ phi1*phi2) holds only for small angles.
- The runner prepares the ancilla (qubit 1) in |0> and measures it in the computational basis after the circuit; outcome 0 signals success.
- The target qubit (qubit 0) may be in an arbitrary input state.
- Ideal gates; rx(lam) = exp(-i lam X/2) so e^{-i phi X} = rx(2 phi).

## Unresolved issues

- The implemented primitive was derived in the math stage and may differ from the paper's actual two basic RUS primitives.
- The 3-ancilla multiplication and reciprocal circuits, composition for general smooth f, and error/resource analysis remain out of scope.
- Failure correction for the two-angle variant with phi1 != phi2 is not a fixed rotation and is not addressed.

## Equation mapping

- `eq_1`: background; no code location. Defines the target family e^{-i f X}; the implemented circuit realises the special case f = arctan(tan phi1 tan phi2) but eq_1 itself is a definition, not an operation.
- `eq_2`: implemented; build_circuit: comments 'eq_2 / eq_4 step 1', 'eq_2 step 2', 'eq_2 / eq_4 step 3' (rx, cx+sdg, rx on ancilla). The full pre-measurement unitary of the one-ancilla squaring primitive is built; projecting the ancilla onto <0| yields K_0 = cos^2 phi I - i sin^2 phi X.
- `eq_3`: background; no code location. Success probability and failure Kraus operator are consequences of the eq_2 unitary; the measurement and the e^{-i pi X/4} correction are non-unitary / classical-control steps performed by the runner, not part of the returned operation.
- `eq_4`: implemented; build_circuit: branch reading 'phi1'/'phi2'; same gate sequence with rx(2 phi1) pre- and rx(-2 phi2) post-rotation. The two-angle variant is supported by allowing distinct phi1 and phi2 in the instance, giving K_0 = cos phi1 cos phi2 I - i sin phi1 sin phi2 X on ancilla outcome 0.
- `eq_5`: background; no code location. Small-angle Taylor expansion explaining the sense of 'approximate' multiplication; purely interpretive, no circuit content.
- `eq_6`: out_of_scope; no code location. Geometric attempt statistics concern the repeat loop, which requires mid-circuit measurement and classical control; the module returns only a single-attempt unitary.

## Specification changes

- eq_2, eq_3, eq_6: Only the single-attempt unitary (before ancilla measurement) is returned; ancilla state preparation, Z measurement, the failure correction e^{-i pi X/4} and repetition are left to the runner. Reason: Task constraints require a measurement-free, unitary circuit without reset or dynamic control.
- eq_2: Controlled-(-iX) realised as CX(a->t) followed by Sdg on the ancilla control, rather than a generic controlled-RX gate. Reason: Exact standard-gate decomposition: controlled-U with U = -iX equals CX times a phase of -i on the control=|1> subspace, which Sdg = diag(1,-i) provides.
- eq_2, eq_4: Tensor order (a,t) in the specification is mapped to Qiskit layout target = qubit 0 (least significant), ancilla = qubit 1. Reason: Qiskit little-endian convention: the leftmost tensor factor is the highest qubit index.
- eq_4: For phi1 != phi2 the failure branch is not a fixed correction; the module makes no attempt to handle it (no scope for the paper's 3-ancilla multiplication circuit). Reason: Failure handling for distinct angles was unspecified in the math stage; only the success-branch unitary is implemented.
