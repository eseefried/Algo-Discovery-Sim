# Equation to Qiskit

Two-qubit circuit for the slice-product unitary of eq_3. Each slice applies the Zeeman Rz phases, then the exact Heisenberg exchange exp(-i J dt/4 (XX+YY+ZZ)), then single-spin drive rotations R(theta, phase). Slice angles are supplied in the instance. No optimal-control search is performed, and the circuit contains no state preparation or measurement.

Source equation run: `f85f0f20-ffc9-4421-9bff-f1dce3c32a8c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = electron 1 spin (least significant bit)
- q1 = electron 2 spin
- No ancilla qubits; total 2 qubits

## Assumptions

- hbar=1 and the Heisenberg exchange has normalization J/4 (XX+YY+ZZ)
- Rz(phi) = exp(-i phi Z/2) with phi = g_j mu_B B_k dt supplied by the user
- Slice 1 is applied first
- Qiskit little-endian ordering with q0 = electron 1
- Number of slices limited to 1..100
- Global phase is not tracked

## Unresolved issues

- Actual parameter values (J, delta g, B) and optimized control angles are unknown
- The exchange-suppression pulse sequence is unspecified
- Trotter splitting error within slices is not controlled
- The RWA and the selectivity condition are not enforced

## Equation mapping

- `eq_1`: background; no code location. Continuous-time model Hamiltonian that the slice circuit approximates. It is not built directly, because the lab-frame time-dependent RF drive is replaced by rotating-frame rotations.
- `eq_2`: background; no code location. Selective-resonance condition. It determines which angles an optimizer would choose. The circuit takes per-spin drive angles as inputs and does not check the inequality.
- `eq_3`: implemented; build_circuit (per-slice loop: rz, rxx/ryy/rzz, r). Slices are ordered with slice 1 first, matching the product over k from N down to 1. Within a slice the order is Rz, then exchange with angle J dt/2 per Pauli-pair rotation, then drive rotations. The user supplies the Zeeman angles phi_{j,k} directly.
- `eq_4`: out_of_scope; no code location. The fidelity objective and GRAPE optimization are offline classical post-processing and are not part of the operation.
- `eq_5`: background; no code location. Identity showing that a common sigma_x pi pulse leaves the Heisenberg coupling unchanged. A decoupling sequence is not implemented, since it is unspecified.

## Specification changes

- eq_3: Zeeman angles phi_{j,k}, per-spin drive (theta, phase) pairs and J*dt are taken directly from the instance. No g_j, mu_B, B_k or dt are computed inside the module. Reason: The numerical parameters and optimized angles are not given in the abstract. This keeps the construction general and valid for any slice parameters.
- eq_1, eq_3: The drive in each slice is a rotating-frame rotation exp(-i theta/2 (cos(phase) X + sin(phase) Y)) applied separately to each spin, rather than a common simultaneous drive. The Zeeman, exchange and drive factors are sequentially Trotterized, so the circuit is an approximation unless the angles absorb the splitting error. Reason: Selective resonance is represented by per-spin drive angles, with an RWA-like assumption. The non-commuting terms cannot be exponentiated exactly together with standard gates.
- eq_5: eq_5 is treated as a true but non-suppressing identity (simultaneous sigma_x conjugation leaves the Heisenberg coupling invariant), not as an exchange-suppression construction. Suppression would need spin-selective pulses, which are not implemented. Reason: The equation is a symmetry fact, and its label and description conflict with its use as suppression.
- eq_4: Scope narrowed to the circuit construction only. No optimal-control search is performed and no target gate is hard-coded. Reason: Offline optimization and the optimized angles are not specified in the abstract.
