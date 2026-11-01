# Equation to Qiskit

Single-qubit operation implementing the alternating two-axis SU(2) rotation sequence U = R_{k_n}(alpha_n)...R_{k_1}(alpha_1). Axis 1 is z and axis 2 lies in the xz-plane at angle theta from axis 1. Axis 2 rotations are built as Ry(theta) Rz(alpha) Ry(-theta). Segment angles, theta, the starting axis and a clockwise-only restriction are instance parameters. The time-optimal search and total-time cost are not implemented.

Source equation run: `2f5a91fb-cd51-4d77-9dca-96fbc2d89bcf`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: the single qubit (Bloch sphere); Qiskit index 0 is the least significant bit
- axis 1 = +z; axis 2 = (sin(theta), 0, cos(theta)) in the xz-plane
- no ancilla qubits

## Assumptions

- Standard spin-1/2 representation with Qiskit rz and ry sign conventions (exp(-i phi P/2)).
- Axes alternate strictly. Consecutive rotations about the same axis would merge into one.
- Rotation speeds are irrelevant to the unitary, so the circuit does not use them.
- Up to 64 segments are allowed.

## Unresolved issues

- The paper's explicit angle bounds, three-angle parametrization and scaling laws are not available, so the circuit does not encode time-optimality.
- The 'clockwise' sign convention relative to the physical orientation of the axes is assumed.

## Equation mapping

- `eq_1`: implemented; _rotate. Rotation about axis 1 is rz(alpha). Rotation about axis 2 is ry(-theta), rz(alpha), ry(theta) in circuit order, which equals exp(-i alpha/2 n_2.sigma) for n_2 at angle theta from z in the xz-plane.
- `eq_2`: implemented; build_circuit (loop over alphas). Alternating product of rotations. alpha_1 is applied first (rightmost factor), the axis alternates, and first_axis selects the starting axis.
- `eq_3`: out_of_scope; no code location. Total time is a classical cost used for the optimal search and does not change the unitary. Rotation speeds Omega_k are not circuit parameters, and no optimization is done.

## Specification changes

- eq_1: Fixed a concrete frame: n_1 = z and n_2 = (sin theta, 0, cos theta). Reason: The spec gives abstract axes. Any pair of non-parallel axes with angle theta is unitarily equivalent to this one, so this loses no generality up to a global frame change.
- eq_2: Added an explicit first_axis parameter and an explicit ordering convention (alpha_1 applied first). The equation's final-axis subscripts are replaced by strict alternation starting from first_axis. Reason: The spec leaves the first and last axis unspecified. A concrete circuit needs a definite choice.
- eq_2, eq_3: Scope narrowed to synthesizing a given sequence of angles. No time-optimal search, no angle bounds, and no minimum-time evaluation are done. Reason: The abstract does not give the bounds or the three-angle parametrization, and eq_3 is an assumed classical cost.
- eq_1, eq_2: The clockwise-only case is modeled as requiring all angles >= 0. Counterclockwise rotations are allowed as negative angles when clockwise_only is false. Reason: This is the assumed sign convention for the two direction sets in the abstract.
