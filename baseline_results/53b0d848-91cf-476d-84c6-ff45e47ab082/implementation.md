# Equation to Qiskit

Implements the single-ancilla Stinespring dilation circuit U_k (eq_3) for one generalized extreme qubit channel (d = 2, Kraus rank <= 2, eq_2) in the Ruskai-Szarek-Werner canonical form K_0 = diag(cos v0, cos v1), K_1 = sin v1 |0><1| + sin v0 |1><0|, which contains amplitude damping (v0 = 0, sin^2 v1 = gamma) and, as a separate 'unitary' channel type, the Pauli channels such as X.X of the tiny instance eq_6. The circuit is Ry(2 v0) on the ancilla, a controlled-Ry(2(v1 - v0)) from system to ancilla, and a CNOT from ancilla back to system; the ancilla starts in |0> and is to be traced out by the runner. The classical decomposition (eq_1), classical random selection of k (eq_4) and fault-tolerant gate compilation (eq_5) are not part of the returned unitary operation.

Source equation run: `30ebe829-eaae-4f22-adb9-d3016a76a688`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 (register s[0]): system qudit S (d = 2); carries the channel input rho and, after tracing out qubit 1, the output E_k(rho)
- qubit 1 (register a[0]): single ancillary qubit A for the Stinespring dilation; must be supplied in |0> by the runner and discarded (traced out) after the circuit; ancilla value |i> labels Kraus index i
- Total qubits: 2. Qiskit little-endian: qubit 0 is the least significant bit, so the combined basis label is |a s> (ancilla bit high, system bit low); the specification's 'S tensor A' ordering corresponds to reading the bitstring reversed.
- Example instance (amplitude damping gamma = 1/2 = U_1 of eq_6): circuit = CRY(pi/2) controlled by s[0] on a[0], then CX(a[0] -> s[0]). The k = 2 term of eq_6 is obtained with {"d": 2, "channel": {"type": "unitary", "pauli": "X"}}.

## Assumptions

- The runner supplies the ancilla qubit 1 in |0> and traces it out (or measures and discards it) after the circuit; the system input state is on qubit 0.
- 'Generalized extreme channel' is interpreted as a channel of Kraus rank at most d, so one ancilla qubit suffices for d = 2.
- Ry(theta)|0> = cos(theta/2)|0> + sin(theta/2)|1>, hence the factor 2 in the rotation angles.
- Angles v0, v1 may be any finite reals (the Kraus form is trace preserving for all of them); gamma must lie in [0, 1].

## Unresolved issues

- The paper's specific nonlinear algebraic equations for the convex decomposition and the parametrisation of generalized extreme qudit channels for d > 2 are unknown, so only the qubit case is implemented.
- The explicit O(d^2)-gate construction of the dilation unitary claimed in the abstract is not reproduced; for d = 2 the three-gate circuit is exact but its relation to the paper's construction cannot be confirmed.

## Equation mapping

- `eq_1`: background; no code location. The classical convex decomposition of E into extreme channels with weights p_k is classical preprocessing whose equations are unavailable; the module takes one already-decomposed extreme channel E_k as input.
- `eq_2`: implemented; _channel_angles (docstring and comments) and the canonical Kraus form in the module docstring. The rank-<=2 Kraus form is realised through the canonical parametrisation K_0 = diag(cos v0, cos v1), K_1 = sin v1 |0><1| + sin v0 |1><0| (plus rank-1 Pauli unitary channels); the trace-preservation condition holds identically for all real v0, v1.
- `eq_3`: implemented; build_circuit: comments 'eq_3: isometry ...', gates qc.ry, qc.cry(s -> a), qc.cx(a -> s). The dilation unitary U_k acting on S tensor A with ancilla in |0> is built from a system-controlled ancilla rotation followed by an ancilla-controlled flip of the system, reproducing sum_i (K_i|psi>)_S |i>_A.
- `eq_4`: out_of_scope; no code location. Random sampling of k with probability p_k into classical dits and the resulting diamond-norm error budget are classical/statistical procedures; the returned object is the unitary circuit for a single chosen k.
- `eq_5`: out_of_scope; no code location. Fault-tolerant Solovay-Kitaev compilation of U_k to a finite gate set with O(d^2 log^c(1/eps)) cost is a transpilation step not performed in this module; the circuit uses exact continuous-angle gates.
- `eq_6`: implemented; _channel_angles branch 'amplitude_damping' (U_1: v0 = 0, v1 = arcsin(sqrt(gamma))) and build_circuit branch 'angles is None' (U_2 = X_S tensor 1_A); example_instance_json uses gamma = 0.5. Both extreme-channel circuits U_1 and U_2 of the tiny d = 2 instance are constructible; the example instance is U_1 with gamma = 1/2. The mixture weights 3/4, 1/4 belong to the classical sampling (eq_4) and are not encoded in the unitary.

## Specification changes

- eq_2, eq_3: Scope narrowed to qubit channels (d = 2 only); the generic qudit dilation for arbitrary d is rejected with ValueError. Reason: For general d the dilation would require synthesising an arbitrary d^2 x d^2 isometry (an opaque dense unitary), and the paper's explicit O(d^2) gate construction is not recoverable from the abstract.
- eq_2: Generalized extreme qubit channels are parametrised by the canonical form K_0 = diag(cos v0, cos v1), K_1 = sin v1 |0><1| + sin v0 |1><0| (two real angles), plus separate rank-1 Pauli unitary channels; arbitrary pre/post local unitaries are not included. Reason: This is the standard canonical form of extreme qubit channels up to local unitaries; it is sufficient to express both terms of the tiny instance eq_6 while keeping the construction a transparent gate sequence.
- eq_4, eq_6: The classical random choice of k (and the weights 3/4, 1/4) is moved outside the circuit: the instance selects a single k and the module returns only U_k. Reason: The output must be a measurement-free, deterministic unitary operation without classical registers or randomness.
- eq_3: Register ordering: the specification writes S tensor A (system first); in the Qiskit circuit the system is qubit 0 (least significant) and the ancilla is qubit 1, so basis labels read |a s>. Reason: Qiskit little-endian convention; the ancilla is traced out so only the physical assignment of S to qubit 0 matters, which is stated explicitly in the layout.
- eq_5: No fault-tolerant compilation is performed; exact Ry/CRY/CX gates are emitted. Reason: Gate-set compilation is a downstream transpiler concern and its parameters (gate set, exponent) are not specified.
