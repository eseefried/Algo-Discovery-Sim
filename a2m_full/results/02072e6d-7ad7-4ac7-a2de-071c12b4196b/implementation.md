# Equation to Qiskit

Builds T iterations of the coined quantum-walk search operator U = S C O on a twisted toroid with n = 2^(2m) nodes. The marked node is compiled in as a multi-controlled phase flip, the coin is the 2-qubit Grover coin, and the shift is a flip-flop shift built from controlled modular increments and decrements. Moving off the x-boundary also shifts y by the twist s. The circuit contains no state preparation or measurement. The runner must supply the uniform initial state.

Source equation run: `461b871e-51f4-4135-9bc4-400ffb7b0aac`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin bit 0 (LSB of direction c)
- qubit 1: coin bit 1 (c: 0=+x, 1=-x, 2=+y, 3=-y)
- qubits 2..m+1: x coordinate, little-endian (x bit 0 is qubit 2)
- qubits m+2..2m+1: y coordinate, little-endian
- marked index w = x + 2^m * y
- total qubits = 2m+2 (m=2 in the example gives 6 qubits)
- the runner prepares the initial state, e.g. Hadamards on all qubits for the uniform state

## Assumptions

- Marked node is given as the integer w = x + 2^m*y, and the phase flip applies to all coin values.
- Twist is y +/- s on x wraparound only. The sign follows the direction of travel, +s for +x and -s for -x.
- Flip-flop shift: the coin direction c is mapped to c XOR 1 after the move.
- Direction encoding is 00:+x, 01:-x, 10:+y, 11:-y, using coin bit 0 as the LSB.
- m is restricted to 1..4. The twist s must be less than 2^m.

## Unresolved issues

- The exact twisted-toroid graph definition from the paper is unknown, so the twist is a plausible guess.
- The paper's oracle and coin conventions are unknown.
- The optimal T is not determined here. The external runner has to scan for it.
- Gate-count scaling is not verified, and gate decompositions are not optimized.
- The other graph families in the abstract are not implemented.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Initial uniform superposition is input-state preparation. The runner prepares it, so build_circuit contains no Hadamard preparation layer.
- `eq_2`: implemented; build_circuit loop: marking block (X on zero bits of w, mcp(pi)) and Grover coin block (H,X,CZ,X,H plus global phase pi). O is I - 2 I_c (x) |w><w| as a multi-controlled phase of pi. C is exactly 2|s><s| - I on the 2 coin qubits, with the -1 recorded as global phase.
- `eq_3`: implemented; _shift, with _inc and _dec. Coin-conditioned modular increments and decrements of x and y. y moves by s when x wraps, detected before x is updated, and the sign follows the direction. The coin is then flipped with X on coin bit 0 (c XOR 1).
- `eq_4`: implemented; build_circuit loop over T iterations. The circuit implements U^T = (S C O)^T with U = S C O applied in the order O, C, S. T is supplied as instance['iterations']. The scan that maximizes P(T), and the readout, are not part of the circuit.
- `eq_5`: background; no code location. The O(sqrt(n) log n) gate-count claim is a target statement from the abstract. It is not implemented or verified here.

## Specification changes

- eq_1: The Hadamard state-preparation step is excluded from the circuit. Reason: The task requires an operation with no input-state preparation. The runner prepares the uniform state.
- eq_2, eq_3, eq_4: The ancilla register is dropped and the circuit uses 2m+2 qubits. Multi-controlled gates use Qiskit's ancilla-free MCX and MCP decompositions. Reason: No ancilla is needed. This also keeps the qubit count within the 12-qubit cap, with m <= 4 giving at most 10 qubits.
- eq_3: The twist offset s is an optional instance parameter (default 1, range 0..2^m-1). The y shift is applied s times as repeated unit increments or decrements. Reason: The spec leaves the twist size and direction as a guess. A parameter keeps the guess explicit and varyable.
- eq_4: The iteration count T is a required input (0..1000) and is not chosen inside the module. Selecting T by scanning P(T) is not implemented. Reason: Choosing T needs simulation, which is not allowed in the generated module.
- eq_2: The Grover coin is implemented with its exact sign, -(HH)(I-2|00><00|)(HH), by adding a global phase of pi. Reason: This preserves 2|s><s| - I exactly.
