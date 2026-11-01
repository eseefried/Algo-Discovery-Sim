# Equation to Qiskit

Builds the ideal three-qubit Deutsch-Jozsa operation H^3 · U_f · H^3 on q0..q2 with no ancilla and one oracle query. U_f is synthesized from a user-supplied 8-entry truth table through its algebraic normal form (Moebius transform), using Z, CZ and CCZ gates plus a global phase for the constant term. The input state, measurement and class readout are left to the runner.

Source equation run: `20be2a71-79ce-43df-83e4-cd455a06dad3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = least significant bit x0 of the function input (data qubit)
- q1 = bit x1 (data qubit)
- q2 = bit x2 (data qubit)
- No ancilla; the runner prepares |000> and measures, and the output string s reads s2 s1 s0 in Qiskit order

## Assumptions

- Basis index x = x0 + 2*x1 + 4*x2, with qubit i holding x_i (Qiskit little-endian).
- Qutrit and cavity hardware are abstracted to ideal qubits.
- Exactly one oracle query and no ancilla.
- truth_table entries are integers 0 or 1; booleans are accepted.

## Unresolved issues

- The paper's explicit gate sequences for the 35 f-controlled phase gates are not reproduced.
- The refined-DJ discrimination criterion among the 35 functions is not specified.
- The two-target controlled-phase gate and the qutrit/cavity pulse details are not modeled.

## Equation mapping

- `eq_1`: implemented; build_circuit: ANF-based Z/CZ/CCZ oracle block (between the two Hadamard layers). The diagonal +-1 phase oracle is realized from the truth table, with entry (-1)^f(x) on |x>.
- `eq_2`: implemented; build_circuit: the two Hadamard layers (include_hadamards=True). H^3 U_f H^3 is built, so the amplitude on |s> starting from |000> is F_hat(s). The initial state is supplied by the runner.
- `eq_3`: background; no code location. The constant-vs-balanced decision rule is a consequence of eq_2 and is not coded.
- `eq_4`: implemented; _anf and the ANF loop in build_circuit. The Moebius transform gives a_S. Each S with a_S=1 yields Z (|S|=1), CZ (|S|=2) or CCZ (|S|=3), and the empty set gives a global phase of pi.
- `eq_5`: out_of_scope; no code location. Class readout is classical post-processing of measurement results. The circuit has no measurement.

## Specification changes

- eq_1, eq_4: The opaque oracle placeholder is made concrete as a user-supplied 8-entry truth table over 3 bits, synthesized by ANF. Only 3 qubits are supported. Reason: A parameterized, non-opaque, unitary circuit requires an explicit f. The paper's own sequences for the 35 gates are not available.
- eq_4: A standard CCZ replaces the paper's two-target controlled-phase hardware gate. The constant ANF term is applied as a circuit global phase. Reason: The hardware gate definition is missing. The global phase makes the operator exactly equal to the ideal U_f.
- eq_2: The returned operation contains the Hadamard layers by default. An optional include_hadamards=False returns only U_f. Reason: The scoped operation is the full DJ unitary H^3 U_f H^3 with no state preparation.
- eq_5: Measurement and Walsh-class readout are excluded from the circuit. Reason: The circuit must be measurement-free.
