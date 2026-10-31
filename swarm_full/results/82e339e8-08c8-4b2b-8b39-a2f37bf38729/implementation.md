# Equation to Qiskit

Implements the 3-qubit CCZ (control-control-phase) and Fredkin (control-swap) operations as defined by eq_1 and eq_2, using the conventional decomposition into conditional two-qubit gates (5 two-qubit gates for CCZ; Fredkin = CNOT, Toffoli, CNOT). The paper's global-gate constructions (3 and 4 global gates, 7-gate four-qubit phase gate, nearest-neighbour variants) are not given in the abstract and are not implemented.

Source equation run: `9cae2747-b830-4fda-a459-e469a8c48c3f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: q1 (control for Fredkin; CCZ control)
- qubit 1: q2 (Fredkin target 1; CCZ control)
- qubit 2: q3 (Fredkin target 2; CCZ target)
- Qiskit little-endian: qubit 0 is the least significant bit; computational basis, no ancillas

## Assumptions

- Standard textbook definitions of CCZ and Fredkin are the intended operations.
- Exact unitary equality (including global phase) with the ideal gate is the target for the decomposition.
- The Toffoli gate is obtained from CCZ by Hadamards on the target, as stated in the specification.

## Unresolved issues

- The paper's global-gate constructions (3 for CCZ, 4 for Fredkin, 7 for the four-qubit phase gate) are not reproduced and no global-gate count claim is realized by this circuit.
- Nearest-neighbour five-interaction constructions are not implemented.

## Equation mapping

- `eq_1`: implemented; _ccz (and build_circuit with gate='ccz'). Sign flip only on |111> realized with three controlled-phase gates (pi/2, -pi/2, pi/2) and two CNOTs.
- `eq_2`: implemented; build_circuit with gate='fredkin'. Controlled swap realized as CNOT(c->b), Toffoli(a,b->c) from H-CCZ-H, CNOT(c->b).

## Specification changes

- eq_1, eq_2: Implemented the target gate definitions with the conventional conditional two-qubit gate decompositions instead of the paper's 3-global-gate (CCZ) and 4-global-gate (Fredkin) constructions. Reason: The abstract does not give the global gate sequences, rotations, or Hamiltonians, so the paper's constructions cannot be reconstructed.
- eq_1, eq_2: Scope narrowed: the four-qubit conditional phase gate and the five-nearest-neighbour-interaction variants are omitted. Reason: No details given in the abstract or specification.
- eq_1, eq_2: Added optional num_qubits and qubits parameters so the gate can be placed on any three distinct qubits of a register up to 12 qubits. Reason: Allows varying valid instances while keeping the operation definition unchanged.
