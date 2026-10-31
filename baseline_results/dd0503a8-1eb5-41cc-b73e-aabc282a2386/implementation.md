# Equation to Qiskit

Implements the erroneous search iteration of eq_2, G_{phi,psi} = -I_s^{psi} I_t^{phi}, applied k times on an n-qubit data register (N = 2^n, single marked item t). The marked-state phase inversion I_t^{phi} = I - (1-e^{i phi})|t><t| is realized by X gates on the qubits where t has bit 0, a multi-controlled phase gate with angle phi = pi + delta1 on all data qubits, and the X gates undone. The mean-state inversion I_s^{psi} = I - (1-e^{i psi})|s><s| is realized as H^{(x)n} X^{(x)n} MCP(psi) X^{(x)n} H^{(x)n} with psi = pi + delta2. The overall sign -1 of each iteration is recorded as a global phase of pi. The input state (uniform superposition |s>, eq_1) is prepared by the runner, and the success rate (eq_3) is obtained by the runner's measurement of the data register. The example instance is the N=4, k=1, matched-error case of eq_6.

Source equation run: `58b11b66-beb4-49d5-8502-a332d6d9ccc4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- data register: qubits 0..n-1 (n = n_qubits = 2 in the example), N = 2^n = 4 database items
- qubit i encodes bit i of the item index x (Qiskit little-endian: qubit 0 = least significant bit)
- marked item t = 3 = |11> in the example; the oracle phase e^{i(pi+delta1)} is applied to this basis state
- no coin register and no ancilla; the runner prepares |s> = H^(x)n |0...0> on the data register and measures it after the circuit

## Assumptions

- Phase errors are systematic: the same delta1, delta2 are used in every iteration.
- The marked item index is encoded little-endian on the data register (qubit 0 = least significant bit of t).
- The runner prepares the uniform superposition |s> on the data register before applying the circuit and measures the data register afterwards.
- mcp (multi-controlled phase) and p are standard Qiskit gates; the decomposition into basis gates is left to the transpiler.

## Unresolved issues

- The actual optimized quantum random-walk search algorithm (graph, coin, shift, optimization) is unknown from the abstract; the implemented operation is the geometric two-inversion model only.
- Whether the paper's phase error enters one or both inversions (matched or unmatched) is unknown; both deltas are exposed as parameters.
- The paper's own success-rate and iteration-count formulas and its robustness comparison with Grover's algorithm are not reproduced.

## Equation mapping

- `eq_1`: background; no code location. Initial uniform superposition |s> and the two-dimensional decomposition; the input state is prepared by the runner (no state preparation is allowed in the returned operation). The decomposition itself is analytic background.
- `eq_2`: implemented; build_circuit (loop body), _marked_inversion, _mean_inversion, _phase_on_all_ones. I_t^{phi} is realized as X-conjugated multi-controlled phase with angle phi = pi + delta1 on the marked basis state; I_s^{psi} as H^n X^n MCP(psi) X^n H^n with psi = pi + delta2; the product with sign -1 (global_phase += pi) is repeated k times.
- `eq_3`: background; no code location. Success rate |<t|G^k|s>|^2 is a measurement statistic computed by the runner from the data register; measurements are excluded from the operation.
- `eq_4`: background; no code location. Effective rotation angle for matched errors is an analytic consequence of the implemented operator; no code is needed.
- `eq_5`: background; no code location. Closed-form success probability for matched errors; a prediction to be compared with runner results, not part of the circuit.
- `eq_6`: background; no code location. Predicted P_1(4, delta) for the tiny instance; the example_instance_json (n_qubits=2, marked=3, iterations=1, delta1=delta2) realizes exactly this instance, but the formula itself is a validation target, not an operation.

## Specification changes

- eq_1: State preparation (Hadamards producing |s>) is omitted from the returned circuit. Reason: The task requires an operation only; the runner prepares the input state.
- eq_2: The mean-state inversion I - (1-e^{i psi})|s><s| is implemented as H^n (X^n MCP(psi) X^n) H^n, which is exactly equal for N = 2^n; the overall factor -1 of G_{phi,psi} is recorded as a circuit global phase of pi per iteration rather than as a gate. Reason: Standard exact decomposition using allowed standard gates; the global phase is physically irrelevant but kept so the circuit unitary equals eq_2 exactly.
- eq_2, eq_3: Scope narrowed to the generic two-phase-inversion (Grover-type) iteration in the two-dimensional model; the coin/shift structure of the optimized quantum random-walk search algorithm is not implemented and no coin register is allocated. Reason: The abstract gives no definition of the random-walk algorithm's operators; only the geometric two-inversion model was reconstructed.
- eq_2: Database size restricted to N = 2^n with 1 <= n <= 12 and exactly one marked item. Reason: Qubit cap of 12 and the single-marked-item assumption of the specification.
