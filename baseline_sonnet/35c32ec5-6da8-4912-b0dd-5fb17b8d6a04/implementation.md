# Equation to Qiskit

Implements only the fanout unitary of eq_4 as a measurement-free circuit of n CNOTs from one control qubit onto n targets, with n given in the instance. The abstract gives no construction for the depth-Theta(n^(1/k)) grid circuit or the adaptive simulation, so those claims are not implemented.

Source equation run: `1cb231b2-abee-4331-9c39-5f36a38f0882`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control x (computational basis, LSB of full register)
- qubits 1..n: targets y_1..y_n (y_i on qubit i)
- no ancilla qubits; total qubits = n+1 <= 12

## Assumptions

- k-th root reading of k√n is not exercised by the code
- Fanout is a CNOT from one control to each of n targets
- Qubit 0 is the control and qubits 1..n are the targets
- The instance parameter is a single integer n with 1 <= n <= 11

## Unresolved issues

- No explicit non-adaptive nearest-neighbor kD-grid fanout circuit or ancilla layout
- No adaptive simulation construction or constant-depth Shor construction
- The generated circuit does not demonstrate the Theta(n^(1/k)) depth bound

## Equation mapping

- `eq_1`: out_of_scope; no code location. Asymptotic depth-equivalence between adaptive grid circuits and the abstract model; it needs a classical-control simulation construction that the abstract does not give.
- `eq_2`: out_of_scope; no code location. Theta(n^(1/k)) depth bound for non-adaptive grid circuits. The construction is not specified, and the generated circuit is an all-to-all fanout, not a grid-optimized one.
- `eq_3`: out_of_scope; no code location. Theta(n) size and width are stated as asymptotics of the unspecified grid construction. The generated circuit has n gates and n+1 qubits but makes no grid-locality or depth claim.
- `eq_4`: implemented; build_circuit: loop applying qc.cx(control[0], targets[i]). Fanout as a CNOT from the single control onto each of the n targets.
- `eq_5`: background; no code location. Illustrative input/output check for n=3. Input state preparation belongs to the runner; the example instance uses n=3.

## Specification changes

- eq_1, eq_2, eq_3: Scope narrowed to the fanout unitary of eq_4 only. The nearest-neighbor kD-grid layout, depth-Theta(n^(1/k)) property, adaptive simulation and ancilla workspace are not implemented. Reason: The abstract gives only asymptotic claims and no explicit construction, so a faithful grid circuit cannot be reconstructed.
- eq_4: Fanout is realized with all-to-all CNOTs sharing one control, so the depth is n in Qiskit's sequential scheduling, not the grid-optimal depth. Reason: This is the simplest circuit that implements the stated unitary without inventing an unspecified construction.
