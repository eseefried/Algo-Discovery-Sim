# Equation to Qiskit

No circuit generated. The specification describes continuous-variable optical phase estimation with a classical robust fixed-interval smoother. It has no gate-based unitary, no finite register, and no fixed construction. Squeezed light, homodyne records, stochastic processes, and minimax smoothing cannot be turned into a faithful finite-qubit Qiskit operation without inventing details the abstract does not give.

Source equation run: `9cd24e7e-7a58-4819-ae2a-47cd182da1e1`

Generation: **unsupported**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- No gate-based operation is specified in the abstract.
- The phase noise model, uncertainty set, and robust smoother algorithm are unspecified; the spec assumed them.
- Squeezing level and measurement scheme are unspecified.
- No public validation contract or requested instance was supplied.
- Equations are classical estimation-theory statements and not circuit equations.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Assumed Wiener phase-diffusion model is a continuous-time classical stochastic process. It has no finite-qubit unitary form without an arbitrary discretization or encoding.
- `eq_2`: background; no code location. Fixed-interval smoothing is a classical conditional expectation over a measurement record. It is postprocessing, not a quantum operation.
- `eq_3`: out_of_scope; no code location. Minimax MSE criterion is a classical optimization design criterion (and an assumption in the spec). It is not a circuit operation.

## Specification changes

- eq_1, eq_2, eq_3: Abstained from implementation; no scope narrowing to a qubit construction was attempted. Reason: The task needs an operation-only unitary circuit, but the specification is an abstract-level continuous-variable estimation problem. Any qubit circuit would require invented encodings, such as a truncated Fock space or discretized phase register, and an invented noise model.
