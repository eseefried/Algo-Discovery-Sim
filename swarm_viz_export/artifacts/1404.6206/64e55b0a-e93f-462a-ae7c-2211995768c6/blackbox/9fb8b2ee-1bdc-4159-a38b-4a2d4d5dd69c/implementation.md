# Equation to Qiskit

build_circuit(instance) applies H to m control qubits and then a CNOT fan-out from the controls to the n-m target qubits. The fan-out follows a GF(2)-linear map f given as a 0/1 matrix. This is the unitary U of eq_2. Acting on a runner-prepared basis input |a>|y>, U gives the Bell-like state of eq_1. The default is n=3, m=2 with f(c1,c2)=c1 xor c2 (eq_4). Only this generic X-type construction is implemented, not the paper's two specific controlled-unitary gates.

Source equation run: `676e596d-38fa-41b0-84f9-add9468f6e77`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = c1 (control, H applied, least significant Qiskit bit)
- qubit 1 = c2 (control, H applied)
- qubit 2 = t (target, CNOT fan-out; t gets c1 xor c2 for the example)
- General: qubits 0..m-1 are controls, qubits m..n-1 are targets
- Input basis |a>|y> is prepared by the runner: a on controls, y on targets, computational-basis encoding with qubit 0 as least significant bit

## Assumptions

- f is GF(2)-linear and X-type only (CNOT fan-out).
- The controls are the first m qubits in register order.
- If f_matrix is omitted, every target receives the parity of all controls.
- The runner prepares the input |a>|y> on the controls and targets respectively, in little-endian computational-basis encoding.

## Unresolved issues

- The paper's actual two multiple-qubit controlled-unitary gates are unknown, so this is not the paper's exact construction.
- With the default f (a single parity target) f is not injective, but the offset y still labels states uniquely, so orthonormality still holds.
- Entanglement and monogamy-score properties are not addressed.

## Equation mapping

- `eq_1`: implemented; build_circuit (full circuit: H loop followed by CNOT fan-out). The circuit acting on |a>|y> produces 2^{-m/2} sum_c (-1)^{a.c}|c>|f(c) xor y>. Input preparation is left to the runner.
- `eq_2`: implemented; build_circuit: 'for i in range(m): qc.h' then the double loop with qc.cx. H on the controls followed by the X-type controlled fan-out onto the targets.
- `eq_3`: background; no code location. Orthonormality follows because the circuit is unitary. No code is needed, and checking it is left to external verification.
- `eq_4`: implemented; build_circuit: default f_matrix [[1]*m for _ in range(n-m)], which gives [[1,1]] for n=3, m=2. The default f is the parity of all controls, realized as CNOT c1->t and CNOT c2->t. A general matrix can also be supplied.
- `eq_5`: background; no code location. The multi-controlled-X form is a schematic, unverified gate definition and is not used in the CNOT fan-out instance. It is not implemented.

## Specification changes

- eq_1, eq_2, eq_4: Generalized from the fixed n=3, m=2 instance to a parameterized family. n, m and an optional GF(2) matrix f_matrix are accepted, with n<=12. The default reproduces eq_4. Reason: The task requires the operation to work for varying valid instance parameters. The default keeps the specified instance.
- eq_1, eq_2: Qubit mapping: controls occupy Qiskit qubits 0..m-1 and targets occupy m..n-1, so the first control c1 is qubit 0, the least significant bit. The spec's 'qubit 0 is most significant in the label' is not followed. Reason: Qiskit is little-endian. The circuit is defined by the physical register layout, and the runner must map the label x=(a,y) to this layout.
- eq_2: The input-loading X gates in the spec's step 1 are not part of the returned circuit. Reason: The runner prepares inputs, and the circuit must be an operation, not an experiment.
- eq_5: The multi-controlled-X projector form is not implemented and no multi-controlled gate is used. Reason: The form is schematic and unverified, and the chosen instance uses only CNOTs.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to a generic Hadamard plus CNOT-fan-out Bell-like basis. The paper's two specific controlled-unitary gates, phase-type gates, the qudit extension, and the entanglement and monogamy analyses are not implemented. Reason: These details are not available in the abstract-derived specification.
