# Equation to Qiskit

Implements the unitary core of a Trugenberger-style Hamming-distance interference step: CNOTs XOR the input register into the pattern register, per-bit controlled phases (angle pi/n) act from an ancilla, the XOR is uncomputed, and a final Hadamard on the ancilla follows. The runner must prepare |M> (eq_1), |x> and the ancilla in |+>. The classification vote (eq_5) is classical and not implemented. The class register is optional and untouched.

Source equation run: `46978259-42a9-4b82-8854-9657211ad1b3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: pattern register (stored patterns |x^k>, little-endian, bit j on qubit j)
- qubits n..2n-1: input register |x> (bit j on qubit n+j)
- qubit 2n: ancilla (must enter in |+>; ancilla=0 is the post-selected outcome)
- qubits 2n+1..2n+class_qubits: optional class register (untouched by the operation)
- Example n=3, class_qubits=1: pattern 0-2, input 3-5, ancilla 6, class 7

## Assumptions

- The ancilla enters in |+> and the pattern and input registers hold computational-basis superpositions prepared by the runner.
- Little-endian qubit order within each register: bit j of a pattern is on qubit j, and bit j of the input is on qubit n+j.
- The optional class register is only reserved in the layout, with no gates applied.
- The phase schedule is a generic Trugenberger-style construction, not the paper's verified circuit.

## Unresolved issues

- The paper's exact state-preparation and training-set storage method is unknown.
- The paper's exact circuit and phase schedule are unverified.
- MNIST binarization and encoding are not addressed.
- The paper's classification rule and advantage claims are not reconstructed.

## Equation mapping

- `eq_1`: background; no code location. The memory superposition |M> is input-state preparation, done by the runner. The circuit acts on it but does not create it.
- `eq_2`: implemented; build_circuit: CNOT loops (cx input_j -> pattern_j) computing x_j XOR x^k_j. The bitwise XOR whose Hamming weight is d_H is computed into the pattern register, and uncomputed after the phase step.
- `eq_3`: implemented; build_circuit: cp(pi/n, ancilla, pattern_j) loop. Ancilla-controlled phase proportional to d_H. The ancilla=1 branch gets exp(i*pi*d_H/n) relative to the ancilla=0 branch.
- `eq_4`: implemented; build_circuit: final qc.h(ancilla). The final Hadamard on the ancilla yields P(anc=0 | k) = cos^2(pi d_H/(2n)). The 1/p factor comes from the runner-prepared uniform |M>.
- `eq_5`: out_of_scope; no code location. The classification rule is classical post-processing of measurement counts and is not part of the unitary operation.

## Specification changes

- eq_3, eq_4: The relative phase between ancilla branches is pi*d_H/n, not pi*d_H/(2n) as written in eq_3. Reason: With the ancilla in |+> and a final Hadamard, a relative phase theta gives P(0)=cos^2(theta/2). Reproducing eq_4, cos^2(pi d_H/(2n)), requires theta=pi*d_H/n. Using pi/(2n) would give cos^2(pi d_H/(4n)), contradicting eq_4.
- eq_1, eq_5: Scope narrowed to the unitary distance-interference operation. State preparation (|M>, |x>, ancilla |+>), measurement, post-selection and voting are excluded. Reason: The task requires an operation circuit with no state preparation or measurement.
- eq_3: The ancilla Hadamard that prepares |+> is not included. The runner must supply the ancilla in |+>. Reason: Ancilla preparation is input preparation. A single Hadamard at the end completes the interference.
