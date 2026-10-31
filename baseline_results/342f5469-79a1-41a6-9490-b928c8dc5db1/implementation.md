# Equation to Qiskit

Qiskit module exposing build_circuit(instance) that constructs the pre-measurement operation of one round/basis of the scoped single-qubit robust phase estimation protocol: the gate under test G(theta)=exp(-i theta X/2) (theta = pi/2 + epsilon, realized as rx(theta)) is applied k = 2^j times to the single system qubit, followed optionally by the Y-basis change S^dagger then H so that computational-basis outcome 0 corresponds to the +y eigenstate. State preparation (|0>), measurement, shot repetition, and the classical phase extraction / unwrapping (eq_4, eq_5) are left to the runner and post-processing and are not part of the returned unitary.

Source equation run: `3d6c4009-c0d5-43ea-87a1-852f954954e2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] (Qiskit qubit index 0): the single system qubit on which G(theta)=rx(theta) is applied k=2^round times (example: k=4, theta=pi/2+0.05); for basis 'Y' the circuit ends with sdg then h so computational-basis outcome 0 corresponds to the +y eigenstate; for basis 'Z' no basis change is applied. Runner prepares |0> and measures in the computational basis.

## Assumptions

- The implemented gate is modeled as an ideal X rotation rx(theta) with theta = pi/2 + epsilon (no detuning), as in the scoped specification.
- Qiskit's rx(theta) = exp(-i theta X/2) matches G(theta) in eq_1 exactly (no sign convention correction needed).
- Y-basis readout convention: computational outcome 0 after sdg, h corresponds to the +y eigenstate (|0>+i|1>)/sqrt2, consistent with eq_3.
- Nonadaptive doubling schedule k_j = 2^j is realized through the 'round' instance key; arbitrary k is also allowed for flexibility.
- The runner prepares |0> on q[0] and performs computational-basis measurement with M shots per circuit; the protocol requires building 2J such circuits (both bases, rounds 0..J-1).

## Unresolved issues

- The paper's exact robustness theorem (tolerated probability error, shot schedule M_j, constants in the Heisenberg bound) is not reconstructed and does not affect the circuit.
- Off-resonance (detuning) error estimation circuits are not implemented in this scoped construction.
- Whether the paper uses adaptive measurement choices or a different candidate-selection rule for unwrapping is unknown; the circuit itself is unaffected.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop `for _ in range(k): qc.rx(theta, qr[0])` and _resolve_theta (theta = pi/2 + epsilon). The gate under test G(theta)=exp(-i theta X/2) is exactly Qiskit's rx(theta); it is applied k times in sequence.
- `eq_2`: implemented; build_circuit: basis == 'Z' branch (comment '# eq_2'), circuit is G(theta)^k with no basis change. The Z-basis circuit variant produces the state whose computational-basis outcome-0 probability is (1+cos(k theta))/2 for input |0>; the measurement itself is done by the runner.
- `eq_3`: implemented; build_circuit: basis == 'Y' branch, `qc.sdg(qr[0]); qc.h(qr[0])`. S^dagger followed by H maps |+y> to |0>, so the runner's computational-basis measurement of outcome 0 realizes P_k^Y(+y) = (1 - sin(k theta))/2.
- `eq_4`: out_of_scope; no code location. Classical extraction of the wrapped phase from empirical probabilities is post-processing of measurement data, not part of the returned unitary operation.
- `eq_5`: out_of_scope; no code location. Iterative unwrapping across rounds is classical post-processing combining results of several circuits; the module only builds one round/basis circuit (the doubling schedule k=2^round is supported via the 'round' key).
- `eq_6`: background; no code location. Heisenberg scaling is a statistical property of the full protocol's estimate and is not a circuit element.

## Specification changes

- eq_2, eq_3, eq_4, eq_5: The module implements only the unitary portion of a single (round j, basis b) circuit: G(theta)^k followed by the optional S^dagger H basis change. State preparation, measurement, shot repetition, phase extraction and unwrapping are left to the runner/post-processing. Reason: The task requires a measurement-free unitary operation with no input-state preparation; the multi-circuit protocol and classical estimator cannot be expressed as one QuantumCircuit.
- eq_1: Repetition count k is capped at 4096 (round index capped at 12) and must be a positive integer; theta may be supplied directly or via epsilon. Reason: Resource cap to keep circuits of bounded size; direct theta input generalizes the instance without altering the model.
