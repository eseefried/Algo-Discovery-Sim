# Equation to Qiskit

Single-qubit operation implementing the k-fold repeated coherent systematic-rotation gate U^k = exp(-i k phi n.sigma/2) from eq_2. The gate is applied as k literal repetitions of a standard-gate decomposition of a rotation by phi about a user-specified axis n. An optional unitary basis-change (Z, X or Y) is appended so a later computational-basis measurement would give the quadrature probabilities. There is no state preparation, measurement or estimation.

Source equation run: `6338ed86-b35d-4935-a8d1-0ae0210358af`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: the single qubit q on which the gate under test is repeated k times (Qiskit index 0, little-endian irrelevant for one qubit); input state prepared by the runner, no classical bits

## Assumptions

- The gate under test is a coherent rotation by angle phi about a fixed axis (illustrative model).
- The gate is applied as k explicit repetitions, not merged into a single rotation by k*phi.
- Input state preparation (e.g. |0>) and measurement are done by the runner.
- Global phase is ignored.

## Unresolved issues

- The paper's actual gate-set and error parametrization (amplitude and off-resonance errors) are not reconstructed.
- The robust phase estimation procedure, choice of k sequence and Heisenberg-scaling error analysis are not implemented.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Heisenberg scaling epsilon=O(1/N) is a statistical property of the whole estimation protocol (choice of k sequence, shots, estimator), not of a single unitary circuit.
- `eq_2`: implemented; build_circuit: loop of k repetitions of the Rz/Ry decomposition of exp(-i*phi*n.sigma/2). Each repetition is a rotation by phi about unit axis n, built as Rz(az)Ry(theta)Rz(phi)Ry(-theta)Rz(-az); k repetitions give U^k = exp(-i k phi n.sigma/2).
- `eq_3`: background; no code location. P(0|k)=cos^2(k phi/2) is the outcome statistic the runner would see for input |0>, axis along x and basis Z; it is not constructed in code. The circuit only supplies the unitary, and the optional basis change selects the measured quadrature.

## Specification changes

- eq_1, eq_3: Scope narrowed to the unitary part of one experiment: k-fold gate plus optional basis-change rotation. Measurement, shot sampling, multiple k values, phase unwrapping and the robust estimator are excluded. Reason: The task requires an operation without measurement or sampling, and the abstract does not specify the estimator.
- eq_2: The rotation axis n is an instance parameter (normalized internally), and k is capped at 1024. The error model is the illustrative coherent rotation, not the paper's actual amplitude/off-resonance gate-set model. Reason: The abstract gives no explicit error model; the axis choice lets the same circuit cover an amplitude-like or off-resonance-like tilted rotation, and the cap bounds circuit size.
- eq_3: The basis-change rotation is limited to the Z (identity), X (H) and Y (Sdg then H) bases. Reason: The abstract does not specify the basis-change rotation, and these are the standard quadrature choices.
