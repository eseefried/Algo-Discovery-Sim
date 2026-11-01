# Equation to Qiskit

Abstained: no circuit was generated. The specification gives only abstract-level claims (a 2/|G| success probability and the problem statements). It does not give the optimal probe state, the oracle construction, the representation, or the discrimination POVM. Any Qiskit circuit would therefore be an invented construction rather than a reconstruction.

Source equation run: `0de25047-722c-41f3-887d-caaa0414286e`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Explicit construction of the optimal probe state is not given.
- The oracle definition and its circuit-level realization are not given for group multiplication or for hidden conjugation.
- The representation of G (and hence the qubit encoding and dimension, which must stay within 12 qubits) is not specified.
- The explicit discrimination POVM and its unitary dilation are not given.
- No public validation contract or instance was supplied, so the scope cannot be narrowed to a concrete group, such as Z_2 (Deutsch) or a specific small group.

## Equation mapping

- `eq_1`: background; no code location. eq_1 is a claimed optimal single-query success probability, 2/|G|, for the product of two group elements. It is a performance claim, not an operation to implement. It could only be checked against a circuit that is not specified here.

## Specification changes

