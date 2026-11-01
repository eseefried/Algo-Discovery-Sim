# Equation to Qiskit

Qiskit construction of U_x^T for the fixed 8-vertex tree-with-tail walk (balanced depth-2 NAND, N=4). The classical x chooses the edge set and coin degrees at compile time. Each step applies the per-vertex Grover coins, then the flip-flop shift as basis-state swaps built from CNOT and multi-controlled X gates. It is a walk-dynamics circuit only: no input prep, no measurement, and no decoding of f(x).

Source equation run: `d4c76f7a-766a-4ce2-b8e2-f1d834f9d67a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: slot bit 0 (least significant)
- qubit 1: slot bit 1
- qubit 2: vertex bit 0
- qubit 3: vertex bit 1
- qubit 4: vertex bit 2 (most significant)
- basis index = slot + 4*vertex
- vertices: 0 tail, 1 root, 2 and 3 internal, 4..7 leaves for x1..x4
- slots: 0 parent/tail direction, 1 and 2 child directions, 3 unused
- intended input |t,0> = all-zero state, prepared by the runner

## Assumptions

- The vertex-to-edge-slot assignment is: tail slot0 to root slot0; root slot1 to vertex 2 slot0; root slot2 to vertex 3 slot0; vertex 2 slots 1 and 2 to leaves 4 and 5; vertex 3 slots 1 and 2 to leaves 6 and 7.
- x is a Python list of four 0/1 integers, and x[i] gives the presence of leaf 4+i.
- The runner supplies |t,0> (all-zero) as input.

## Unresolved issues

- This is not the paper's construction, and nothing shows that the output state decodes f(x).
- T and the threshold theta are uncalibrated.
- The tail is a single edge, so there is no real scattering or energy-near-zero analysis.
- The degree-1 coin sign follows the spec's assumption and conflicts with the displayed formula.

## Equation mapping

- `eq_1`: background; no code location. Boolean identity for the reference value f(x). It is not computed in the circuit; x only selects which leaf edges exist.
- `eq_2`: implemented; _coin, _swap and the per-step loop in build_circuit. Coin C_x is vertex-controlled Grover coins on the used slots, with degrees derived from x. Shift S_x is basis-state swaps across present edges. Absent leaves are disconnected and the parent's slot is unused.
- `eq_3`: background; no code location. Initial state |t,0> is the all-zero state, prepared by the runner. The circuit applies no state preparation. The qubit layout follows the stated little-endian encoding.
- `eq_4`: implemented; for _ in range(steps) loop in build_circuit. U_x is applied 'steps' times, T = steps. The heuristic default is 4, which is uncalibrated.
- `eq_5`: out_of_scope; no code location. The return-probability statistic and threshold are offline classical postprocessing. No measurement is in the circuit and no theta is available.

## Specification changes

- eq_2: Degree-1 vertices (tail, present leaves, internal vertices with no present leaf) get coin -1 on their single used slot, as the spec's assumption states. This is implemented as a phase flip on |v,0>. Reason: The literal formula 2|s><s|-I gives +1 for degree 1. The spec's explicit assumption of -1 was followed, so the code differs from the displayed formula.
- eq_2: Degree-2 coins are the swap of the two used slots, which equals 2|s><s|-I on that subspace. Degree-3 coins are the Grover reflection on slots 0..2 with unused slot 3 fixed at +1. Ordering is coin then shift, U = S C. Reason: Standard gates must realize the coin without opaque dense unitaries. The unused slot must be untouched.
- eq_4: The instance has an optional 'steps' (1..32, default 4 via dict.get). The circuit is fixed at 5 qubits and N=4. Reason: T is an uncalibrated free choice. The scope is limited to the depth-2 instance.
- eq_3, eq_5: State preparation and decoding are excluded from the module. Reason: The task requires an operation only, with no preparation or measurement, and no validated theta exists.
