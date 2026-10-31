# Equation to Qiskit

Implements the ideal Toffoli (CCNOT) target unitary of eq_1 as a measurement-free Qiskit circuit on a register of 3 to 12 qubits, with configurable control and target indices. The paper's pulse-level optimal-control synthesis (Differential Evolution, transmon Hamiltonian) is not reconstructed, because the abstract does not specify it. The fidelity objective eq_2 is not implemented.

Source equation run: `43abf61d-e4db-4998-84df-f69218363dd0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control a (end of chain, spec register q0)
- qubit 1: control b (middle of chain, spec register q1)
- qubit 2: target c (spec register q2)
- Qiskit little-endian: basis index = a + 2*b + 4*c, so the bitstring reads c b a
- If num_qubits > 3, extra qubits are idle spectators

## Assumptions

- Target qubit is at one end of the chain (index 2), with control b in the middle.
- The ideal Toffoli unitary stands in for the pulse-synthesized U(T) with F >= 0.999.
- Leakage and noise are ignored; the circuit is the ideal gate-level operation.
- Input states and measurements are supplied by the runner.

## Unresolved issues

- The actual transmon control-pulse implementation and Differential Evolution procedure are not reconstructed.
- The paper's fidelity definition and gate time are unknown.
- The qubit ordering and target choice in the paper are unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.ccx(qr[a], qr[b], qr[c]). The ideal Toffoli action |a,b,c> -> |a,b,c XOR ab> is implemented with the standard CCX gate on the selected control and target qubits.
- `eq_2`: out_of_scope; no code location. The fidelity objective belongs to the classical Differential Evolution optimization of pulses. It is an assumed definition and is not part of the gate operation, so it is not a circuit element.

## Specification changes

- eq_1, eq_2: Scope narrowed to the ideal target unitary (a single ccx gate). The pulse-level single-shot control synthesis, the transmon Hamiltonian, and the optimizer are not implemented. Reason: The abstract gives no Hamiltonian, pulse parameterization, gate time, or optimizer details, and the required output is a unitary gate-model Qiskit circuit.
- eq_1: Added optional num_qubits and configurable control and target indices, which generalize the fixed 3-qubit chain layout. Reason: The operation must accept varying valid parameters. The default layout (a=0, b=1, c=2) matches the specification.
