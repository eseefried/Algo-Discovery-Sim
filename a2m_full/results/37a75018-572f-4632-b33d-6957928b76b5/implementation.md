# Equation to Qiskit

Measurement-free 4-qubit two-qubit Simon sampling operation: H on x (q0,q1), a Simon oracle U_f built from CNOTs for a hidden period s given in the instance, then H on x. The oracle uses f(x)=x xor (x_j s), where j is the highest set bit of s, and f(x)=x for s=00. The f-register collapse is left to deferred measurement by the runner. Input state and measurements are supplied by the runner.

Source equation run: `395d74f9-624d-477d-b2dd-799063a6ca8f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0: x bit 0 (least significant), input/readout register
- q1: x bit 1, input/readout register
- q2: f bit 0, oracle output register
- q3: f bit 1, oracle output register
- Qiskit little-endian: s string is written s1s0 and bits[::-1][i]=s_i

## Assumptions

- s is given as a 2-character bit string s1s0 with q0 as the least significant bit
- The oracle form |x>|y> -> |x>|y xor f(x)> is used with f(x) = x xor (x_j s), j the highest set bit of s; for s=00, f is the identity copy (a 1-to-1 function)
- The runner prepares |0000> and measures q0,q1 (optionally q2,q3)

## Unresolved issues

- The specific Simon functions used in the original experiment are not given, so the oracle choice is a representative one
- Verification of s=0 versus nonzero via an f(x) comparison is not implemented

## Equation mapping

- `eq_1`: implemented; build_circuit: initial H layer and CNOT oracle block. Hadamards create the uniform superposition on x and the CNOT-built oracle XORs f(x) into the f register (runner supplies |0000>).
- `eq_2`: background; no code location. Collapse from measuring the f register is not implemented because measurements are excluded; by deferred measurement the x statistics are the same, and the runner may measure.
- `eq_3`: implemented; build_circuit: final H layer on q0,q1. The final Hadamards on x map the pair state to the distribution supported on y.s=0; sampling itself is done by the runner.
- `eq_4`: background; no code location. Classical linear-constraint property of the samples; not a circuit element.
- `eq_5`: out_of_scope; no code location. Classical brute-force decoding of s is postprocessing, not part of the quantum operation.

## Specification changes

- eq_1: The opaque oracle is replaced by an explicit CNOT oracle f(x)=x xor (x_j s) parameterised by s in the instance, which is one valid 2-to-1 Simon function. Reason: The circuit must be built from standard gates with no opaque unitaries; f is not otherwise specified.
- eq_2: The mid-circuit f-register measurement is omitted (deferred/ignored). Reason: Measurements and dynamic circuits are not allowed in the returned operation; x statistics are unchanged.
- eq_3, eq_4, eq_5: Scope narrowed to the quantum sampling circuit; the multiple samples (m), constraint solving and decoding are left to the runner. Reason: The output is a single unitary operation with no sampling or classical postprocessing.
- eq_1, eq_2, eq_3, eq_4, eq_5: Only n=2 logical qubits (4 physical qubits); the cluster-state one-way implementation, ancilla verification and n-qubit scaling are excluded. Reason: The specification does not give the cluster-state angles or the verification circuit.
