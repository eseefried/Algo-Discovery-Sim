# Equation to Qiskit

No circuit generated. The specification gives only standard Krylov/Lanczos background and a generic statement of reduced dynamics. It does not fix any Hamiltonian, graph, marked vertex, hopping rate, oracle form, seed state, qubit encoding, evolution time or observable. No public validation contract narrows the scope. Any circuit would need those choices invented here. It would also have to approximate e^{-iHt} (for example by Trotterization), which the abstract does not describe.

Source equation run: `43ce1b75-75b4-49e7-9d71-d2430819ab8a`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- No specific graph Hamiltonian is given (adjacency or Laplacian, graph family, size, broken links, hopping rate).
- The oracle or marked-vertex term is not specified.
- The seed state and the mapping from vertices to qubits are not specified.
- The evolution time is not given and no gate-level or exact synthesis of e^{-iHt} is specified.
- The transport efficiency and sink model are not defined, and the XY spin-chain fidelity bound is not defined.
- No public validation contract was supplied to fix the scope.

## Equation mapping

- `eq_1`: background; no code location. Definition of the Krylov invariant subspace used by the Lanczos method. It is a classical analysis tool, not a gate-level operation.
- `eq_2`: background; no code location. The Lanczos three-term recurrence is a classical procedure that tridiagonalizes H. Its coefficients depend on an unspecified H and seed, so there is nothing to implement as a circuit.
- `eq_3`: out_of_scope; no code location. Evolution under e^{-iHt} requires a concrete H, t and encoding, none of which are given. Building it would mean choosing a specific search Hamiltonian and an approximate decomposition, which the specification does not support.

## Specification changes

