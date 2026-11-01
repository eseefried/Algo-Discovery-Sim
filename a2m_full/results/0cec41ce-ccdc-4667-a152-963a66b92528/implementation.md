# Equation to Qiskit

Qiskit implementation of the Trugenberger-style Hamming-distance interference stage for classification. It acts on a supplied pattern|label memory state: X gates XOR the classical query into the pattern register, H on the ancilla, controlled phases CP(-pi/n) from the ancilla onto each pattern qubit, then H on the ancilla. For a pattern at Hamming distance d, the ancilla then reads 0 with probability cos^2(pi d/(2n)). The training-state loading (eq_1) and the classical post-selection/vote (eq_5) are outside the circuit.

Source equation run: `47b05809-ca72-46a5-aa49-6a0e3c5c5af6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: pattern register p (p_j on qubit j, little-endian; becomes XOR/difference register)
- qubits n..n+m-1: class label register c (untouched by the circuit, carries class labels from the prepared memory state)
- qubit n+m: interference ancilla a (expected |0> on input; post-select a=0)
- Example n=2,m=1: p0=q0, p1=q1, c0=q2, a=q3

## Assumptions

- Input state has the ancilla in |0> and p, c holding sum_k |p_k>|c_k> with p_j on qubit j
- query[j] is the bit compared against qubit j of the pattern register
- m may be 0 or more; label qubits are only included for layout and are idle
- n+m+1 <= 12

## Unresolved issues

- The paper's actual loading procedure, decision rule and measurement or amplification scheme are unknown
- Training-set loading is not part of this circuit, so a separate preparation is needed to reproduce the full classifier
- MNIST preprocessing is out of scope

## Equation mapping

- `eq_1`: background; no code location. Training superposition is the input memory state. The runner prepares it on p and c, with a in |0>, so the circuit does not load it.
- `eq_2`: implemented; build_circuit: X gates on p[j] where query[j]==1. XOR with the classical query, no extra XNOR layer, so the Hamming weight of p is d_k.
- `eq_3`: implemented; build_circuit: first H on a and the cp(-pi/n, a, p[j]) loop. Gives the a=1 branch the phase exp(-i*pi*d_k/n).
- `eq_4`: implemented; build_circuit: final H on a. The closing Hadamard gives P(a=0|k)=cos^2(pi d_k/(2n)); no measurement is included.
- `eq_5`: out_of_scope; no code location. Post-selection on a=0, class tally and argmax are classical post-processing; the circuit has no measurement.

## Specification changes

- eq_3, eq_4: Fixed the per-qubit controlled-phase angle at -pi/n, ignoring eq_3's alternative half-angle (pi/(2n)) conventions. Reason: Only a relative phase pi*d/n yields P(a=0)=cos^2(pi d/(2n)) as in eq_4. The half-angle variants in the eq_3 text would give cos^2(pi d/(4n)) and are inconsistent with eq_4.
- eq_1: Scope narrowed to the distance-imprinting/interference operation acting on a supplied memory state. The state-loading circuit is not implemented. Reason: The task requires the circuit to be an operation on runner-prepared inputs, and the paper's loading scheme is unspecified.
- eq_5: Measurement, post-selection and the class vote are excluded. Reason: The circuit must be measurement-free and unitary.
- eq_2: The query is a classical parameter in the instance, so the x register is dropped and loaded by X gates. Reason: Matches the specification, which uses a classical query; qubit j of p corresponds to query[j] (little-endian).
