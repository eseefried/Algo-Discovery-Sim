# Equation to Qiskit

Gate-level Qiskit implementation of the Toffoli (CCNOT) target unitary from eq_1, with configurable control and target qubits on a register of 3 to 12 qubits. An optional flag selects the standard H/T/Tdg/CX decomposition instead of the native ccx gate. The paper's pulse-level control, Hamiltonian, and Differential Evolution optimization are not implemented.

Source equation run: `dff39218-e480-4abc-8641-a1c3eecfa2a1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0: control a (least significant bit)
- q1: control b
- q2: target c (flipped iff q0 and q1 are both 1)
- Optional q3..q11: idle spectator qubits if num_qubits > 3
- Computational basis: Qiskit little-endian, qubit 0 is the least significant bit

## Assumptions

- The default qubit order maps a to q0, b to q1, and c to q2.
- The standard H/T/Tdg/CX decomposition is an exact Toffoli up to no extra global phase, so it equals ccx.
- The circuit is closed-system, measurement-free, and unitary.

## Unresolved issues

- The paper's pulse-level single-shot implementation cannot be reconstructed from the abstract.
- No gate duration or transmon parameters are available.
- The fidelity definition and leakage handling remain assumptions.

## Equation mapping

- `eq_1`: implemented; build_circuit (qc.ccx, or the H/T/Tdg/CX decomposition when decompose is true). The Toffoli action |a,b,c> -> |a,b,c xor (a and b)> is applied as a gate on the chosen control and target qubits.
- `eq_2`: background; no code location. The time-ordered propagator describes how a pulse-level gate would be generated. It is context only, and no time evolution is simulated.
- `eq_3`: out_of_scope; no code location. The transmon-chain Hamiltonian is an unconfirmed placeholder. Its parameters and controls are unspecified and pulse-level physics is outside this gate-level circuit.
- `eq_4`: out_of_scope; no code location. The fidelity is an evaluation metric that needs operator construction, which the generated module must not do. Software outside the module can evaluate it.
- `eq_5`: out_of_scope; no code location. The Differential Evolution optimization is a classical loop over pulse parameters. Its enhanced and non-greedy details are unavailable and it is not a quantum circuit operation.

## Specification changes

- eq_2, eq_3, eq_4, eq_5: Narrowed scope to the gate-level Toffoli target unitary (eq_1) only. No pulse-level control, Hamiltonian evolution, fidelity computation, or Differential Evolution optimization is implemented. Reason: The Hamiltonian parameters, pulse parametrization, gate time, and optimizer details are missing. Operator construction and optimization are not allowed in the generated module.
- eq_1: Generalized the qubit labels (a,b,c) to configurable distinct indices on a register of 3 to 12 qubits, with defaults q0 and q1 as controls and q2 as target. This follows Qiskit little-endian ordering instead of a written (a,b,c) ordering. Reason: Gives the operation varying valid parameters while preserving the Toffoli action.
