# Equation to Qiskit

Grover-baseline iteration operator with systematic phase errors: k applications of G_delta = -R_{pi+delta}(|s>) R_{pi+delta}(|w>) on an n-qubit register (n<=12), where R_phi(|a>) = I + (e^{i phi}-1)|a><a|. It is built from X, H, P and multi-controlled phase gates. No state preparation or measurement is included. This is the assumed Grover baseline, not the paper's optimized quantum random-walk search operator.

Source equation run: `8e49f898-0f4a-4bbb-8b6e-2ce0391ab2b8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form the 'search' register; qubit 0 is the least significant bit of the database index.
- Marked integer m is encoded with bit i of m on qubit i (example: m=3 is |11> on qubits 1,0).
- No ancilla qubits; the runner prepares the input state (e.g. the uniform superposition H^n|0>).

## Assumptions

- The same systematic error delta applies to both phase inversions.
- Exactly one marked item, whose bits are encoded little-endian on the register.
- The runner prepares the uniform superposition (or any other input) before the circuit.
- The global phase -1 per iteration is recorded as circuit global_phase.

## Unresolved issues

- The paper's optimized quantum random-walk search operator, graph and coin are not specified, so they are not implemented.
- The paper's exact phase-error model and closed-form results are unknown; the model implemented here is an assumption.
- The robustness comparison with Grover's algorithm is not realized by this single circuit.

## Equation mapping

- `eq_1`: background; no code location. Geometric picture of the initial state. The uniform state |s> is prepared by the runner, and the circuit contains no state preparation. It is used only as the reflection axis inside R_s.
- `eq_2`: out_of_scope; no code location. Malformed draft explicitly marked as superseded; not implemented. The corrected content is in eq_4 and eq_5.
- `eq_3`: out_of_scope; no code location. Draft explicitly marked 'not used'; not implemented.
- `eq_4`: implemented; _phase_about_basis (called for |w> and, between Hadamard layers, for |0..0>). R_phi(|a>) = I + (e^{i phi}-1)|a><a|, phi = pi+delta, implemented with X conjugation and a multi-controlled phase gate (a single P gate for n=1). R_s is obtained by conjugating the |0..0> version with H^n.
- `eq_5`: implemented; build_circuit loop body. The iteration operator G_delta = -R(|s>) R(|w>) is repeated k times, with R_w applied first and the minus sign as a global phase of pi per iteration. P_k(delta) = |<w|G^k|s>|^2 is not computed in the circuit; it is a classical post-processing quantity.

## Specification changes

- eq_2, eq_3: Excluded from the implementation as discarded or malformed drafts. Reason: The specification itself says they are superseded or unused, and their LaTeX is incomplete.
- eq_4, eq_5: Generalized from N=4 with marked |11> to n qubits (1..12) with an arbitrary marked integer, iteration count and delta, all given in the instance. Reason: The task requires the operation to work for varying valid parameters. The N=4 case is the example instance.
- eq_5: Only the iteration operator G_delta^k is implemented. State preparation, measurement and the success probability P_k(delta) are omitted. Reason: The circuit must be an operation with no input preparation or measurement.
- eq_4, eq_5: Scope narrowed to the Grover baseline with an assumed phase-error model, not the paper's optimized quantum random-walk search. Reason: The random-walk operator and the paper's exact error model are not specified.
