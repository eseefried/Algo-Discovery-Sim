# Equation to Qiskit

Coined discrete-time quantum walk step U = S (I (x) C) repeated t times on a plain cycle C_N with N = 2^n nodes (C4, C8, C16). The walker has a 2-dimensional coin qubit and n node qubits. The shift is built from multi-controlled X gates: increment mod N on coin 0, decrement mod N on coin 1. The coin is selectable as Hadamard, Grover (X for degree 2) or a Y-rotation. The module builds only the walk operation, with no state preparation or measurement.

Source equation run: `ed0f13c3-c880-4fae-87e6-79b8bd9373a3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin qubit (|0> = move +1, |1> = move -1 around the cycle)
- qubits 1..n: node register, little-endian binary encoding of node x in 0..2^n-1 (qubit 1 is the least significant bit)
- Total qubits = node_qubits + 1 (example: 4 qubits, cycle C8)

## Assumptions

- Coin dimension is 2 (degree-2 cycle) and is encoded in one qubit.
- Node labelling is binary x with neighbours x±1 mod 2^n; the antipodal node of x is x + 2^(n-1).
- The number of steps is capped at 256 and the node qubits at 11, so there are at most 12 qubits in total.
- The runner prepares the initial state |a>|c0>.

## Unresolved issues

- Exact cycle modifications, graph families and the three coins are unknown.
- The decoherence model and the continuous-time walk are not implemented.
- C6 is not representable as a plain power-of-two cycle here.
- Antipodal PST for the plain cycle depends on the coin and initial state and is not asserted.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop over steps calling _apply_coin (C) then _apply_shift (S). One walk step U = S (I (x) C), with the coin acting on the coin qubit and the shift implemented as coin-controlled increment/decrement of the node register.
- `eq_2`: out_of_scope; no code location. The fidelity F(t) is a measurement and post-processing quantity, so it is not part of the operation circuit. Software computes it after the circuit is built.

## Specification changes

- eq_1: Narrowed to the plain unmodified cycle C_N with N = 2^n (C4, C8, C16). C6 and the modified cycles/graph families are not implemented. Reason: The abstract does not specify the modifications, and a non-power-of-two node count does not map cleanly onto a qubit register without extra choices.
- eq_1: The three coins are replaced by a selectable set: Hadamard, Grover (equal to X for degree 2) and a Y-rotation with angle theta. Reason: The abstract does not name the three coin operators.
- eq_1: The shift is the standard moving shift on the cycle (coin 0 increments the node, coin 1 decrements it). The operator order is coin first, then shift. Reason: The shift convention is not given and is assumed.
- eq_2: The fidelity computation and the PST scan are excluded from the circuit. Reason: The task requires a measurement-free operation and the runner prepares the inputs.
