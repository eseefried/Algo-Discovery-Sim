# Equation to Qiskit

Implements the scoped dA=dB=2 instance P = CNOT(A->B) = |0><0|(x)I + |1><1|(x)X. Mode 'direct' is a single CNOT on 2 qubits. Mode 'teleport' is a measurement-free, gate-teleportation-style non-local CNOT on 4 qubits: a Bell pair is shared across the A|B cut, and the classical corrections are made coherent so both ancillas return to |0>.

Source equation run: `3ab650c6-99d8-4901-bb8f-85d9caa4d1a9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- direct mode (2 qubits): q0 = A (control, data), q1 = B (target, data)
- teleport mode (4 qubits): q0 = A (Alice data), q1 = B (Bob data), q2 = e0 (Bell-pair ancilla on Alice's side), q3 = e1 (Bell-pair ancilla on Bob's side)
- Encoding: computational basis, qubit index 0 is least significant; |a> on q0 means a in {0,1}; ancillas q2,q3 must be |0> on input and return to |0>

## Assumptions

- Ancillas e0,e1 are supplied in |0> by the runner in teleport mode
- Qubit placement: e0 on Alice's side, e1 on Bob's side of the A|B cut
- Local gates are free; cost is counted in cut-crossing two-qubit gates
- Default mode is 'teleport' if mode is omitted

## Unresolved issues

- The general nonnegative-rank protocol and its CNOT-cost relation to r_+ are not reconstructed
- The coherent version is not cheaper than the direct CNOT; it demonstrates the structure only

## Equation mapping

- `eq_1`: background; no code location. Operator-Schmidt decomposition; for CNOT, r=2 with terms |0><0|(x)I and |1><1|(x)X. Not computed in code, only motivates the instance.
- `eq_2`: background; no code location. Communication-matrix reshaping and rank relation; no classical postprocessing in the circuit module.
- `eq_3`: out_of_scope; no code location. Nonnegative factorization and r_+ protocol are not implemented; the general protocol is not specified in the abstract.
- `eq_4`: implemented; build_circuit: 'direct' branch (qc.cx(0,1)) and the 'teleport' branch, which realizes the same operator on A,B. CNOT_{A->B} = |0><0|(x)I + |1><1|(x)X on one qubit per side.
- `eq_5`: implemented; build_circuit: 'teleport' branch (final cz/h gates uncompute e1 and e0). The circuit is constructed so that W|a,b,00_anc> = |a, b xor a>|00_anc>. Verification is left to the runner.

## Specification changes

- eq_4, eq_5: The coherent teleportation-style CNOT uses three cut-crossing two-qubit gates (Bell-pair CX e0->e1, coherent correction CX e0->e1, and CZ(A,e1)) instead of one CNOT. Bell-pair prep is counted as the ebit resource and the other two are the coherent versions of the classically-controlled corrections. Reason: Measurement-free unitary implementation requires coherent corrections, which cross the cut; the 1-CNOT cost of a direct CNOT is retained in the 'direct' mode.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to dA=dB=2 with P=CNOT; general permutations, r_+ protocol, and nonnegative factorization are not implemented. Other dimensions raise ValueError. Reason: The abstract does not specify the general protocol; only the toy instance can be built faithfully.
- eq_5: The spec's 'flag' and 'reverse round' uncompute is realized as H-CZ-H on e1 and H on e0, not a literal reverse of the forward round. Reason: This is the shortest coherent way to return both ancillas to |0>.
