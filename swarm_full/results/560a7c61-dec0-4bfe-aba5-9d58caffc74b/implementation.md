# Equation to Qiskit

Builds the miter circuit V^dagger U on n data qubits (eq_3). Two user-described unitary gate lists U and V are validated and assembled. U is applied first, then the exact inverse of V. If U equals e^{i theta} V, the composite acts as identity up to a global phase. The circuit contains no state preparation or measurement. State-vector equivalence (eq_1, eq_2) is a classical comparison and is not a circuit.

Source equation run: `e4ad5601-243f-4e33-bbd3-16cdf90ccfb5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: data register q (qubit 0 is least significant bit); both U and V act on this same register
- No ancilla qubits, no classical bits
- Gate qubit indices in the instance refer directly to these Qiskit indices

## Assumptions

- Both circuits are unitary, measurement-free and ancilla-free on the same n qubits (from eq_3).
- The generic miter formulation stands in for the paper's unspecified algorithm.
- Instance format: {n, U:[{name, qubits, params?}], V:[...]}.
- Rotation and phase angles are in radians.

## Unresolved issues

- The paper's actual equivalence-checking algorithms and data structures are not given in the abstract and are not reproduced.
- The full list of equivalence notions in the paper is unknown.
- Hundreds-of-qubit scalability is outside this construction because of the 12-qubit cap.

## Equation mapping

- `eq_1`: background; no code location. Exact state equality is a classical vector comparison made by the runner or verifier. It is not a unitary operation and is not implemented as a circuit.
- `eq_2`: background; no code location. Equivalence up to a global phase is a property to check on outputs. A circuit cannot detect global phase, so no code is emitted.
- `eq_3`: implemented; build_circuit (compose U, then v.inverse()) with _build_part. Constructs V^dagger U from the user-supplied gate lists. If U equals e^{i theta} V, the circuit acts as the identity up to a global phase.

## Specification changes

- eq_3: Narrowed scope to the miter construction V^dagger U for unitary circuits given as explicit gate lists, with a fixed gate set of at most 500 gates each. The set is h, x, y, z, s, sdg, t, tdg, rx, ry, rz, p, cx, cz, swap, cp. n is at most 12. Reason: A finite, validated, parameterized instance format is needed. The abstract gives no benchmark circuits or algorithm.
- eq_1, eq_2: No circuit is generated for state equivalence. Comparing states exactly or up to phase is left to classical post-processing. Reason: The task asks for a measurement-free unitary operation without input preparation, and state equality is not an operation.
- eq_3: The proportionality to identity is not enforced or checked inside the circuit. The circuit only produces V^dagger U, and the global phase is not tracked. Reason: The check is an analysis step on the resulting operator or on measurement statistics, which software does after generation.
