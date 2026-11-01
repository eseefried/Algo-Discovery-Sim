# Equation to Qiskit

Abstained: the specification gives no explicit Clifford+T circuit W, no gate sequence, and no failure-correction scheme, so no single well-defined RUS operation can be implemented without inventing the paper's construction. The abstract only motivates the problem and gives T-count figures, which are classical cost statements. The measurement and restart parts of an RUS protocol are also excluded from a unitary, measurement-free circuit.

Source equation run: `5a3c35cf-3741-466a-9de5-66524ded06c1`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- No assumption can fix the missing W, so none was made. Choosing a specific known RUS gadget would replace the paper's synthesis algorithm with an invented construction.

## Unresolved issues

- The explicit RUS circuit W (Clifford+T gate sequence on data and ancilla) is not given.
- The failure-correction or restart scheme is not specified, and it would require dynamic circuits.
- The synthesis algorithm that maps a target U and precision epsilon to W is absent.
- The error metric and global-phase convention are unspecified.
- No public validation contract or requested instance was supplied to narrow the scope.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Classical lower-bound formula for ancilla-free T-count. It is a cost benchmark, not a quantum operation.
- `eq_2`: out_of_scope; no code location. Empirical average ratio of expected T-counts, taken from the paper's numerics. It is not a circuit construction.
- `eq_3`: background; no code location. Generic RUS success-branch structure. It needs a specific W and a mid-circuit measurement, and W is not specified. The measurement and branching are also not allowed in the unitary output.
- `eq_4`: out_of_scope; no code location. Approximation-precision criterion. It would be checked classically after synthesis, and the norm and phase convention are unspecified.
- `eq_5`: background; no code location. Geometric-repetition expectation for the T-count. It is classical cost accounting and needs dynamic repetition, which is excluded.

## Specification changes

