# Equation to Qiskit

Abstained: the specification does not fix the algorithm (phase estimation vs variational), the HeH+ qubit Hamiltonian coefficients or mapping, the circuit structure, or the register sizes. Any circuit would rest on invented chemistry data. No public validation contract or requested instance was supplied to narrow the scope.

Source equation run: `5f1a64bc-d954-4f96-ab98-069a241022e1`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Algorithm used (phase estimation vs variational) is unknown.
- HeH+ minimal-basis Hamiltonian coefficients and qubit mapping at each bond distance R are not given.
- Number of system and ancilla qubits and the circuit details are unspecified.
- No public validation contract or instance was provided to define a concrete operation.
- How the 1e-14 Hartree uncertainty is defined and obtained is unspecified.

## Equation mapping

- `eq_1`: background; no code location. The variational ground-state energy definition is standard background. It is not a concrete unitary operation, and the Hamiltonian H(R), the ansatz and the algorithm are unspecified, so nothing can be implemented faithfully.
- `eq_2`: out_of_scope; no code location. The reported 1e-14 Hartree uncertainty is an experimental result and not a circuit operation. It cannot be encoded in a unitary circuit.

## Specification changes

- eq_1, eq_2: No construction was implemented. The scope was narrowed to an empty artifact. Reason: The essential details (algorithm, Hamiltonian coefficients, qubit mapping, circuit steps) are missing from the specification, and inventing them would fabricate scientific content.
