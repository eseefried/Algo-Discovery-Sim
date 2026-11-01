# Equation to Qiskit

Measurement-free swap-test unitary W = (H_a)(CSWAP_{a;A,B})(H_a)(I x U_A x V_B) on 1+2n qubits (n<=5). U is H on the first qubit of A followed by a CNOT fan-out (the Bell preparation for n=2). V is U followed by an optional variant: identical, Z on qubit 0, X on qubit 0, or an explicit global phase e^{i theta}. The ancilla's P(a=0) is left for the runner to decode.

Source equation run: `7fa86105-1e23-4038-8ef0-0eb58dceb9cc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: ancilla a (swap-test control)
- qubits 1..n: register A holding U|0^n> (A[0]=qubit 1)
- qubits n+1..2n: register B holding V|0^n> (B[0]=qubit n+1)
- Little-endian Qiskit ordering; for n=2: a=q0, A=q1,q2, B=q3,q4
- Runner prepares the input |0...0>; ancilla outcome 0 is read from qubit 0

## Assumptions

- The runner prepares |0> on all qubits and decodes P(a=0) from the ancilla.
- Z/X variants act on the first qubit of B after U.

## Unresolved issues

- The paper's scalable equivalence-checking algorithms and its equivalence taxonomy are not recovered.
- Teleportation and Grover benchmark circuits are not implemented.

## Equation mapping

- `eq_1`: background; no code location. Criterion for global-phase equivalence (unit overlap); used only for decoding by the runner, not built into the circuit. The global_phase variant exercises it.
- `eq_2`: background; no code location. Swap-test probability identity that the built unitary W realizes. It is evaluated by the runner from the statevector and is not a gate itself.
- `eq_3`: implemented; build_circuit: _prep on A and B plus variant gates, then h(a), cswap loop, h(a). Direct construction of W = H_a CSWAP H_a (I x U_A x V_B), with the ancilla at qubit 0 followed by A then B.
- `eq_4`: out_of_scope; no code location. The Choi-state variant needs reference registers and is not the primary build.
- `eq_5`: out_of_scope; no code location. The Hadamard test with controlled-U and controlled-V† is a different circuit and is not built.

## Specification changes

- eq_3: n is generalized to a validated parameter 1..5 (qubit cap 12), and U is H on the first qubit plus a CNOT fan-out, which is the Bell preparation for n=2 and a GHZ preparation for larger n. Reason: The task requires varying valid parameters; the n=2 specification is recovered by the default.
- eq_3: The V variants are identical, Z on qubit 0, X on qubit 0, or an explicit global phase e^{i theta}, the last implemented as P(theta) followed by X P(theta) X on B[0]. Reason: The spec's 'U followed by Z on q0' variant is kept, and the global-phase option exercises eq_1's invariance. Only the Z variant is the spec's literal alternative.
- eq_1, eq_2, eq_4, eq_5: Scope narrowed to the state-equivalence swap test on |0^n> inputs only. The Choi-state and exact-phase Hadamard-test variants are not built. Reason: The task allows implementing one scoped construction, and the spec marks those variants as non-primary.
