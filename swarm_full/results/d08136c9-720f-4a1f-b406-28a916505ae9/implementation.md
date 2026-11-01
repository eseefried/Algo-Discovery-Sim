# Equation to Qiskit

Ancilla-assisted fanout / controlled single-qubit gate on a k-dimensional grid with nearest-neighbor interactions only. Each grid site holds one target qubit and one copy qubit. The origin site's copy qubit is the control. The control value is spread by CNOTs along a spanning tree between adjacent sites, so tree depth equals Manhattan distance. Each copy then acts locally on its target (CX, CZ or CP), and the spreading is uncomputed in reverse. Depth is O(k*side), size is Theta(n) and width is 2n. This is a small-scale, non-adaptive reconstruction of the assumed plan, not the paper's adaptive simulation result.

Source equation run: `5265f42c-b6b8-4d45-8c16-506c4e52ac87`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- n = product(shape) sites, site index idx = x0 + shape[0]*x1 + shape[0]*shape[1]*x2 + ... (first coordinate fastest)
- qubits 0..n-1: register t, target at site idx is qubit idx
- qubits n..2n-1: register c, copy qubit at site idx is qubit n+idx
- qubit n (c[0], origin site) is the control qubit and holds the original control value
- qubits n+1..2n-1 are copy ancillas; the runner must prepare them in |0>
- total qubits = 2n <= 12
- encoding: computational basis, qubit 0 least significant

## Assumptions

- Copy qubits (all c qubits except the control c[0]) are supplied in |0> by the runner.
- The control is qubit c[0] at the grid origin, and each grid site also hosts one target qubit.
- Interactions are only between grid-adjacent copy qubits, or between a site's copy and target qubits.
- The k-th root reading of 'k√n' is used.
- Spanning-tree spreading is an assumed scheme, not taken from the paper.

## Unresolved issues

- The paper's actual non-adaptive optimal circuit and its lower bound are not reconstructed.
- The adaptive simulation of arbitrary standard-model circuits is not reconstructed.
- Shor's algorithm and constant-depth claims are not addressed.
- Correctness requires the copy ancillas to start in |0>. This cannot be enforced inside a unitary circuit.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The adaptive-to-standard depth equivalence is an asymptotic theorem about classical-controller simulation. The abstract gives no construction, and the circuit here is non-adaptive.
- `eq_2`: implemented; _spread_edges and the spreading/uncompute loops in build_circuit. Control copies spread over the kD grid only between adjacent sites, in layers of increasing Manhattan distance. For a cubic shape of side about n^(1/k) with constant k, this gives depth O(n^(1/k)). The implementation is limited to at most 12 qubits, so the asymptotic claim is only structurally reflected and the lower bound is not addressed.
- `eq_3`: implemented; register layout and local-operation loop in build_circuit. The circuit uses n target qubits plus n copy qubits (width 2n = Theta(n)). The gate count is 2(n-1) spreading CNOTs plus n local gates (size Theta(n)).

## Specification changes

- eq_2, eq_3: Narrowed scope to one explicit non-adaptive ancilla-assisted fanout/controlled-gate (CX, CZ or CP) on a grid with side lengths given by the 'shape' parameter. Total qubits are capped at 12, so n <= 6. Reason: The abstract gives no gate-level construction, so the spec's assumed spread-apply-uncompute plan was implemented. The 12-qubit cap limits the size.
- eq_1: The adaptive depth-equivalence result is not implemented. Reason: No simulation mechanism is given in the abstract, and adaptivity requires mid-circuit measurement and classical control, which are not allowed.
- eq_2: The Theta(n^(1/k)) depth is realized only as O(sum of shape side lengths) for chosen shapes, not proven. No lower-bound circuit is implemented. Reason: Asymptotic statements cannot be verified by a fixed small instance.
