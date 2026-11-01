# Equation to Qiskit

Coined discrete-time quantum walk step operator U=S(I⊗C) on the unmodified cycle C_N, N=2^n (default N=4), repeated t times. The coin is the Grover coin (equal to Pauli X on a degree-2 vertex), with an optional Hadamard coin. The shift moves +1 for coin 0 and -1 for coin 1, built from CX and multi-controlled X gates. No state preparation or measurement is included, and the fidelity and PST analysis is left to postprocessing.

Source equation run: `9d9fdc56-eb85-46fd-b1d2-339e92bc9cb0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register, little-endian binary node label v (v = sum_k 2^k q_k); n=2 gives q0,q1 for N=4
- qubit n: coin register (c=0 moves forward +1, c=1 moves backward -1); n=2 gives q2

## Assumptions

- Cycle is unmodified C_N with N a power of two
- Coin is applied before the shift, so U=S(I⊗C)
- Coin 0 moves +1 and coin 1 moves -1 mod N
- The runner prepares the initial state, nominally |0,0>

## Unresolved issues

- The paper's modified C4/C6/C8 graphs, the three coins and the generalised families are not specified, so they are not implemented
- No claim is made that this unmodified walk with the Grover coin exhibits PST
- The decoherence model and the continuous-time walk are not implemented

## Equation mapping

- `eq_1`: implemented; build_circuit (shift block with cx conjugation) and _increment. Coin then conditional shift on the cycle, with c=0 moving +1 and c=1 moving -1 mod N, built from CX and multi-controlled X gates.
- `eq_2`: implemented; build_circuit (coin block: qc.x(c) for 'grover'). The Grover coin on a 2-dimensional coin space equals Pauli X. A Hadamard option is added as an extra.
- `eq_3`: implemented; build_circuit (for _ in range(steps) loop). The circuit implements U^t. The initial state |0,0> is the default all-zero state and is prepared by the runner, not by the circuit.
- `eq_4`: out_of_scope; no code location. Antipodal fidelity is a measurement and postprocessing quantity, which the operation circuit excludes.
- `eq_5`: out_of_scope; no code location. The PST criterion is a classical postprocessing check over t and is not part of the circuit.

## Specification changes

- eq_1: Position register generalised to N=2^n nodes (n>=2), with N=4 as the default example. The graph is the unmodified cycle only. Reason: Binary position encoding needs a power-of-two N, and the abstract's graph modifications are unspecified.
- eq_2: Optional Hadamard coin added alongside the Grover coin. Reason: Provides one more simple coin choice, since the abstract's three coins are not named.
- eq_3, eq_4, eq_5: Initial state preparation, fidelity measurement and PST criterion excluded from the circuit. Reason: The task requires an operation without state preparation or measurement.
- eq_1: Shift implemented as CX conjugation, an unconditional increment, then CX again, in place of separate controlled increment and decrement. Reason: Same unitary because ~(~v+1)=v-1, using fewer gates.
