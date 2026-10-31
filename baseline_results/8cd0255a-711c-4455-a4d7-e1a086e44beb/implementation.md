# Equation to Qiskit

Implements the circuit-equivalence 'miter' construction from the specification: given two gate-list circuits U and V on the same n qubits, build_circuit returns the difference operator W = U^dagger V (mode 'u_dag_v', decides eq_3: W is a scalar multiple of identity iff U and V are equivalent up to global phase) or W = U V^dagger (mode 'u_v_dag', decides the circuit half of eq_4: W is a diagonal unitary iff U = D V). The example instance is the n=1 pair U = X*Z (Z first, then X) and V = Y from eq_5, for which W = U^dagger V = i*I. The actual decision (checking W against identity/diagonal) is a classical post-processing step on the unitary of W and is not part of the returned operation; state-equivalence notions and the paper's decision-diagram algorithms are out of scope.

Source equation run: `290dd413-31b5-4914-8e61-37e47c9e3238`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- system[0] = Qiskit qubit 0: the single qubit of the eq_5 instance; U = X*Z (Z applied first, then X), V = Y; returned circuit W = U^dagger V = Z X Y (time order: Y, X, Z) = i*I, i.e. identity up to global phase (eq_3 satisfied, eq_1 fails).
- General instance: system[k] = Qiskit qubit k for k in 0..n-1 (Qiskit little-endian: qubit 0 is the least-significant basis-index bit); gate 'qubits' entries refer directly to these physical indices; total qubits = n <= 12.

## Assumptions

- Compared circuits U and V are given as whitelisted standard-gate lists (single-qubit Paulis/Clifford/T/sx, rx/ry/rz/p, cx/cy/cz/ch/swap, cp/crx/cry/crz/rxx/rzz, ccx/cswap) in time order on the same n qubits; gate parameters are finite real floats in radians.
- mode defaults to 'u_dag_v' (global-phase miter) when omitted; params defaults to an empty list when omitted.
- Empty gate lists are accepted and denote the identity circuit.
- The paper's compact decision-diagram algorithms and benchmark circuits are not reconstructable from the abstract and are replaced by this explicit gate-level miter construction.

## Unresolved issues

- The paper's actual set of equivalence notions and its scalable (hundreds of qubits) algorithms remain unknown; the miter construction here is a standard dense-unitary-checkable surrogate limited to n <= 12.
- No numerical tolerance is defined for deciding when W is 'identity up to phase' or 'diagonal'; that choice belongs to the classical post-processing stage.

## Equation mapping

- `eq_1`: background; no code location. Exact entrywise equality is a classical comparison of representations; the miter W = U^dagger V equals the identity exactly iff eq_1 holds for circuits, but the check itself is post-processing on W, not part of the operation.
- `eq_2`: out_of_scope; no code location. State global-phase equivalence requires state vectors / input preparation, which the operation-only contract forbids; not implemented.
- `eq_3`: implemented; build_circuit, branch mode == 'u_dag_v' (comment 'eq_3: W = U^dagger V'). Builds W = U^dagger V by applying V then U.inverse(); W is e^{i theta} I (|Tr W| = N) iff U and V are equivalent up to global phase.
- `eq_4`: implemented; build_circuit, branch mode == 'u_v_dag' (comment 'eq_4 (circuit part): W = U V^dagger'). Circuit half only: builds W = U V^dagger, which is a diagonal unitary D iff U = D V. The state half (squared-moduli comparison) is a classical state check and is not implemented.
- `eq_5`: implemented; example_instance_json and _build_sub docstring (time-order convention 'XZ = Z first'). The example instance encodes U = X*Z as gate list [z, x] (Z first) and V = Y; the returned miter is Z X Y = i*I, matching U = e^{-i pi/2} V. The state pair |+>,|-> part of eq_5 is not encoded (state checks out of scope).

## Specification changes

- eq_1, eq_3, eq_4: Qubit index convention: the specification treats qubit 0 as the most-significant basis-index bit; the implementation uses Qiskit's native little-endian ordering (qubit 0 least significant). Gate 'qubits' entries are physical Qiskit indices. Reason: Required by the Qiskit API; the identity/diagonality properties of the miter W are invariant under any fixed relabeling of basis indices, so the equivalence decisions are unaffected.
- eq_2, eq_4, eq_5: Scope narrowed to circuit equivalence only: the state-equivalence relations (eq_2 and the state part of eq_4, including the |+>,|-> pair of eq_5) are not implemented. Reason: The deliverable must be a measurement-free operation without input-state preparation; state checks are classical comparisons of amplitude vectors.
- eq_3, eq_4: The equivalence decision (|Tr(W)| = N, or W diagonal) is left to classical post-processing on the unitary of the returned miter circuit W; only W is constructed. Reason: Operation-only contract: no operator construction, simulation, or verification may be performed in the module.
