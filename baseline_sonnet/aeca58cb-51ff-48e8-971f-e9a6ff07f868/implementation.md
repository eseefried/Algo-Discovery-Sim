# Equation to Qiskit

No Qiskit circuit was generated. The specification describes a classical compilation and optimization flow (ULB size selection by weighted latency, DAG scheduling with routing delays, force-directed scheduling). It defines no quantum register, unitary operation, initial state or gate-level construction, so there is nothing to implement as a measurement-free unitary build_circuit(instance).

Source equation run: `cce47a62-b94a-449f-9803-00a2b4a5ce4b`

Generation: **unsupported**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- The task requires a unitary quantum operation, which the supplied specification does not define.
- The abstract provides no formal equations. All equations in the spec are inferred or generic background.

## Unresolved issues

- The ULB definition and architecture model are not given.
- The FT code and operation latency model L(o,s) are not given.
- The modified force-directed scheduling formulas, placement cost function and routing algorithm are not given.
- No quantum operation or register layout is specified, so a build_circuit contract cannot be met.
- No public validation contract was supplied.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Classical frequency-weighted latency sum for ULB size selection. It has no unitary or qubit-level meaning. The latency model L(o,s) and the weighting are also unspecified.
- `eq_2`: out_of_scope; no code location. Classical argmin over candidate ULB sizes. It is not a quantum operation.
- `eq_3`: out_of_scope; no code location. Classical precedence constraint with routing latency in a scheduling DAG. The routing latency depends on an unspecified placement and architecture model.
- `eq_4`: background; no code location. Standard makespan definition for DAG scheduling. It is context only and not a circuit construction.
- `eq_5`: background; no code location. Classical force-directed scheduling force. The paper's modified version is unspecified, and it does not correspond to any quantum gate sequence.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5: Abstained from implementation. No equation was turned into a quantum circuit. Reason: The specification is a classical mapping, scheduling and optimization problem with no quantum registers, initial state or unitary. Any circuit would be fabricated and would not preserve the meaning of the construction.
