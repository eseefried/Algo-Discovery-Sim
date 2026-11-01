# Equation to Qiskit

Coined discrete-time quantum walk on a cycle of N=2^n sites, built as U_T...U_1 with U_t = S (C_t x I). The coin is one qubit with a per-step U(theta,phi,lam) gate. The shift S is a coin-controlled increment (coin 0) or decrement (coin 1) mod N, made from multi-controlled X gates. The scope is only the generic walk operation, with no state encoding and no paper-specific transfer protocol.

Source equation run: `8ab17e1e-03fc-4766-9741-aa33c71834c8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin (computational basis |0>,|1>; coin 0 shifts +1, coin 1 shifts -1)
- qubits 1..n: position register pos[0..n-1], little-endian integer x (qubit 1 is least significant bit), N=2^n sites
- example: n=2 gives 3 qubits (q0 coin, q1-q2 position, N=4 cycle)

## Assumptions

- 1D cycle with a single coin qubit.
- Coin applied before the shift in each step, as in eq_1.
- Increment applies for coin |0> and decrement for coin |1>.
- Position labels use little-endian integer encoding.

## Unresolved issues

- Coin settings that give perfect two-qubit state transfer are unknown.
- The encoding of the two-qubit state into walk degrees of freedom is unspecified.
- The network geometry, the multi-qubit entanglement distribution and the routing protocol are not reconstructed.

## Equation mapping

- `eq_1`: implemented; build_circuit (loop over steps: coin gate then _shift). Per-step coin C_t as a U(theta,phi,lam) gate on the coin qubit, followed by the shift S; steps are composed in order U_1 first to U_T last.
- `eq_2`: implemented; _shift. Coin-conditioned increment/decrement mod 2^n, built from multi-controlled X gates with ctrl_state; coin |0> gives x+1 and coin |1> gives x-1.
- `eq_3`: out_of_scope; no code location. The transfer condition is a property to be checked and depends on an unspecified encoding and coin sequence. The circuit does no state encoding.
- `eq_4`: out_of_scope; no code location. Fidelity is an analysis quantity, not part of the unitary operation.

## Specification changes

- eq_2: Generalized the cycle length from the assumed N=4 to N=2^n for 1<=n<=11, with the default example at n=2. Reason: A power-of-two cycle maps directly onto qubit registers, and one parametrized builder covers the N=4 case.
- eq_1: Coin C_t is parametrized as a general single-qubit unitary u(theta,phi,lam) supplied through the instance. Reason: The abstract does not give the paper's coin settings, so they are left as inputs.
- eq_3, eq_4: Scope narrowed to the walk operator only. There is no two-qubit state encoding, no perfect-transfer protocol, no multi-qubit entanglement distribution, no routing, and no multi-dimensional network. Reason: The abstract gives no coin sequence, encoding or geometry, so these cannot be reconstructed. The task also requires an operation rather than an experiment.
