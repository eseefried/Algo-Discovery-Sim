# Equation to Qiskit

Builds t steps of a lazy discrete-time quantum walk on a cycle of N=2^n sites. Each step applies a 3x3 DFT coin embedded in a 2-qubit coin register (state |3> idle), then the conditional shift. The coin is compiled by a Givens (two-level) decomposition into controlled-U gates and phases, with no dense unitary. The shift is built from multi-controlled X ripple increment/decrement. The circuit has no state preparation or measurement. Moments, occupancy and comparison walks are classical post-processing and are not implemented.

Source equation run: `b86db6bd-fb01-4784-9682-519858c2084f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register 'pos', little-endian integer x in [0, 2^n) (cycle, x+1 mod N)
- qubit n: coin bit c0 (least significant coin bit)
- qubit n+1: coin bit c1 (most significant coin bit)
- coin value 2*c1+c0: 0=|L> (shift -1), 1=|S> (stay), 2=|R> (shift +1), 3=idle (identity, never populated if input has no weight there)
- Example n=4: pos = qubits 0-3, coin = qubits 4-5, 6 qubits total

## Assumptions

- Coin encoding |L>=|00>, |S>=|01>, |R>=|10>, |idle>=|11> in (c1 c0)
- Coin acts as identity on the idle state and the shift is identity there
- Position register is little-endian with wraparound mod 2^n via ripple MCX increment/decrement
- Coin sign convention exp(+2*pi*i*jk/3) by default
- Controlled phases implement the diagonal exactly, including the global phase of the coin (global phase is irrelevant to the walk anyway)

## Unresolved issues

- The paper's exact lazy-walk definition (3-state coin vs laziness parameter) is not confirmed
- The paper's occupancy number/rate definition and threshold are unknown
- Symmetry of the DFT-coin distribution with the chosen initial state is not guaranteed and must be checked numerically by post-processing
- MCX gates with up to n+1 controls are used without ancillas, so transpiled depth grows with n and t

## Equation mapping

- `eq_1`: implemented; _shift (called each step in build_circuit). Conditional shift: multi-controlled-X ripple increment when coin=|10> (R), decrement when coin=|00> (L), identity for |01> (S) and |11> (idle). The coin is applied before it in each step, giving U = S (C x I).
- `eq_2`: implemented; _dft3, _givens, _coin. F_3 is computed as plain complex numbers and compiled by Givens elimination into two-level rotations (controlled UGate plus phases) and a diagonal of controlled phases on coin states 0..2. State |3> is left as identity. The sign of the exponent is selectable via coin_sign.
- `eq_3`: implemented; build_circuit loop over steps. The circuit implements U^t. The initial state (|L>+i|R>)/sqrt2 (x) |0> must be prepared by the runner, and the marginal P(x,t) is computed from the output statevector, so neither is part of the circuit.
- `eq_4`: out_of_scope; no code location. Moment computation and the O(t^k) slope fit are classical post-processing on P(x,t).
- `eq_5`: out_of_scope; no code location. Occupancy number/rate (with an assumed threshold) and the comparison with Hadamard, classical and lazy classical walks are classical post-processing and are not circuit operations.

## Specification changes

- eq_3: Removed the initial-state preparation (H and S on the coin MSB) from the circuit. Reason: The task requires an operation without input-state preparation. The runner prepares the input, e.g. coin=(|00>+i|10>)/sqrt2 and pos=|0>.
- eq_2: Resolved the open question of the F_3 decomposition by an exact Givens (two-level) decomposition into controlled U gates and controlled phases. The sign convention is exposed as the parameter coin_sign (+1 matches the spec). Reason: Opaque dense unitaries are not allowed and F_3 is not a library gate. The decomposition is exact up to numerical precision.
- eq_1, eq_3, eq_4: Generalised from the fixed n=4, t<=5 instance to n in [2,10] and steps in [0,64]. The constraint 2t+1<N is not enforced, so wraparound is allowed. Reason: The operation is a valid unitary on any cycle. The no-wraparound condition only matters for the classical moment and occupancy analysis.
- eq_4, eq_5: Narrowed scope to the walk operation only; moments, occupancy number/rate, interval and comparison walks are excluded. Reason: They are classical post-processing, and the occupancy definition and threshold are guessed in the specification.
