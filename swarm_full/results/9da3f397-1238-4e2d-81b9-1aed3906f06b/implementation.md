# Equation to Qiskit

Builds t steps of a 1D lazy discrete-time quantum walk on a cyclic position register. The coin is 4-dimensional (2 qubits) with a DFT or Hadamard-tensor coin. Coin values 0, 1, 2, 3 map to left, stay, right, stay. The conditional shift is a QFT-basis phase adder, and no dense unitaries are used. Only the unitary walk operation is implemented. Moment scaling, occupancy measures and concentration intervals are classical post-processing and are not implemented.

Source equation run: `a6c6f469-071a-450e-8c71-aa0740d7fb9e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin bit 0 (LSB of coin value c)
- qubit 1: coin bit 1 (MSB of coin value c)
- qubits 2..(n+1): position register, little-endian, cyclic mod 2^n; qubit 2 is the LSB
- coin value 0 = move left (-1), 1 = stay, 2 = move right (+1), 3 = stay

## Assumptions

- Coin value 0 shifts the position by -1, value 2 by +1, and values 1 and 3 leave it unchanged.
- The runner prepares the initial state (e.g. position 0 and a fixed coin state).
- Position register size n is between 2 and 10, so the total is at most 12 qubits.
- In the QFTGate convention, adding s to the position equals a phase exp(2*pi*i*s*2^m/2^n) on Fourier qubit m, applied before QFTGate inverse.

## Unresolved issues

- Exact lazy-walk operator and laziness parameter of the source paper are unknown.
- Definitions of occupancy number and rate are unavailable.
- The paper's initial coin state and DFT coin dimension are unknown.
- Negative positions appear as wrapped high indices in the cyclic register.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The n-th moment and its O(t^n) scaling are classical post-processing of the measured distribution P(x,t). The circuit has no measurement and does not compute moments.
- `eq_2`: background; no code location. Normalization follows from the circuit being unitary (coin gates, QFTGate, phase gates only). It is not coded separately.

## Specification changes

- eq_1, eq_2: Scope narrowed to the unitary lazy-walk operator for a finite cyclic position register. No moments, occupancy number or occupancy rate are computed. Reason: The abstract gives only qualitative claims, and the occupancy definitions are missing.
- eq_1: The lazy walk is realised as a 4-dimensional coin (2 qubits) with the directions left, stay, right, stay. The coin is either the 4-point DFT (QFTGate(2)) or H tensor H. Childs' exact lazy-walk operator is not used. Reason: The exact operator and laziness parameter are not given. A 3-direction coin cannot be a DFT on whole qubits, so a duplicated stay direction is used.
- eq_2: The position shift is implemented mod 2^n with QFT-basis phases. The step count is required to satisfy 2t+1 <= 2^n so the walk does not wrap around the register. Reason: Without this, a cyclic register would alias positions.
