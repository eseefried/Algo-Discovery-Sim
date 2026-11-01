# Equation to Qiskit

Qiskit circuit for t steps of the Grover-coined flip-flop discrete-time quantum walk U=S*C on the plain 4-cycle. A 2-qubit node register and a 2-qubit arc/coin register are used. The coin is X on the coin LSB for c in {0,1} and identity on padding c=2,3. The shift is a controlled increment or decrement of the node followed by a coin flip. It uses only X, CX and multi-controlled X gates, with no dense unitaries and no state preparation.

Source equation run: `7cf51438-ede9-4d50-b7b1-a5013bccb59f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pos bit 0 (LSB of node v in {0..3})
- qubit 1: pos bit 1 (MSB of node v)
- qubit 2: coin bit 0 (LSB of arc label c; c=0 arc to v+1, c=1 arc to v-1)
- qubit 3: coin bit 1 (MSB of c; c=2,3 are padding states left unchanged)
- Basis state |v,c> has Qiskit integer index v + 4*c; initial state |v=0,c=0> is |0000>, prepared by the runner
- Antipodal node 2 corresponds to qubit1=1, qubit0=0

## Assumptions

- Node index v uses qubits 0-1 and arc label c uses qubits 2-3, both in little-endian binary.
- Label convention: c=0 is the arc to v+1 mod 4 and c=1 is the arc to v-1 mod 4.
- The Grover coin is assumed to be one of the paper's three coins (unverified).
- The step order is U = S C, with the coin applied first and then the shift.
- Unknown instance keys are rejected with ValueError.

## Unresolved issues

- The specific C4/C6/C8 modifications that preserve PST are not specified in the abstract and are not implemented.
- The paper's other two coin operators and its exact shift definition are unknown.
- The plain C4 walk is trivially ballistic, so this instance does not reproduce the nontrivial modified-graph results.

## Equation mapping

- `eq_1`: background; no code location. Initial arc state |0,0> is the all-zero state, prepared by the runner. The circuit contains no state preparation.
- `eq_2`: implemented; _coin. G_2 equals X, applied on coin qubit 0 controlled on coin qubit 1 being 0, with identity on the padding labels c=2,3. The same coin acts at every node because it has no position control.
- `eq_3`: implemented; _shift. Flip-flop shift as a controlled mod-4 increment (c=0) or decrement (c=1) of the node register, followed by a coin-label flip on the used subspace. Padding states are untouched.
- `eq_4`: implemented; build_circuit. Repeats the coin step (_coin) followed by the shift step (_shift) t times to give U^t with U=SC.
- `eq_5`: out_of_scope; no code location. The antipodal probability P_t is external post-processing of the simulated state. The circuit has no measurements.

## Specification changes

- eq_2, eq_3, eq_4: The unitary is compiled directly into X, CX and multi-controlled X gates instead of building an explicit 16x16 matrix and then compiling it. Reason: The task forbids dense or opaque unitaries. The gate-level construction represents the same permutation and coin operators.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to the plain unmodified C4 with the Grover coin and flip-flop shift. The only instance parameter is the integer steps t in 0..64. Reason: The abstract does not specify the modified graphs, the other coins, or the larger graph families, so they cannot be built faithfully.
