# Equation to Qiskit

One step of a lazy discrete-time quantum walk on a cyclic line with a 3-level DFT coin (left, stay, right), repeated t times. The coin is a two-qubit register with 3 of 4 levels used. The 3x3 DFT is built from standard gates through an analytic two-level (Givens) decomposition. The shift is a coin-controlled increment (right) or decrement (left) mod 2^n, and 'stay' is the identity. No state preparation or measurement is included.

Source equation run: `d9e90636-dfaa-4c79-aaf4-db0aa6ae77e5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register 'pos', unsigned integer, qubit 0 is the least significant bit; the walker position is x = value - offset (offset chosen by the runner), arithmetic mod 2^n
- qubit n: coin bit c0 (least significant coin bit)
- qubit n+1: coin bit c1 (most significant coin bit)
- coin code (c1 c0): 00 = left (c=-1, logical 0), 01 = stay (c=0, logical 1), 11 = right (c=+1, logical 2), 10 = unused (identity under the coin, shift acts trivially)
- example: n=4 gives 6 qubits, pos = qubits 0-3, coin = qubits 4-5

## Assumptions

- Lazy walk model is the 3-state-coin walk with a DFT coin, as in the spec's assumed eq_2.
- Coin applied first, then shift, each step.
- Each lattice position offset is applied by the runner; the circuit only adds integers mod 2^n.
- steps limited to 0..64 and position_qubits to 2..10, so total qubits are at most 12.

## Unresolved issues

- The exact lazy walk definition from the source paper (e.g. Childs' lazy walk) may differ from this 3-state-coin model.
- Definitions of occupancy number and occupancy rate were not provided.
- The initial coin state is not fixed by the source and must be chosen by the runner.
- The abstract does not specify the coin dimension. The 3x3 DFT is an assumption.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The n-th moment and its O(t^n) scaling are classical post-processing of the measured position histogram. The circuit has no measurement, so it is not implemented.
- `eq_2`: implemented; _shift and the loop in build_circuit. Each step applies the coin and then the conditional shift. The shift is a coin-controlled increment (right) or decrement (left) of the position register, and stay is the identity. The position register is cyclic.
- `eq_3`: implemented; _dft_coin. The 3x3 DFT C_jk = w^(jk)/sqrt(3) is built analytically from ch, cp, z and two controlled-Ry gates, as a product of two-level rotations. It acts as identity on the unused fourth coin level.
- `eq_4`: background; no code location. The Born-rule marginal over coin states is obtained by measuring the position register, which the runner does.
- `eq_5`: out_of_scope; no code location. The initial state (walker at the origin, coin chi) is prepared by the runner. The circuit is an operation only.

## Specification changes

- eq_2: The position register has a fixed instance-supplied size n and the shift is cyclic mod 2^n, not an unbounded line. Reason: A finite qubit register requires periodic boundaries. Wrap-around is avoided if the walker starts near the register centre and t < 2^(n-1).
- eq_2, eq_3: The 3-level coin is embedded in 2 qubits with the logical-to-physical code 0->00, 1->01, 2->11 and the unused code 10 acting as identity. The DFT index j=0,1,2 is identified with c=-1,0,+1. Reason: A 3-level system needs 2 qubits. The Gray-code ordering lets the two-level rotations be single controlled gates.
- eq_3: The DFT is synthesized from standard gates through an exact analytic decomposition, with no dense unitary matrix. Reason: Opaque unitaries are not allowed. The decomposition is DFT = R12(pi/4) R01(acos(1/sqrt3)) applied after (-S H on span{1,2}), where the -1 is a Z on c0.
- eq_5: State preparation is excluded. Reason: The task defines the output as an operation. The runner prepares the walker and the coin state.
- eq_1, eq_4: Scope is limited to the walk unitary t steps. Moments, occupancy number and occupancy rate are not computed. Reason: The occupancy definitions are missing, and moments are classical post-processing.
