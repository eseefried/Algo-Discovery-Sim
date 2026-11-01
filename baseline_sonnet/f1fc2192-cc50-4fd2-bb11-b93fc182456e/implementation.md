# Equation to Qiskit

Abstained. The abstract does not give the two RUS primitives, the ancilla circuits, the angle encoding, or the success and failure Kraus operators. A circuit built only from the target rotation RX(2*phi1*phi2) with classically computed angles would be a direct parameterized gate. It would not be a RUS multiplication construction and would not use the specified ancilla register, so no code is emitted.

Source equation run: `9c1a7fb1-afe9-41fe-b291-541e2f8e0137`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- The two basic primitives used to synthesize f are unspecified.
- The explicit RUS circuits and gate set are unspecified.
- How inputs phi_j are encoded in gates is unspecified.
- The Kraus operators K and K_fail, the success probability and the error scaling are unspecified.
- The failure-recovery procedure is unspecified and needs dynamic circuits, which are disallowed.
- The reciprocal construction is unspecified.
- No public validation contract or requested instance was supplied.

## Equation mapping

- `eq_1`: background; no code location. Defines the target rotation exp(-i f X) = cos f I - i sin f X. Without the RUS primitives it cannot be realized as a faithful construction, and a direct RX(2f) gate would bypass the RUS framework.
- `eq_2`: background; no code location. Approximation criterion under an assumed operator-norm error metric. It is an analysis condition, not a gate operation, and no circuit is generated to test it.
- `eq_3`: background; no code location. Generic RUS Kraus completeness. It needs mid-circuit measurement and classical control, which are excluded from a unitary measurement-free circuit, and the specific K and K_fail are unknown.
- `eq_4`: background; no code location. Expected number of attempts for a geometric process. It is a classical statistical property and has no circuit realization.
- `eq_5`: out_of_scope; no code location. The multiplication target f = phi1*phi2 would need the paper's unspecified RUS multiplication circuit, including its 3-ancilla construction and angle encoding. These cannot be reconstructed from the abstract.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5: Narrowed the implementation scope to nothing; no circuit is generated. Reason: The essential RUS primitives, circuits and encodings are missing from the abstract. The RUS success/failure flow needs measurement and classical feedback, which this unitary, measurement-free operation format excludes. Any gate sequence written here would be fabricated.
