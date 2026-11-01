# Equation to Qiskit

Qiskit operation for the assumed minimal instance: one walker on two vertices is a dual-rail qubit, stored as one circuit qubit. A tunneling-generated X rotation U_X = RX(-2Jt) is followed by an on-site-offset-generated Z rotation U_Z = RZ(Delta*t), both on a chosen target qubit of an n-qubit register. Other qubits are untouched. No inputs, measurements or sampling are included.

Source equation run: `00ab34cd-2883-4cb5-b7f5-b62d5d3660aa`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Circuit qubit k (k = 0..num_qubits-1; index 0 is least significant) is one logical dual-rail qubit.
- |0> on qubit k is the walker at vertex 1 (|0>_L = a_1^dag|vac>); |1> is the walker at vertex 2 (|1>_L = a_2^dag|vac>).
- Gates act only on qubit 'target'; the other qubits are idle.
- No ancilla qubits and no explicit bosonic Fock-space register.

## Assumptions

- The logical qubit is a single walker on two vertices, with |0>_L at vertex 1 and |1>_L at vertex 2.
- epsilon_1 = epsilon_2 during the hopping step and J = 0 during the potential step.
- The sign convention of eq_1 holds, so the hopping term is -J and RX angle is -2 J t.
- Evolution times are nonnegative.
- The gate is applied to one target qubit of an n-qubit register (n <= 12), with the rest idle.

## Unresolved issues

- The paper's actual graph geometry, encoding, and parameter schedules are unknown.
- The cphase and swap constructions with interacting bosons are not implemented.
- The Steane code, 3D extension, and optical lattice details are not covered.
- The one-qubit model does not reflect the paper's linear-in-qubits vertex scaling.

## Equation mapping

- `eq_1`: background; no code location. Generic Bose-Hubbard Hamiltonian. It is the origin of the hopping and on-site-energy terms but is not simulated; U drops out for a single walker.
- `eq_2`: implemented; build_circuit docstring: logical qubit encoding, one circuit qubit per two-vertex walker. The dual-rail walker position encoding is the identification of the circuit qubit basis states with vertex 1 and vertex 2. Input state preparation is left to the runner.
- `eq_3`: implemented; build_circuit: qc.rx(theta, target) with theta = -2*J*t_hop. Single-walker hopping evolution equals the logical rotation exp(iJtX) = RX(-2Jt) in Qiskit's convention RX(theta) = exp(-i theta X/2).
- `eq_4`: implemented; build_circuit: qc.rz(phi, target) with phi = delta*t_pot. The relative on-site potential gives exp(-i phi Z_L/2), with Z_L = n1 - n2 = diag(1,-1) matching Qiskit's Z and RZ(phi) = exp(-i phi Z/2).
- `eq_5`: out_of_scope; no code location. The cphase and swap gate definitions need the interacting multi-walker construction, which the abstract does not specify. They are not implemented.

## Specification changes

- eq_3, eq_4: Time-dependent Hamiltonian evolutions are replaced by the equivalent ideal single-qubit gates RX(-2 J t_hop) then RZ(delta t_pot). The two segments use separate durations t_hop and t_pot, and the gate order is X then Z. Global phases are ignored. Reason: The unitaries are exactly these rotations for the assumed two-vertex single-walker model. Separate durations follow the two sequential steps in the spec.
- eq_1, eq_2: Scope is narrowed to the one-walker, two-vertex logical qubit, with the logical qubit stored directly in the circuit qubit instead of a bosonic Fock-space simulation. The interacting multi-walker, piecewise-constant graph is not modelled. Reason: The abstract does not give the graph, parameters, or multi-walker encoding, so the minimal assumed instance is implemented.
- eq_5: The cphase and swap gates are excluded. Reason: Their bosonic construction is unspecified, and the standard gate matrices alone would not reproduce the paper's mechanism.
