# Equation to Qiskit

Operation-only Qiskit circuit for T steps of the lackadaisical phase-flip-coin walk on K_4 with one self-loop per vertex (l=1, 4 qubits). Each step applies the coin C' (-I on the marked vertex, 2|s><s|-I on the other vertices, with s the uniform coin state) and then the relative-XOR flip-flop shift S. Instance parameters are the step count T and the marked vertex w. The runner prepares the initial state and measures.

Source equation run: `7f3587c5-9471-4d7a-8d0d-d2d191fd2b32`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pos bit 0 (least significant bit of vertex v)
- qubit 1: pos bit 1 (most significant bit of vertex v)
- qubit 2: coin bit 0 (least significant bit of arc label c)
- qubit 3: coin bit 1 (most significant bit of arc label c)
- coin encoding: c=0,1,2 are the neighbours v xor 1, v xor 2, v xor 3; c=3 is the self-loop
- computational basis, little-endian; the runner prepares the state (the spec's initial state is H on all 4 qubits) and measures pos

## Assumptions

- N=4, l=1, so the coin dimension is 4 and the coin state is uniform
- Marked vertex w is an instance parameter, defaulting to 0
- The runner prepares the uniform superposition over all 16 arcs
- Qubits 0,1 hold pos and qubits 2,3 hold coin, little-endian

## Unresolved issues

- The exact arc encoding and shift used in the original paper are not known
- The optimal T is not determined here
- General l, the SKW coin, multiple marked vertices and the continuous-time walk are not implemented
- For N=4 the success probability of 1 is not guaranteed by the abstract, which makes its claim for general N

## Equation mapping

- `eq_1`: implemented; _coin (H on both coin qubits conjugating the phase flip on coin==00). For N=4, l=1 the weighted coin state is uniform, so |s_c> = H^2|00> and the reflection is built from Hadamards. General l is not implemented.
- `eq_2`: implemented; _coin. Unmarked vertices get 2|s><s|-I = -D and the marked vertex gets -I. The circuit applies the coin-00 phase flip to all vertices, undoes it for pos==w with a multi-controlled phase, and adds a global phase of pi.
- `eq_3`: implemented; _shift. The flip-flop shift uses the relative-XOR encoding, with multi-controlled X gates on the pos qubits controlled by the coin value. The loop state c=3 is fixed.
- `eq_4`: implemented; build_circuit loop (S C')^T. Only the unitary (S C')^T is built. The uniform initial state and the position readout are left to the runner.
- `eq_5`: out_of_scope; no code location. This is a target claim about success probabilities, to be checked by external simulation. It is not part of the circuit.

## Specification changes

- eq_4: The initial-state preparation (H on all qubits) and the measurement are removed from the circuit. Only (S C')^T is built. Reason: The task requires an operation without state preparation or measurement.
- eq_1, eq_2, eq_3, eq_4: Scope narrowed to N=4, l=1, phase-flip coin. The marked vertex w is a validated parameter in 0..3, and steps T is a parameter. Other N and l are rejected with ValueError. Reason: The spec scopes the construction to N=4, l=1. General l needs non-power-of-two coin padding.
- eq_2: The coin is implemented as a controlled reflection (phase flip on coin==00 conjugated by H^2) plus a global phase of pi. This is exactly -I on marked and 2|s><s|-I on unmarked vertices. Reason: This uses standard gates and avoids dense unitaries.
- eq_3: The coin-to-neighbour encoding is fixed as c in {0,1,2} -> v xor (c+1), with c=3 the loop. The abstract does not give this encoding. Reason: The spec asks for an explicit arc encoding, and this one makes S an involution.
