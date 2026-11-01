# Equation to Qiskit

Abstained: the abstract and specification give only asymptotic running-time bounds (classical O(n^3), trivial quantum O~(n^2.5), target O(n^{2.5-epsilon})). They give no circuit, oracle model, register encoding or structure-exploiting subroutine. Any circuit would be an invented generic Grover skeleton rather than the paper's construction, so no code is produced.

Source equation run: `00244d4b-ba1a-4c03-9e6c-7ff15e44dac6`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Concrete quantum algorithms and subroutines for each APSP variant are not specified.
- The oracle model (adjacency list or matrix) and its gate-level implementation are not specified.
- The register sizes and encoding for vertices, weights and work ancillas are not specified.
- The value of epsilon for each variant is not given.
- No public validation contract was supplied to define a narrower, well-posed circuit target.

## Equation mapping

- `eq_1`: background; no code location. Classical O(n^3) baseline complexity. It is a runtime statement, not a unitary operation, so there is nothing to implement.
- `eq_2`: background; no code location. Trivial Grover-based O~(n^2.5) quantum complexity. It is context for the paper's improvement. An implementation would need an unspecified graph oracle and minimum-finding routine.
- `eq_3`: out_of_scope; no code location. O(n^{2.5-epsilon}) is the target complexity of the paper's algorithms. The abstract does not describe those algorithms, so no gate-level construction can be reconstructed.

## Specification changes

- eq_1, eq_2, eq_3: No construction was implemented. The scope was narrowed to none, and no code was generated. Reason: All supplied equations are complexity bounds. The registers, oracle and measurement in the specification are generic assumptions, not content from the source, so an implementation would not preserve the paper's meaning.
