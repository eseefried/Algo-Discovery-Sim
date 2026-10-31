# Equation to Qiskit

Abstained: the specification describes a classical exact-synthesis compilation algorithm for single-qubit Clifford-cyclotomic unitaries. The abstract gives no reduction rule, size measure, or input encoding for the matrix U. Any circuit I wrote would be an invented gate-word builder, not the paper's construction, so I return no code.

Source equation run: `ca526c3d-f211-49b8-96fe-a714533ce0d8`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- The abstract gives no concrete reduction rule or size measure for the generalized KMM synthesis.
- The exceptional values of n where the ring characterization fails are not stated.
- Mapping an input unitary U to a circuit needs the classical synthesis algorithm, which is not specified.
- A trivial builder that applies a user-supplied Clifford and Rz(pi/n) word would not reconstruct the paper's synthesis, so it was not written.

## Equation mapping

- `eq_1`: background; no code location. This defines the gate set (Clifford plus Rz(pi/n)) that the synthesis output is expressed in. The algorithm that produces gate sequences over this set is classical and its details are not supplied, so no circuit construction was implemented from it.
- `eq_2`: background; no code location. This is the ring Z[e^{i pi/n},1/2] used for classical arithmetic on matrix entries and for the characterization of exactly synthesizable unitaries. It is not a quantum operation.

## Specification changes

