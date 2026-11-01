# Equation to Qiskit

Exact Toffoli (CCX) on a 3-qubit linear nearest-neighbor chain 0-1-2. The target position is selectable (default q2) and the other two qubits are controls. It uses the Nielsen-Chuang H/T/Tdg/CX decomposition. The one non-adjacent CX (between q0 and q2) is realized as SWAP(1,q) · CX · SWAP(1,q), so every two-qubit gate acts only on adjacent pairs 0-1 or 1-2. The DE-optimized parameterized ansatz is NOT implemented, because no optimized parameters are available and none are fabricated.

Source equation run: `b9f13044-a3a6-442e-a185-57e04fc760eb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control (chain end, little-endian bit 0) when target=2
- qubit 1: control (chain middle, bit 1) when target=2
- qubit 2: target (bit 2) when target=2
- chain adjacency: 0-1 and 1-2 only; for other target values the two non-target qubits are controls
- basis index = x0 + 2*x1 + 4*x2

## Assumptions

- Gate set includes H, T, Tdg, CX and SWAP, with two-qubit gates only on adjacent pairs 0-1 and 1-2
- Little-endian Qiskit ordering; default target is qubit 2
- Pulse-level transmon physics, leakage and decoherence are ignored
- The reported 99.9% fidelity and gate-time claims are not reproduced

## Unresolved issues

- The DE-optimized, single-shot or small-depth variational NN ansatz is not implemented
- It is unknown whether a small-depth nearest-neighbor ansatz reaches F=1
- Pulse-level optimization and timing comparisons are not addressed

## Equation mapping

- `eq_1`: implemented; build_circuit (H/T/Tdg/CX sequence on controls a,b and target c). The circuit implements the Toffoli action exactly (up to no global phase) on the chosen target qubit.
- `eq_2`: out_of_scope; no code location. The layered u-gate ansatz with DE-found angles is not built. No optimized parameters exist and none are invented. A deterministic nearest-neighbor decomposition replaces it.
- `eq_3`: background; no code location. Trace fidelity is an evaluation metric for the runner, not part of the circuit.
- `eq_4`: out_of_scope; no code location. The DE cost minimization is an offline optimization that is not reproduced.
- `eq_5`: out_of_scope; no code location. The DE mutation/crossover update is an optimizer detail, not a circuit operation, and is not implemented.

## Specification changes

- eq_2, eq_4, eq_5: Replaced the DE-optimized parameterized u+entangler ansatz with a fixed analytic Toffoli decomposition restricted to nearest-neighbor interactions (SWAP-routed CX for the 0-2 pair). Reason: Optimized parameters are not supplied and cannot be computed or hardcoded without simulation. An exact known decomposition preserves the target operation (CCX with nearest-neighbor coupling only). This is not the single-shot or pulse-level construction, and it uses more two-qubit gates.
- eq_1: Added an optional 'target' instance parameter selecting which chain qubit is the target (default 2). Reason: Allows varying valid instances while keeping the specified default of q0,q1 controls and q2 target.
