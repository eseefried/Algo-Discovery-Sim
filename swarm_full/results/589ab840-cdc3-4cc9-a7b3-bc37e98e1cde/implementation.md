# Equation to Qiskit

Abstained. The only supplied equation (eq_1) is an inferred scalar threshold condition, not a unitary construction. The gate error models (systematic, random, combined), the threshold form epsilon_th(N), and the exact circuit are all missing, so any circuit would be invented rather than reconstructed.

Source equation run: `325ab114-719b-4dce-b35f-1d44a995d13b`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Explicit gate error models (systematic, random, combined) are not given.
- The functional form of epsilon_th(N) is not given.
- Exact circuit and register sizes are not given. The spec assumes a textbook Shor layout.
- Reversible modular exponentiation for a given a and N is not specified. Implementing it would need arithmetic circuits that the spec does not describe.
- Measurement and success criteria are outside the scope of a measurement-free operation.
- A scoped ideal Shor circuit could be built, but it would not be tied to any supplied equation and would discard the error-robustness content that is the paper's subject.

## Equation mapping

- `eq_1`: out_of_scope; no code location. eq_1 is an abstract-inferred inequality, epsilon < epsilon_th(N), with unknown functional form. It is a success criterion and cannot be implemented as a circuit operation. Neither the error models nor the threshold are specified.

## Specification changes

