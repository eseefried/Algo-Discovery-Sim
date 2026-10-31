# Equation to Qiskit

Trotterized continuous-time quantum-walk search on the n-dimensional hypercube (N=2^n), approximating exp(-i t H) for H = gamma(D - A) - |w><w|. The graph term is a layer of RX rotations and the oracle term is a phase on the marked basis state. Perturbation theory is background analysis and is not implemented.

Source equation run: `0e327e21-7e19-471d-a1fb-d074c0f9ef58`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex label of the hypercube, qubit q = bit q of the vertex index (qubit 0 least significant)
- Marked vertex w is given as an integer bitstring in the same encoding
- No ancilla qubits; total qubits = n <= 12

## Assumptions

- Hypercube graph with N=2^n vertices and vertex-basis encoding with qubit q as bit q.
- Laplacian convention L = A - D, so H = gamma(D-A) - |w><w|.
- Input state preparation (for example uniform superposition) and measurement are done by the runner and are not part of this operation.
- Lie-Trotter ordering within each step is the graph layer followed by the oracle phase.

## Unresolved issues

- The abstract does not specify the graphs, weights, or the growing-dimension case, so the paper's actual constructions are not reproduced.
- Optimal gamma and evolution time are not specified and are left to the instance.
- Trotter error is not controlled or quantified by this module.

## Equation mapping

- `eq_1`: implemented; build_circuit (RX layer for the graph term) and _oracle_phase (oracle term). Search Hamiltonian restricted to the hypercube graph and simulated by first-order Trotterization with trotter_steps steps. The graph term uses RX rotations, the oracle uses a multi-controlled phase, and the constant degree shift is a global phase.
- `eq_2`: background; no code location. Degenerate perturbation theory is an analytical tool for estimating the dynamics and is not a circuit operation, so it is not implemented.

## Specification changes

- eq_1: Narrowed the graph to the n-dimensional hypercube (N=2^n) and fixed the Laplacian sign convention so that -gamma*L = gamma*(D-A) with L = A-D. This is positive semidefinite and the uniform state has energy 0. Reason: The specification gave no graph, and the sign of L is ambiguous in the text. The chosen convention is the standard CTQW search one, and the hypercube is exactly decomposable into single-qubit rotations.
- eq_1: The exact evolution exp(-iHt) is replaced by a first-order Lie-Trotter product with a user-chosen number of steps, so the circuit is approximate. gamma, time, marked vertex and step count are instance parameters. Reason: The graph and oracle terms do not commute, so exact implementation as standard gates is not available, and the abstract gives no values for gamma or t.
- eq_2: Perturbation theory is not implemented, and the weighted self-loop reduced graphs are not constructed. Reason: They are analysis tools rather than a unitary operation, and the abstract gives no specifics.
