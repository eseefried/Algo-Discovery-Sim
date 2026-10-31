# Equation to Qiskit

Implements the unitary block U_delta^tau of the Tulsi-like controlled-rotation coined-walk search (eq_2, applied tau times as the inter-measurement evolution of eq_3) on a 2^(p/2) x 2^(p/2) periodic grid with a 2-qubit four-direction coin and one control qubit. Each step applies (i) a rotation R_delta = RY(2*delta) on the control conditioned on the position register being equal to the marked vertex w, (ii) the 4-dimensional Grover diffusion coin, and (iii) the flip-flop shift realised as coin-controlled QFT-based modular +-1 adders on the column and row coordinates followed by a sign-bit flip. Initial-state preparation (eq_1), the projective control measurement (channel part of eq_3), success probability, mutual information and order estimation (eq_4-eq_6) are left to the runner / classical post-processing.

Source equation run: `a354b527-3827-4677-802f-9a40fa93a243`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1 (pos[0], pos[1]): column coordinate x_2 of the 4x4 periodic grid, qubit 0 least significant
- qubits 2-3 (pos[2], pos[3]): row coordinate x_1; vertex index x = 4*x_1 + x_2, marked vertex w = 5 -> (x_1, x_2) = (1, 1)
- qubit 4 (coin[0]): direction sign bit, 0 = +1 step, 1 = -1 step (flipped by the flip-flop shift)
- qubit 5 (coin[1]): direction axis bit, 0 = column/x axis, 1 = row/y axis
- qubit 6 (ctrl[0]): Tulsi control qubit, rotated by RY(2*delta) when the walker is at w; it is the most significant qubit
- total 7 qubits for the example (p + 3 in general, p even, p + 3 <= 12)

## Assumptions

- The Tulsi-like step of eq_2 (control rotation conditioned on the marked vertex, then Grover coin, then flip-flop shift) is accepted as the schematic step; Tulsi's original control-conditioned coin is not reproduced, as stated in the specification.
- delta is a free real parameter supplied in the instance (example uses pi/4).
- Measurement outcomes of the control are not fed back; the runner applies the non-post-selected control measurement between blocks of tau steps.
- Position encoding x = x_1 * 2^k + x_2 with qubit 0 the least significant bit of the column coordinate.
- Multi-controlled RY and doubly-controlled phase gates are produced via standard-gate .control(), not dense unitaries.

## Unresolved issues

- Exact form of Tulsi's operator and the paper's specific choice of delta remain unknown; the implemented step is a placeholder consistent with the specification's assumption.
- The flip-flop shift uses QFTGate-based adders with 2-controlled phases per coordinate qubit, which is deep for p = 8 and large tau; no depth optimisation was attempted.

## Equation mapping

- `eq_1`: background; no code location. Initial state |0>_C (x) |c_u> (x) |s> is an input state prepared by the runner; the module returns only the operation.
- `eq_2`: implemented; _tulsi_step (with _controlled_marked_rotation for the |w>-conditioned R_delta = RY(2*delta), _grover_coin for C, _flip_flop_shift / _controlled_coordinate_shift for S). One step U_delta: controlled rotation of the control at the marked vertex, Grover coin on 2 coin qubits (exact sign fixed via global_phase), QFT-based coin-controlled modular +-1 shifts on both coordinates plus sign-bit flip.
- `eq_3`: implemented; build_circuit: for-loop applying _tulsi_step tau times. Only the unitary inter-measurement block U_delta^tau is built; the projective control-measurement channel M is non-unitary and must be applied by the runner between successive circuits.
- `eq_4`: out_of_scope; no code location. Success probability requires a final position measurement / state analysis, which is excluded from the operation.
- `eq_5`: out_of_scope; no code location. Mutual information is a classical post-processing quantity computed from the (mixed) state, not part of the circuit.
- `eq_6`: out_of_scope; no code location. Order estimation is a classical fit over several N and is not a circuit operation.

## Specification changes

- eq_3: Scope narrowed to the unitary segment U_delta^tau between control measurements; the dephasing/projective measurement channel M on the control is not included in the circuit. Reason: The deliverable must be a measurement-free, unitary QuantumCircuit; the runner can apply the measurement between consecutive applications of this block.
- eq_2: Fixed concrete conventions: coin basis coin[1] = axis, coin[0] = sign; position register split into column (low k qubits) and row (high k qubits) coordinates with n = 2^(p/2); R_delta realised as RY(2*delta); Grover coin realised with an explicit global phase pi to match 2|c_u><c_u| - I exactly (not only up to phase). Reason: The specification left the coin-direction encoding and gate decomposition unspecified; these choices are needed to produce a concrete circuit and were made consistent with the spec's register description.
- eq_2: Grid side length restricted to powers of two (num_position_qubits even), so N = 4^(p/2) in {4, 16, 64, 256}; the spec's N = 16 example corresponds to p = 4. Reason: Binary position encoding with QFT-based modular adders requires n = 2^k; the 12-qubit cap limits p <= 8.
