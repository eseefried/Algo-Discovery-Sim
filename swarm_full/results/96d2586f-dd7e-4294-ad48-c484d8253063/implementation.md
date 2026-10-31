# Equation to Qiskit

Abstained: the abstract and specification do not give the RUS synthesis algorithm, the joint Clifford+T circuit, the success/failure outcomes or the correction step. Any circuit I wrote would be an invented generic RUS skeleton, not the paper's construction, so no code is emitted.

Source equation run: `ab0636d5-9012-43da-8a9e-4bd1290ccef7`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- No assumptions were made about the RUS circuit structure, because adding any would change the scientific content.

## Unresolved issues

- The RUS synthesis algorithm and its classical runtime are not specified.
- The joint data/ancilla Clifford+T gate sequence is not specified.
- The success/failure outcome convention and the correction or restart procedure are not specified.
- Mid-circuit ancilla measurement and repeat-until-success control are dynamic and conflict with the required measurement-free unitary output, so a faithful implementation would need a deterministic scope such as one attempt with a post-selected ancilla.
- The distance metric d and the test distribution behind the 2.5 average are not specified.

## Equation mapping

- `eq_1`: background; no code location. This is a classical T-count lower bound for ancilla-free synthesis, 3*log2(1/epsilon). It is a comparison benchmark, not a unitary operation, so there is nothing to implement.
- `eq_2`: background; no code location. This is a reported numerical average ratio (about 2.5) of expected T-count. It is a statistical result about synthesized circuits, not an operation, and it cannot be reproduced without the synthesis algorithm.
- `eq_3`: out_of_scope; no code location. This approximation criterion needs the unspecified synthesized circuit and an unspecified distance metric. It is a verification criterion for software, not a gate-level construction, and there is no fixed circuit to check it against.

## Specification changes

- eq_1, eq_2, eq_3: Narrowed scope to no implementation: abstained instead of building a circuit. Reason: The abstract gives only the problem statement and a numerical claim. The RUS synthesis algorithm, circuit structure, ancilla measurement convention, correction operation and distance metric are all missing. A generic Clifford+T RUS skeleton would be fabricated and would not match the paper.
