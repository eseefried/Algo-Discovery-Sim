# Equation to Qiskit

Abstained: the specification gives only generic classical background equations (Bayes update, a generic Lieb-Robinson bound, Cramer-Rao bound) and no Hamiltonian form, couplings, geometry, Trotter scheme or circuit. Any Ising evolution circuit would be an invented construction rather than a reconstruction of the source, so no code is emitted.

Source equation run: `149b9458-1779-44f3-b70e-936a43c7e18a`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- Treating the equations as background or classical is consistent with the abstract-level specification.

## Unresolved issues

- Explicit Hamiltonian form (couplings, fields, geometry) is missing.
- Exact experiment circuits and the Trotterization or evolution scheme are missing.
- Light-cone size selection and the measurement scheme are unspecified.
- The Bayesian update algorithm and the epistemic Lieb-Robinson velocity computation are unspecified.
- No public validation contract was supplied and no instance was requested.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Bayesian posterior update is classical inference over the Hamiltonian parameters. It is not a unitary circuit operation.
- `eq_2`: background; no code location. Generic Lieb-Robinson bound that motivates restricting simulation to a light cone. It is not a gate-level construction, and the paper's exact form and constants are unknown.
- `eq_3`: background; no code location. Cramer-Rao bound relating Fisher information to the number of experiments. It is a statistical bound with no circuit realization.

## Specification changes

- eq_1, eq_2, eq_3: No circuit construction was implemented. Scope was narrowed to an abstention. Reason: None of the three equations defines a unitary operation. The Ising Hamiltonian form, geometry, parameters and evolution scheme are listed as missing information, so a device-evolution circuit cannot be reconstructed without fabricating details.
