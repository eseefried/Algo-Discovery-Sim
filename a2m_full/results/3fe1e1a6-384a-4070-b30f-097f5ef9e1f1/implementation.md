# Equation to Qiskit

Builds T steps of the coined discrete-time quantum walk U=S(I⊗C) on the cycle C_N with N=2^n_pos. The position register uses little-endian encoding and the coin is one qubit. Coin 0 increments the position mod N and coin 1 decrements it. Coin choices are hadamard, grover (2-dim Grover coin = X) and dft (2-dim DFT = H). The circuit contains no state preparation or measurement, so the runner prepares the initial state and reads out P(t) and the return amplitude.

Source equation run: `9a2bd00e-2576-49e1-8118-5fbf02d22a57`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pos bit 0 (least significant node-index bit)
- qubit 1: pos bit 1 (most significant bit for n_pos=2, node index x=q0+2*q1)
- qubit n_pos-1: most significant position bit for general n_pos
- qubit n_pos: coin qubit (0=forward/increment, 1=backward/decrement)
- Total qubits = n_pos+1 (example n_pos=2 gives 3 qubits: q0,q1 position, q2 coin)

## Assumptions

- N=2^n_pos, with the node index stored little-endian in the position qubits.
- Coin 0 moves forward (+1) and coin 1 moves backward (-1).
- The coin is applied before the shift in each step, so U=S(I⊗C).
- steps is limited to 1..64 and n_pos to 2..11, so the total is at most 12 qubits.
- Multi-controlled X gates are left to Qiskit's standard decomposition, with no ancillas.

## Unresolved issues

- The paper's modified graphs that give PST and their arc and coin conventions are not specified in the abstract and are not implemented.
- The flip-flop shift convention for higher-degree graphs is unresolved.
- Antipodal PST on the plain C4 with the Hadamard coin is not asserted here and must be checked by the runner's simulation.

## Equation mapping

- `eq_1`: implemented; _shift and _incrementer. Coin-controlled incrementer (coin=0, via X-conjugation of the coin) and decrementer (coin=1, reversed gate order) mod 2^n, built from CX and multi-controlled X gates.
- `eq_2`: implemented; build_circuit loop with _coin_op then _shift. Each step applies the coin to the coin qubit and then the shift, repeated 'steps' times to give U^t with no intermediate measurement.
- `eq_3`: out_of_scope; no code location. Initial-state preparation is done by the runner. The circuit is only the operation U^t.
- `eq_4`: out_of_scope; no code location. Antipodal probability P(t) is classical postprocessing of the output state. It is not part of the circuit.
- `eq_5`: out_of_scope; no code location. The periodicity test is a return-amplitude postprocessing check, not part of the circuit.

## Specification changes

- eq_1, eq_2: Scope narrowed to the plain cycle C_N with N=2^n_pos (n_pos in 2..11), using the moving shift. The modified graphs, flip-flop shift, interpolation, decoherence and continuous-time walk are not implemented. Reason: The abstract does not specify the modifications, and arbitrary even N would need non-power-of-two modular arithmetic. N=6 therefore cannot be built.
- eq_2: The Grover and DFT coins are realised as the 2-dimensional coins X and H on the single coin qubit. The coin is chosen by instance['coin']. Reason: On a degree-2 cycle the Grover coin 2|s><s|-I is X and the 2-point DFT is H, as the specification noted.
- eq_3, eq_4, eq_5: State preparation and readout are removed from the circuit. Reason: The task requires an operation only, with no input preparation or measurement.
