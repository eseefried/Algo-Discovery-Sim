# Equation to Qiskit

Abstained. The specification supplies only the generic isometry definition and the Stinespring form as background. It does not give the paper's explicit C-not-efficient decompositions, the lower-bound formula, or the small-case optimizations. Any circuit I wrote would be an invented construction, or would hide an opaque dense unitary or a library isometry synthesis. Neither is faithful to the paper.

Source equation run: `526fbe2b-9546-4703-a3aa-36b18c808fbd`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Exact C-not lower bound formula is not given.
- The three explicit decomposition circuits and their gate counts are not given.
- Small-case optimizations are not given.
- The input format for the isometry V is not specified. A dense matrix would require an opaque unitary, which is disallowed.
- The environment register size and the POVM outcome mapping are not specified.

## Equation mapping

- `eq_1`: background; no code location. This is the standard definition of an isometry, V^dagger V = I. It is the target property and not a construction that can be coded. The decomposition that realizes V is not specified.
- `eq_2`: out_of_scope; no code location. This is the Stinespring dilation. Its use for operations and POVMs needs environment register sizes and a measurement or outcome mapping, and the specification leaves both unspecified. Tracing out the environment is also not a unitary operation.

## Specification changes

