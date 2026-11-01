# Equation to Qiskit

Qiskit operation for the phase-gate distribution stage of generalized Kitaev phase estimation. On M probe qubits (qubit j = Qiskit index j), n_j copies of the single-qubit phase gate P(phi) are applied, so qubit j acquires phase n_j*phi, with N = sum n_j. The default distribution is the standard Kitaev n_j = 2^j, and arbitrary non-negative integer counts are accepted. Input product-state preparation (e.g. |+>), measurement, the estimator and the error analysis are left to the runner or out of scope.

Source equation run: `31997fec-73e0-4d23-ba5f-95774293f8a3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] (Qiskit index 0): probe qubit j=0, receives n_0 phase gates P(phi)
- q[1] (index 1): probe qubit j=1, receives n_1 phase gates
- q[j] (index j): probe qubit j, receives n_j phase gates; j = 0..M-1, M<=12
- Encoding: computational basis; |1> of qubit j picks up phase exp(i*n_j*phi) relative to |0>. Runner is expected to prepare |+> on each qubit.
- No ancilla qubits; total qubits = M

## Assumptions

- Phase gate is P(phi)=diag(1,exp(i*phi)) on a single probe qubit.
- Each qubit j receives n_j gates with N = sum n_j; default n_j = 2^j (standard Kitaev) when gate_counts is omitted.
- Input state is a product state such as |+>^M prepared externally by the runner.
- Total gate number is capped at 4096 and qubits at 12 for safety.

## Unresolved issues

- Optimal gate distribution for the generalized algorithm is not specified in the abstract.
- Loss model, Bayesian bound formula and alternative resource quantification are not specified and not implemented.
- Measurement basis and estimator are not part of the operation and remain unspecified.

## Equation mapping

- `eq_1`: background; no code location. Scaling claim (MSE ~ 1/N) for the standard algorithm; it is a statistical statement, not a circuit. The default gate_counts n_j=2^j in build_circuit only reproduces the standard gate distribution, not the error scaling.
- `eq_2`: out_of_scope; no code location. Heisenberg 1/N^2 scaling depends on the optimal distribution, estimator and error analysis, none of which are given in the abstract. The circuit accepts arbitrary gate_counts but does not implement the optimal choice or the scaling.
- `eq_3`: out_of_scope; no code location. MSE definition is classical post-processing/evaluation and involves measurement and an estimator, which are excluded from the operation.

## Specification changes

- eq_1, eq_2: Scope narrowed to the unitary phase-gate distribution stage: n_j copies of P(phi) on qubit j with caller-supplied (or default 2^j) counts. Reason: The equations are scaling statements about estimation error; only the gate distribution is expressible as a circuit operation. The optimal distribution is not given in the abstract.
- eq_3: Measurement, estimator, and error computation are omitted. Reason: The operation must be measurement-free and contain no state preparation or sampling; these are performed by the runner.
- eq_1: Each phase gate is taken to be P(phi)=diag(1,e^{i phi}) acting on one qubit, applied repeatedly rather than merged into P(n_j*phi). Reason: The abstract does not define the gate; this is the standard Kitaev form and matches counting N as the number of gate uses.
