# Equation to Qiskit

No circuit was generated. The specification describes only a classical absorbing-Markov-chain framework and an asymptotic gate-count claim. It gives no explicit PQF unitaries, ancilla count, measurement bases, fallback rules, or gate-set-specific constructions. Implementing any of these would mean inventing the protocol, and the task also forbids measurements, dynamic circuits and hardcoded outputs.

Source equation run: `9fa3f7bc-ff2d-45b1-9abc-ed1e4b085856`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Explicit state space and transition unitaries for PQF are not given.
- The definition and values of b per gate set are not given.
- The fallback rule details are not given.
- The measurement bases and outcomes are not given. The protocol also needs mid-circuit measurement and classical control, which are excluded from the required measurement-free unitary output.
- The ancilla count is not given.
- No public validation contract or requested instance was supplied to narrow the scope.

## Equation mapping

- `eq_1`: out_of_scope; no code location. This is an asymptotic expected-gate-count claim with an unspecified b. It is not a unitary operation and cannot be built as a circuit.
- `eq_2`: out_of_scope; no code location. This is the classical block form of the transition matrix. Realizing it needs the unspecified PQF unitaries plus mid-circuit measurements, which are not allowed in a measurement-free unitary circuit.
- `eq_3`: background; no code location. This is standard absorbing-chain theory for the fundamental matrix. It is classical post-processing, not a quantum operation.
- `eq_4`: out_of_scope; no code location. This is a classical cost-accounting formula based on an assumed cost model. It has no circuit realization.
- `eq_5`: out_of_scope; no code location. This is a nilpotency condition on the transient block that expresses finite termination. It is a property of the protocol and cannot be built without the fallback rules.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5: Abstained from implementing any construction. No scope was narrowed to a smaller circuit. Reason: The specification lists the missing information (state space, transition unitaries, definition of b, fallback rules, measurement bases, ancilla count). It contains no single unitary construction that can be implemented without inventing details.
