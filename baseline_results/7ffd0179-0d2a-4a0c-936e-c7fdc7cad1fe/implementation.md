# Equation to Qiskit

Qiskit module implementing the unitary core of the Trugenberger-style Hamming-distance classifier from the specification: CNOTs from input to memory qubits (eq_2), the ancilla-controlled distance-to-phase unitary U = exp(-i pi/(2n) Z_c (x) sum_j (I-Z_j)/2) decomposed into single-qubit phase and controlled-phase gates (eq_3), and the final Hadamard on the ancilla (eq_4). The training-superposition input state (eq_1) is supplied by the runner; measurements, postselection and the classical vote (eq_5) are outside the returned operation. Register layout: input qubits 0..n-1, memory qubits n..2n-1, class qubits 2n..2n+m-1, ancilla qubit 2n+m.

Source equation run: `726b1fe5-abf6-4c08-a925-103b33aa611b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: inp[0] = input bit x_1 (register I, unchanged by the circuit)
- qubit 1: inp[1] = input bit x_2
- qubit 2: mem[0] = training bit x^k_1 (register M), overwritten with x_1 XOR x^k_1
- qubit 3: mem[1] = training bit x^k_2, overwritten with x_2 XOR x^k_2
- qubit 4: cls[0] = class label y^k (register Y, binary class; idle in the operation, measured by the runner on postselected runs)
- qubit 5: anc[0] = ancilla c, expected in |+> at input, H applied at the end, postselect outcome 0
- Encoding: computational basis, qubit index 0 is the least significant bit; pattern bit j (j=1..n) of a register sits in that register's qubit j-1
- Expected input state for eq_6: (1/sqrt2)(|00>_I|00>_M|0>_Y + |00>_I|01>_M|1>_Y)(|0>+|1>)_c/sqrt2, where |01>_M means x^2_1 = 0 in mem[0] and x^2_2 = 1 in mem[1]

## Assumptions

- Pattern bit j (1-indexed) of each register is stored in that register's qubit j-1; Qiskit index 0 is the least significant bit.
- The ancilla is supplied in |+> and the memory register holds the uniform superposition of training patterns entangled with class labels, as in eq_1.
- Phase scale theta = pi/(2n) as in the specification, so d_k = n yields zero amplitude for ancilla outcome 0.
- The sign convention diag(e^{-i theta}, e^{+i theta}) for the ancilla branches follows eq_3; outcome probabilities are convention independent.
- Class register qubits are untouched by the operation and only serve as entangled labels read out by the runner.

## Unresolved issues

- The paper's exact circuit (phase scale, ancilla handling, decision rule, multi-class label encoding) is not known from the abstract; the implementation follows the reconstructed Trugenberger routine.
- The storage algorithm for the training superposition and the MNIST binarisation are not implemented; the runner must supply the eq_1 input state.

## Equation mapping

- `eq_1`: background; no code location. The training superposition with input pattern and |+> ancilla is the input state of the operation; the runner prepares it (no state preparation is allowed in the returned circuit). Documented in the module docstring and register_layout.
- `eq_2`: implemented; build_circuit, loop commented '# eq_2' (qc.cx(inp[j], mem[j])). One CNOT from input qubit j to memory qubit j for all j, leaving mem in |x XOR x^k> with Hamming weight d_k.
- `eq_3`: implemented; build_circuit, block commented '# eq_3' (qc.p(-theta, mem[j]); qc.cp(2*theta, mem[j], anc[0])). U = exp(-i pi/(2n) Z_c (x) sum_j |1><1|_j) is factorised into commuting terms; each term equals a phase gate P(-theta) on mem[j] followed by a controlled-phase CP(2 theta) from mem[j] to the ancilla, giving diag(e^{-i theta}, e^{i theta}) on c exactly when mem[j]=1.
- `eq_4`: implemented; build_circuit, line commented '# eq_4' (qc.h(anc[0])). The Hadamard on the ancilla is implemented; the subsequent computational-basis measurement and postselection on c=0 are performed by the runner and are not part of the operation.
- `eq_5`: out_of_scope; no code location. Class-register measurement, postselection and the argmax vote are measurement/classical post-processing steps, excluded from the measurement-free unitary operation.
- `eq_6`: implemented; example_instance_json ({"n": 2, "num_class_qubits": 1}) and register_layout. The example instance realises the 6-qubit circuit (2 input + 2 memory + 1 class + 1 ancilla) of the tiny explicit instance; the specific training patterns/input of eq_6 are encoded in the runner-prepared input state, not in the circuit.

## Specification changes

- eq_1, eq_4, eq_5: Scope narrowed to the unitary core (eq_2, eq_3, eq_4 Hadamard). State preparation of eq_1 and the measurements/postselection/classical vote of eq_4-eq_5 are delegated to the runner. Reason: The task requires an operation without input-state preparation, measurement or classical processing.
- eq_3: The exponential of the Hamiltonian is realised gate-by-gate as P(-pi/(2n)) on each memory qubit plus CP(pi/n) from each memory qubit to the ancilla, rather than as a dense unitary. Reason: Opaque dense unitaries are disallowed; the factorisation is exact because all terms commute and each term acts as diag(e^{-i theta}, e^{i theta}) on the ancilla conditioned on the memory qubit being 1.
- eq_1, eq_6: The construction is parametrised by n (bits per pattern) and num_class_qubits (class register size, 1 for binary labels), with total qubits 2n + num_class_qubits + 1 capped at 12; the class register is idle in the operation. Reason: Generalises the fixed n=2, binary instance to varying valid instance parameters as required, while keeping the specified register order I, M, Y, c.
