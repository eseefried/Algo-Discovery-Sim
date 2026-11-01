# Equation to Qiskit

Builds one sampled term U_k of the convex mixture as a parametrized Stinespring dilation on 1 system qubit (qubit 0) and 1 ancilla qubit (qubit 1), using standard gates only. The sampled index k and the probabilities p_k are supplied in the instance, because the classical decomposition is out of scope. The ancilla is assumed to be prepared in |0> by the runner. The circuit is: system u3, ancilla ry, ancilla-controlled cu on the system, system u3, ancilla u3. There are no measurements or resets.

Source equation run: `da94eae0-b4da-46d9-9e76-4be025f11395`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: sys (system qubit, d=2, input rho prepared by runner)
- qubit 1: anc (ancilla qubit, must start in |0>, prepared by runner)
- No classical bits: sampled index k and probabilities p_k are passed as classical instance data

## Assumptions

- d=2 with 1 system qubit and 1 ancilla qubit; ancilla dimension m=2.
- The runner prepares the system input state and the ancilla in |0>.
- Term parameters (pre, theta, ctrl, post, anc_post) are given classically and are not derived from a target channel.
- At most d^2 = 4 terms are allowed, as in the assumed Caratheodory-type bound.
- Angles are in radians and the gates are u(theta, phi, lambda), ry, and cu with global phase gamma = 0.

## Unresolved issues

- The exact definition of generalized extreme channels and the nonlinear coupled equations are unknown and not implemented.
- The ansatz yields channels whose Kraus operators are linear combinations of two fixed unitaries, so it does not cover all qubit channels or the paper's extreme channels.
- General qudit d and the gate-count and run-time scaling claims are not addressed.
- The use of ancilla measurement outcomes and classical dits is not specified.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The classical convex decomposition and its diamond-norm bound are not reconstructed. build_circuit only validates that the supplied p_k are nonnegative and sum to 1.
- `eq_2`: implemented; build_circuit (u, ry, cu, u, u gate sequence). A parametrized unitary U_k on sys+anc acts on rho (x) |0><0|. Tracing out the ancilla gives a channel with Kraus operators K_j = <j|U_k|0>_anc, each of the form a_j*V1 + b_j*V2 with fixed unitaries. This is a restricted family, not the paper's generalized extreme channels.
- `eq_3`: implemented; build_circuit (selection of terms[k] after validating probabilities). The term k is selected by the instance, since classical sampling happens outside the circuit. Averaging over k ~ p_k is left to the runner.
- `eq_4`: background; no code location. The error budget is a norm argument on the classical decomposition and gate synthesis. The circuit uses exact standard gates and does no approximation.
- `eq_5`: out_of_scope; no code location. Measurement and shot averaging are runner-side. The returned circuit is measurement-free.

## Specification changes

- eq_2: Narrowed to d=2 (1 system qubit + 1 ancilla qubit), and U_k is restricted to a fixed parametrized ansatz (single-qubit rotations plus one ancilla-controlled U gate) instead of an arbitrary unitary completion of the isometry V_k. Reason: The abstract does not define generalized extreme channels, and opaque dense unitaries are forbidden. Only a standard-gate family is implementable without inventing the paper's parametrization.
- eq_1, eq_3: Decomposition and random sampling are performed classically outside the circuit. k and p_k are supplied as instance data, and the circuit builds only the selected term. Reason: The task requires a deterministic, unitary, measurement-free operation, and the nonlinear solver is not specified.
- eq_4, eq_5: Error budget and readout are not implemented. Reason: They are analysis and measurement steps, not circuit operations.
