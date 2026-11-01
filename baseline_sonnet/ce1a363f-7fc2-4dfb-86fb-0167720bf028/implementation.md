# Equation to Qiskit

Builds T steps of a coined quantum-walk search operator U = S(marked coin) on a cycle of n = 2^p nodes with one coin qubit. The coin is the d=2 Grover coin (equal to X) on unmarked nodes and -I on the marked node. The shift is a coin-controlled increment/decrement mod n. State preparation and measurement are left to the runner.

Source equation run: `95b12169-4a43-45d5-b6ee-e79c67989562`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..p-1: pos register, node index x in binary, qubit 0 least significant
- Qubit p: coin register (1 qubit); coin |0> = step +1, coin |1> = step -1
- Example (p=2): qubits 0,1 = pos; qubit 2 = coin; total 3 qubits
- Input state is prepared by the runner; the circuit applies U^T only

## Assumptions

- Node x is stored in binary on the pos qubits with qubit 0 as the least significant bit.
- Coin |0> moves the walker to x+1 and coin |1> moves it to x-1, modulo n.
- The marked node's coin is -I, as in eq_3, and U applies the marked coin first and then the shift.
- The coin operator is applied to all nodes as X, with the marked node's X cancelled and a -1 phase added.

## Unresolved issues

- The paper's graph families, twisted toroid, explicit circuits and optimal step count are not available, so this is only a generic background construction.
- The number of steps is a user parameter, and no optimal T is derived.
- Only power-of-two cycle sizes are supported.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Asymptotic gate-count claim for the twisted toroid family. It is not implemented here, and the circuit does not claim this scaling.
- `eq_2`: implemented; _marked_coin (qc.x on coin). For d=2 the Grover coin 2|s><s|-I equals Pauli X, so it is applied as an X gate on the coin qubit.
- `eq_3`: implemented; _marked_coin and _shift, repeated in build_circuit. The marked-node coin -I is obtained by cancelling X with an X controlled on pos==m and applying a -1 phase on pos==m. The shift is a coin-controlled increment/decrement built from multi-controlled X gates. One U is the coin step followed by the shift.
- `eq_4`: background; no code location. The uniform initial state is prepared by the runner, so the module contains no state preparation.
- `eq_5`: background; build_circuit loop over steps. The circuit applies U^T with T = steps. The success probability p_T is a measurement-side quantity and is not computed in the module.

## Specification changes

- eq_2, eq_3, eq_4: Narrowed the scope to a cycle with n=2^p nodes, p between 2 and 11, and d=2 with one coin qubit, rather than the generic d-regular graph. The example uses the 4-cycle (p=2). Reason: The shift must be an explicit efficient circuit. The cycle is the only graph the specification suggested, and the qubit cap is 12.
- eq_2: The Grover coin for d=2 reduces to X. Reason: 2|s_2><s_2|-I = X exactly. This coin makes the walk a poor search algorithm in general, so no amplification claim is made.
- eq_4, eq_5: Removed the Hadamard state preparation and the measurement steps from the module. Reason: The task requires an operation only, with input preparation and measurement handled by the runner.
- eq_1: Gate-count claim not implemented. Reason: The specification gives no construction for it, and it concerns a different graph family.
