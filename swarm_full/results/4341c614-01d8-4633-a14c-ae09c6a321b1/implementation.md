# Equation to Qiskit

Abstained: the abstract does not define the QPA unitary U (its form and theta dependence), the encoding of the length-5 binary input into the particle state, the number of evolution steps, the position-space dimension, or the GA-found boundary partition. Any circuit would rely on invented details, so no code was generated.

Source equation run: `e306ca7c-b147-4306-89e5-001b8a4f6050`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Exact form of U and its dependence on theta is not given.
- Encoding of the length-5 binary input into the initial QPA state is not given.
- Position-space dimension and qubit register layout are not given.
- Number of evolution steps t is not given.
- The GA-found boundary partition is not given.
- No public validation contract or requested instance was supplied to narrow the scope.

## Equation mapping

- `eq_1`: background; no code location. The evolution |psi_t> = U^t |psi_0> is an assumed generic model. U is not specified, so it cannot be turned into a gate sequence without fabricating the operator.
- `eq_2`: out_of_scope; no code location. The decision rule is a measurement-probability and classical post-processing step that depends on the unknown boundary partition. It is not part of a measurement-free unitary operation.

## Specification changes

