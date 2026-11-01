# Equation to Qiskit

Abstained: the specification does not give an explicit span program for MAJ_3, the span-program-to-graph construction with weights, or how the zero-eigenvector relates to the output. It also gives no way to implement exp(iA_G) with standard gates. Any circuit would rest on invented details, so no code is produced.

Source equation run: `5c82c5df-f432-4c9c-bd05-5300f3495ed8`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Explicit span program for MAJ_3 and its weights are not specified.
- The exact span-program-to-weighted-bipartite-graph correspondence is not given.
- The relation between the start state, the zero-eigenvector and the function output is not specified.
- No method is given for implementing exp(iA_G) with standard gates without a dense unitary.
- The operation-versus-experiment boundary is unclear because the full algorithm centres on a measured phase-estimation test, and there is no public validation contract or requested instance.

## Equation mapping

- `eq_1`: background; no code location. Standard definition of the 3-majority function. It is not implemented because no circuit is generated.
- `eq_2`: background; no code location. Generic span program acceptance rule. The explicit span program for MAJ_3 is missing, so it cannot be turned into a concrete operation.
- `eq_3`: out_of_scope; no code location. The graph construction, edge weights and eigenvector structure are unspecified, and the direction of the equivalence is only an assumption. A faithful graph operator cannot be built from this.
- `eq_4`: out_of_scope; no code location. Phase estimation of exp(iA_G) needs a concrete A_G and a gate-level way to implement exp(iA_G). Neither is specified, and dense unitaries are disallowed.

## Specification changes

