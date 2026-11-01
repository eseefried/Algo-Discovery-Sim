# Equation to Qiskit

Abstained: the specification does not define generalized extreme channels, the nonlinear coupled equations, or the per-channel circuit construction. Any circuit would rest on invented structure, and a random mixture of channels cannot be written as one unitary, measurement-free circuit without inventing a mechanism for the randomness.

Source equation run: `44a4adb9-e3ac-4fd0-95c9-45141057079b`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Definition of generalized extreme channels is not given.
- The nonlinear coupled algebraic equations and the optimization procedure are not given.
- The circuit for each generalized extreme channel (the system plus single ancilla qudit unitary) is not given.
- The role and number of classical dits is unspecified.
- It is unclear how random selection of a circuit should be represented in a single measurement-free unitary build_circuit(instance).
- No instance or validation contract was supplied.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The convex decomposition needs the definition of generalized extreme channels and the classical optimization that produces the weights p_k and channels E_k. Neither is given, so the decomposition cannot be implemented faithfully.
- `eq_2`: out_of_scope; no code location. The diamond-norm tolerance is a classical accuracy criterion on the decomposition. It is not a gate-level operation, and checking it would require simulation or verification, which is excluded from the generated module.
- `eq_3`: out_of_scope; no code location. Sampling circuit k with probability p_k needs classical randomness and a dynamic or externally chosen circuit. It also needs the unspecified circuits for each E_k. A single unitary build_circuit cannot realize this without invented structure.
- `eq_4`: background; no code location. This is the standard definition of the diamond norm. It is background for the error criterion and has no circuit counterpart.

## Specification changes

- eq_1, eq_2, eq_3: No implementation was produced. The scope was narrowed from the convex-decomposition and random-sampling structure to nothing. Reason: The definition of generalized extreme channels, the optimization equations, the per-channel circuit and the role of the classical dits are all missing. Implementing any of them would fabricate the construction instead of reconstructing it.
