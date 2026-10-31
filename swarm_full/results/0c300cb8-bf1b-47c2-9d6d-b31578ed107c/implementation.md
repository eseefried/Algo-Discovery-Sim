# Equation to Qiskit

Scoped to the Trugenberger-style Hamming-distance interference operation on registers prepared by the runner. A Hadamard goes on the control qubit. CNOTs write x XOR p into the memory register. A controlled phase of pi/n per differing bit follows, so the control=1 branch picks up exp(i*pi*d_H/n). The XOR is optionally undone and a final Hadamard goes on the control, giving P(control=0)=cos^2(pi*d_H/(2n)) for each memory branch. Memory superposition preparation, MNIST encoding, measurement and majority voting are excluded.

Source equation run: `43ee3bdf-f699-44a9-8d6a-13fad38786dc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: input register (x_i at qubit i, little-endian, runner-prepared)
- qubits n..2n-1: memory register (pattern p_k bit i at qubit n+i, runner-prepared superposition)
- qubit 2n: control ancilla (starts |0>)
- example n=3: input q0-q2, memory q3-q5, control q6

## Assumptions

- The control-qubit interference template follows the Trugenberger style: H, XOR, controlled phase proportional to d_H, H.
- Phase per differing bit is pi/n.
- Little-endian layout; input bit i is at qubit i and memory bit i at qubit n+i.

## Unresolved issues

- The authors' modifications to Trugenberger's algorithm are unknown.
- Class label storage and the final decision rule are not implemented.
- The MNIST encoding and shot count are unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit: CNOT loop computing x XOR p into memory, then controlled-phase loop cp(pi/n) from the control onto each memory qubit. The bitwise XOR is computed in the memory register. The sum over i of the XOR bits is realized as a total phase exp(i*pi*d_H/n) on the control=1 branch.
- `eq_2`: background; no code location. The uniform memory superposition is an input state, so the runner prepares it. The operation acts linearly on any memory state.

## Specification changes

- eq_2: Memory superposition preparation is not included in the circuit; the circuit is only the Hamming-distance interference operation acting on prepared registers. Reason: Task rules forbid input-state preparation inside build_circuit.
- eq_1: The abstract gives no phase angle, so a per-differing-bit phase of pi/n was chosen. The XOR is uncomputed by default (configurable) so the memory register retains p_k. Reason: The abstract does not give gate details. This choice makes P(control=0)=cos^2(pi*d_H/(2n)), which is 1 at d_H=0 and 0 at d_H=n.
- eq_1, eq_2: Measurement, post-selection, class labels, MNIST binarization and majority-vote postprocessing are out of scope. Pattern length is capped at n<=5 (2n+1<=12 qubits). Reason: These are not specified in the abstract. The operation must be measurement-free and respect the 12-qubit cap.
