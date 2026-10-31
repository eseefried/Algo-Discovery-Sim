# Equation to Qiskit

Abstained: the specification contains only an asymptotic expected-gate-count scaling (eq_1) and no explicit unitaries, ancilla counts, measurement-outcome transition rules, fallback rules, or definition of b. A faithful unitary, measurement-free Qiskit operation cannot be built without fabricating these details.

Source equation run: `da0df690-d948-4db8-8e7c-cb226fae4d88`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Unresolved issues

- Definition of b for each gate set is missing.
- Explicit multi-qubit unitaries per Markov chain state are missing.
- Ancilla count and per-transition step structure are missing.
- Outcome-to-transition mapping and fallback rules are missing.
- Finite termination bound is missing.
- The protocol is inherently dynamic (measurement plus classical control), which conflicts with the measurement-free unitary requirement.
- No public validation contract or requested instance was provided.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Asymptotic expected-gate-count scaling of the PQF protocol. It is a cost statement, not a unitary construction, and cannot be implemented as a circuit. The underlying protocol requires measurements and classical control, which are excluded from the unitary-only output.

## Specification changes

- eq_1: No circuit implemented; scope narrowed to abstention. Reason: The PQF protocol needs mid-circuit measurement and classical feed-forward, which are disallowed here. Its multi-qubit unitaries, Markov chain transitions, and fallback rules are also not specified, and no validation contract or instance was supplied.
