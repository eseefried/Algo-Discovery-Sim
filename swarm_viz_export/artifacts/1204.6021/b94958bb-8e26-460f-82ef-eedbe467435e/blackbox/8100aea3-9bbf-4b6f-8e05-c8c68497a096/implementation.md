# Equation to Qiskit

Logical-level 2-qubit circuit for the dual-rail bosonic-walker gate algebra: Rx(theta) on logical qubit 0, then Rz(phi) on logical qubit 1, then CZ. It acts on the 4-dimensional logical space only. It does not simulate the Bose-Hubbard dynamics, the graph geometry, or the walker routing.

Source equation run: `7f01a5a6-dd8a-4dcd-ac22-5f8ba1c6aa5d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Circuit qubit 0 = logical qubit 1 (q1), dual rail on sites 2,3: |0> = walker on site 2, |1> = walker on site 3; least significant bit
- Circuit qubit 1 = logical qubit 0 (q0), dual rail on sites 0,1: |0> = walker on site 0, |1> = walker on site 1; most significant bit
- Computational basis index = 2*q0 + q1, which equals the Qiskit little-endian integer of (qubit1, qubit0)

## Assumptions

- Inputs are prepared in the logical 4-dimensional space by the runner, and the circuit contains no state preparation or measurement.
- Instance parameters theta and phi are finite real numbers in radians.
- The dual-rail walkers are idealized as exactly one per qubit, and tunnelling, detuning and interaction phases are exact.

## Unresolved issues

- The piecewise-constant graph construction, the walker routing and the swap gate are not implemented.
- The Steane code, the 3D extension and the optical-lattice implementation are out of scope.
- The physical parameters (J, U, detuning, times) that realize the gates are not modelled.

## Equation mapping

- `eq_1`: background; no code location. The Bose-Hubbard Hamiltonian is the underlying physical model. It is not simulated; the reduced logical gates replace its dynamics.
- `eq_2`: implemented; build_circuit docstring and register_layout: logical qubit 0 -> circuit qubit 1, logical qubit 1 -> circuit qubit 0. The dual-rail encoding is realized as one circuit qubit per rail pair, with basis index 2*q0+q1 preserved by the qubit assignment.
- `eq_3`: implemented; build_circuit: qc.rx(theta, 1). Rx(theta) = exp(-i theta X/2) on logical qubit 0, with the hopping generator compiled directly into the standard gate.
- `eq_4`: implemented; build_circuit: qc.rz(phi, 0). Rz(phi) = diag(exp(-i phi/2), exp(i phi/2)) on logical qubit 1, with the detuning compiled directly into the standard gate.
- `eq_5`: implemented; build_circuit: qc.cz(1, 0). The interaction phase exp(-i Ut |11><11|) at Ut = pi equals diag(1,1,1,-1) and is applied as CZ.
- `eq_6`: implemented; build_circuit: gate order Rx on q0, Rz on q1, CZ. The composite U_tot = CZ (I x Rz(phi)) (Rx(theta) x I) is built by applying the gates in that order.

## Specification changes

- eq_3: Implemented the standard Rx(theta) = exp(-i theta X/2). The literal hopping form exp[i Jt (a0^dag a1 + h.c.)] with Jt = theta/2 equals Rx(-theta), so a sign convention (Jt = -theta/2) is absorbed. Reason: The spec's stated equality has a sign inconsistency; the intended unitary is Rx(theta).
- eq_1, eq_3, eq_4, eq_5: Scope narrowed from the many-body bosonic dynamics to the 4-dimensional logical space. The gates are compiled directly and no Hamiltonian evolution or walker routing is simulated. Reason: The graph geometry and gate schedules are not specified, and no opaque unitaries or Hamiltonian simulation are allowed.
- eq_2, eq_6: Mapped logical qubit 0 (left tensor factor, most significant) to Qiskit qubit 1 and logical qubit 1 to Qiskit qubit 0. Reason: Qiskit qubit 0 is the least significant bit, while the spec uses basis index 2*q0+q1.
- eq_5: Ut is fixed at pi and is not an instance parameter. Reason: The CZ gate requires Ut = pi.
