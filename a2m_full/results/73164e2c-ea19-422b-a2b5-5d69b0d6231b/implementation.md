# Equation to Qiskit

Implements the SWAP-routing construction (eq_4) from the specification. A logical Clifford+T circuit on n<=12 qubits is mapped onto a 1-D line of physical qubits from a given initial placement. Each non-adjacent CX is routed by moving the control along the shortest path with SWAPs, each decomposed as CX(a,b) CX(b,a) CX(a,b). The permutation accumulated by routing is left in place by default, or optionally undone with an adjacent-SWAP sort. Scheduling, force-directed scheduling, placement optimisation and ULB sizing are not implemented.

Source equation run: `f0f31957-e85b-47bb-8038-1fb9e00b3791`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits q[0..n-1] are physical qubits on a 1-D line, with adjacency between q[i] and q[i+1]. Little-endian: q[0] is the least significant bit.
- Logical qubit i initially resides on physical qubit placement[i] (identity by default). The runner prepares inputs on physical qubits.
- With restore_permutation=false, logical qubit i ends at the physical position given by the routing permutation (P_pi). With true, it returns to placement[i].
- No ancillas.

## Assumptions

- Logical gate order is the given order, and no reordering by scheduling is applied.
- Adjacent physical qubits on the line are the only coupled pairs.
- The SWAP-moved control stays at its new position afterwards, so the permutation accumulates.
- The input state is prepared by the runner on physical qubits consistent with placement, and logical qubit i starts at physical placement[i].
- Gate list length is capped at 500 for safety.

## Unresolved issues

- The paper's QDFG construction, force modification, ULB architecture, and routing congestion model are unknown and not reproduced.
- 2-D grid routing is not implemented.
- The 40% latency reduction is not reproduced, and the circuit carries no latency information.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Slack/ASAP/ALAP scheduling is a classical compiler computation with no unitary realization; the chosen construction is only SWAP routing.
- `eq_2`: background; no code location. Force-directed scheduling is classical background; the paper's modification is unknown, and gate order is taken as given.
- `eq_3`: background; no code location. Timing-driven placement cost is not optimised in the circuit. The resulting placement is supplied as the 'placement' input, and routing uses its Manhattan distance on the line implicitly.
- `eq_4`: implemented; _swap (CX-CX-CX SWAP decomposition with permutation tracking) and build_circuit (shortest-path routing loop, optional restore). SWAP = CX_ab CX_ba CX_ab is implemented exactly. The mapped circuit yields P_pi|psi_orig>, with P_pi tracked by loc/occ. The fidelity check F is a classical post-processing criterion left to the runner.
- `eq_5`: out_of_scope; no code location. Weighted ULB size argmin is a classical optimisation over given latencies, with no quantum circuit content.

## Specification changes

- eq_1, eq_2, eq_3, eq_5: Scope narrowed to the routing construction only. No scheduling, force computation, placement search or ULB selection is done in the circuit. Reason: These are classical compiler computations that do not define a unitary operation.
- eq_4: Topology fixed to a 1-D line (1xn) with n<=12. Placement is an input permutation, and the control qubit is moved toward the target along the shortest path. The final permutation is kept by default, with an optional adjacent-SWAP sort to undo it. Reason: The spec's tiny instance is a 1x4 line. The operation needs a deterministic, testable routing rule, and the permutation criterion in eq_4 is checked externally.
- eq_4: The fidelity criterion F=|<psi_orig|P_pi^dagger|psi_map>|^2 is not placed in the circuit. P_pi is determined by the routing and placement inputs, so the runner must derive it. Reason: Circuit generation must be measurement-free and contain no reference or test code.
- eq_4: The supported logical gate set is limited to h, s, sdg, t, tdg, x, z and cx. Reason: Clifford+T matches the specified instance. This limit also keeps the implementation compact and the validation simple.
