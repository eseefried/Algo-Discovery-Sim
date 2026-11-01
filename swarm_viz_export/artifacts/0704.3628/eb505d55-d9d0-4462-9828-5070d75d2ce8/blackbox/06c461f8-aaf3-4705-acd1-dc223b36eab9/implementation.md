# Equation to Qiskit

Fixed unitary 5-qubit coined quantum walk on the 8-vertex tail+root+2 internal+4 leaf tree for the N=4 balanced NAND formula. The 4 input bits x are compiled into the flip-flop shift: leaf edges exist only where x_i=1, and absent leaf edges act as self-loops (reflecting). Each step is a coin I-2|s><s| (-1 on degree-1 slots) followed by the shift, repeated T times. State preparation, decoding and threshold calibration are left to the runner.

Source equation run: `c3b98cf5-0ddd-4902-9a42-2d32d39280fc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: slot bit 0 (LSB of slot)
- qubit 1: slot bit 1 (slot in 0..2 used; slot 3 unused)
- qubit 2: vertex bit 0
- qubit 3: vertex bit 1
- qubit 4: vertex bit 2
- basis index = slot + 4*vertex; vertices: 0 tail, 1 root, 2 internal a (leaves 4,5), 3 internal b (leaves 6,7), 4-7 leaves for x1..x4
- slots: 0 toward parent/tail; 1,2 toward children (root: 1->a, 2->b; a: 1->leaf4, 2->leaf5; b: 1->leaf6, 2->leaf7)
- input |t,0> = |00000> (runner default, no preparation in the circuit)

## Assumptions

- Vertex/slot numbering and edge layout as in register_layout
- x is classical and compiled into the gates
- Absent leaf edges are reflecting self-loops
- steps is an integer in 1..64
- Controlled coin gates are built from standard gates via circuit-to-gate conversion and .control

## Unresolved issues

- No threshold or T is known to separate all 16 inputs; the circuit may be only a walk-dynamics demo
- The paper's actual walk, weights and phase-estimation procedure are not reconstructed
- The decode direction (reflection vs transmission) is unverified
- The general-formula O(N^(1/2+O(1/sqrt(log N)))) algorithm is not implemented

## Equation mapping

- `eq_1`: background; no code location. Boolean identity defining f(x) for the N=4 instance. It is not a gate; x enters only through which leaf edges are present.
- `eq_2`: implemented; _step, _coin3_gate, _phase_on, _swap_states. U_x = S_x C_x: the coin is -1 on degree-1 slots and I-2|s><s| on degree-3 vertices controlled on the vertex register. The shift is a product of disjoint basis-state transpositions over the x-dependent edge set.
- `eq_3`: background; no code location. |t,0> is the all-zero basis state, which the runner prepares. The circuit contains no state preparation.
- `eq_4`: implemented; build_circuit (loop over steps calling _step). U_x^T is built by repeating the step T times, with T given by instance['steps'].
- `eq_5`: out_of_scope; no code location. Decoding via the return probability and threshold calibration is classical post-processing/measurement and is excluded from the unitary operation.

## Specification changes

- eq_2: The coin is I-2|s><s| on the used slots (the negated Grover coin), which gives -1 for degree-1 vertices as the spec states. It is identity on unused slot 3. Reason: The spec's 'Grover coin' (2|s><s|-I) gives +1 at degree 1, contradicting its stated -1 phase. A single sign convention is needed.
- eq_2: Parent vertices (root, a, b) keep degree 3 and use the full 3-slot coin even when a leaf edge is absent. The absent edge is a self-loop (shift fixes that state), and absent leaves are isolated and never populated. Reason: Makes the reflecting-boundary assumption concrete and keeps the coin x-independent except at present leaves.
- eq_2: The flip-flop shift swaps |u, slot at u pointing to v> with |v, slot at v pointing to u>, not the same slot index e on both sides. Reason: The spec's 'same e' wording is ambiguous. Slot labels are direction-dependent, so the edge-specific slot pair is the consistent flip-flop.
- eq_3: The initial state is not prepared in the circuit; |t,0> = |00000> is supplied by the runner. Reason: The task requires an operation without input-state preparation.
- eq_4: T is an input parameter (1..64) rather than fixed to O(sqrt N). Reason: The spec leaves T to calibration.
- eq_5: The decode statistic and threshold are not implemented. Reason: They are measurement/post-processing.
- eq_1, eq_2, eq_4, eq_5: Scope narrowed to the explicit-x, compiled, N=4 walk. There is no black-box query claim, and no claim that the walk decodes f(x). Reason: The paper's exact construction is unknown and the decode is unvalidated.
