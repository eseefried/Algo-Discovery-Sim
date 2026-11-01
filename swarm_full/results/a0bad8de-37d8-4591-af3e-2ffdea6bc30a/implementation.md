# Equation to Qiskit

Gate-model Simon's algorithm operation for n logical input qubits plus n output qubits (n<=6, so at most 12 qubits). It applies H on the input register, a CNOT-built oracle U_f|x>|y> = |x>|y XOR f(x)> with f(x) = x XOR (x_p * s), then H on the input register. Here p is the highest set bit of s, so f(x) = f(x XOR s). This is a scope narrowing: it is not the one-way five-qubit cluster-state implementation, whose geometry and measurement angles are not specified.

Source equation run: `8460b7cf-15f8-4c11-92c0-0c35255214e3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: input x bit 0 (least significant)
- qubit 1: input x bit 1
- qubit 2: output f bit 0 (least significant)
- qubit 3: output f bit 1
- General n: qubits 0..n-1 input register x, qubits n..2n-1 output register f; bit i of s acts on x bit i / f bit i
- Input state (typically |0...0>) is prepared by the runner; no measurements included

## Assumptions

- Hidden period s is supplied as an integer; bit i of s maps to input qubit i.
- s=0 is allowed and gives a one-to-one function f(x)=x.
- Input state preparation and measurement are done by the runner.
- The oracle is a representative function, not necessarily the specific functions in the experiment.

## Unresolved issues

- The one-way cluster-state implementation (graph, measurement bases, byproduct corrections) is not reconstructed.
- The mapping of physical cluster qubits to logical registers is unknown.
- The n-qubit resource analysis is out of scope.

## Equation mapping

- `eq_1`: implemented; build_circuit: oracle section (CNOT copy x->f, then CNOTs from x_p onto f_i for each set bit i of s). Oracle computes f(x)=x XOR (x_p s), which satisfies f(x)=f(x XOR s) for every x and is two-to-one when s is nonzero (one-to-one when s=0).
- `eq_2`: background; no code location. Orthogonality y.s=0 mod 2 is a property of the output distribution of the final Hadamard layer. It is not coded explicitly and is left for downstream checking.

## Specification changes

- eq_1, eq_2: Implemented the standard circuit-model (gate-based) Simon algorithm for general n<=6 instead of the five-qubit one-way cluster-state implementation. Reason: The cluster graph, measurement angles, feed-forward, and tested functions are not given, so the one-way construction cannot be reconstructed. The unitary operation realises the same logical algorithm.
- eq_1: Chose one specific oracle family, f(x)=x XOR (x_p s) with p the highest set bit of s, with 2n qubits and no auxiliary qubit. Reason: A concrete reversible oracle is needed. The specification's 2 input + 2 output + 1 auxiliary split was an assumption, and the auxiliary qubit is not needed in the gate model.
