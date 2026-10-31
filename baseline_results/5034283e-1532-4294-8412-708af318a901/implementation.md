# Equation to Qiskit

Qiskit module implementing t steps of the coined discrete-time quantum walk U = S (I ⊗ C) on the cycle C_N for N a power of two (N = 2^n, 4 <= N <= 2048), with the degree-2 Grover coin C = X (or optionally the Hadamard coin) and the flip-flop (arc-reversing) shift. The position register (n qubits, binary node label) and a single coin qubit are laid out so that the basis index is 2v + c (position most significant, as in the specification). The circuit is the pure walk operator U^t: no state preparation or measurement. The default example is the baseline C4 instance with t = 2, for which the specification predicts perfect antipodal transfer 0 -> 2.

Source equation run: `b19fb3b5-3034-4ec6-9534-a9d8300ae632`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin register c (c=0 -> move toward v+1, c=1 -> move toward v-1 mod N)
- qubit 1: position bit v_0 (LSB of node label v)
- qubit 2: position bit v_1 (MSB of node label v for N=4)
- Basis index = 2*v + c, i.e. |v>|c> with position most significant as in the specification; node 0 = index 0 or 1, antipodal node 2 = index 4 or 5 (binary 10c)
- Total qubits for the example: 3 (general: log2(N) + 1, capped at 12)

## Assumptions

- Node-independent coin (valid for the regular cycle; the paper's modified cycles are not reconstructed).
- Flip-flop (arc-reversing) shift convention with c=0 meaning 'toward v+1' and c=1 meaning 'toward v-1'.
- Grover coin at degree 2 equals Pauli X; the Hadamard option is an extension not fixed by the specification.
- mcx gates are used in no-ancilla mode; circuit depth grows with log2(N) and steps but qubit count stays at log2(N)+1.
- For the example (C4, X coin, t=2) the specification predicts the walker starting at node 0 (any coin state) is found at node 2 with probability 1; this is a prediction, not a verified result.

## Unresolved issues

- Cycles with N not a power of two (C6 in the abstract) are not supported by the binary modular shift.
- The paper's actual graph modifications, the three coin operators, generalised families, continuous-time results, interpolation and decoherence studies remain unreconstructed and out of scope.
- Whether the paper's PST definition requires coin-state transfer or only vertex occupation is unknown; the runner's fidelity should trace out the coin qubit per eq_5.

## Equation mapping

- `eq_1`: implemented; build_circuit: QuantumRegister allocation (coin_reg, pos_reg) and module docstring layout comment. Position-coin Hilbert space realised as an n-qubit binary position register plus one coin qubit, ordered so the basis index is 2v + c (position most significant).
- `eq_2`: implemented; _apply_coin. Degree-2 Grover coin G_2 = X applied to the coin qubit; 'hadamard' offered as an optional alternative coin.
- `eq_3`: implemented; _flip_flop_shift, _controlled_increment. Flip-flop shift: coin-controlled modular increment (c=0) and decrement (c=1) of the position register, followed by X on the coin for arc reversal. Modular arithmetic is mod 2^n, hence N restricted to powers of two.
- `eq_4`: implemented; build_circuit: for-loop over steps applying _apply_coin then _flip_flop_shift. U = S (I ⊗ C) composed t times to give U^t; the circuit is the bare operator with no state preparation.
- `eq_5`: out_of_scope; no code location. The antipodal fidelity F(t) is a measurement/post-processing quantity to be estimated by the runner from position outcomes; the module returns only the unitary operator.
- `eq_6`: background; no code location. Predicted behaviour of the C4/X instance (PST at t=2, period 4). It is a consequence of the implemented operator, not an additional construction, and no verification is claimed here.

## Specification changes

- eq_3: Cycle size restricted to N = 2^n (4 <= N <= 2048, 12-qubit cap) instead of arbitrary even N. Reason: The shift is implemented as a binary modular increment/decrement with multi-controlled X cascades, which is exact only mod 2^n; general-N modular increments (e.g. C6) would need a different arithmetic construction and are excluded.
- eq_2: Added an optional 'hadamard' coin choice alongside the specified Grover (= X) coin; the example uses 'grover'. Reason: The abstract mentions three unnamed coins; Hadamard is the natural degree-2 alternative and costs nothing to expose, but it is an assumption beyond the specification.
- eq_1: Physical qubit ordering fixed as coin = qubit 0 (least significant), position bits = qubits 1..n. Reason: Qiskit qubit 0 is the LSB; this layout reproduces the specification's |v>|c> ordering with position most significant (basis index 2v + c).
- eq_4: Step count capped at 1024 and must be a non-negative integer; steps = 0 returns the identity circuit. Reason: Bounded resource usage and explicit instance validation required by the implementation contract.
- eq_5, eq_6: No initial state preparation or measurement is included; the predicted PST of eq_6 is not asserted by the code. Reason: The module must return only the operation; input preparation and fidelity estimation are the runner's responsibility.
