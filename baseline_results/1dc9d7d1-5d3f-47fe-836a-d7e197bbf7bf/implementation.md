# Equation to Qiskit

Qiskit module implementing the refined (ancilla-free) three-qubit Deutsch-Jozsa operation H^{x3} U_f H^{x3}, where the f-controlled phase oracle U_f|x> = (-1)^{f(x)}|x> is built from the algebraic normal form of f as a product of single-qubit Z gates, two-qubit CZ gates and (optionally merged) one-control/two-target CZ gates, exactly as the abstract's gate set prescribes. f is specified either by ANF coefficients or by a truth table (converted by a GF(2) Moebius transform); functions with cubic or higher ANF terms are rejected because they lie outside the Z/CZ/two-target-CZ gate set. Hadamard layers can be switched off to return the bare oracle. The example instance is f = x1 XOR x2 x3 (U_f = Z_1 CZ_23).

Source equation run: `c0fc7471-c935-4366-a8fb-577ef783f42a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[2] (Qiskit MSB) = paper qubit 1 carrying x_1
- q[1] = paper qubit 2 carrying x_2
- q[0] (Qiskit LSB) = paper qubit 3 carrying x_3
- Qiskit basis-state integer = 4 x_1 + 2 x_2 + x_3, matching the specification's label x; for the example U_f = Z_1 CZ_23 = diag(1,1,1,-1,-1,-1,-1,1) in this order, and the full circuit maps |000> to a state with zero amplitude on |000>

## Assumptions

- 'f-controlled phase gate' is the ancilla-free phase oracle (-1)^{f(x)}; constant functions give identity up to global phase.
- The two-target controlled-phase gate applies Z to both targets when the control is |1>, i.e. equals CZ_{c t1} CZ_{c t2} (eq_5).
- The global phase (-1)^{a0} is physically irrelevant but is retained as qc.global_phase for exactness.
- Ideal gates; no transmon qutrit, cavity or decoherence modeling.
- The example instance f = x1 XOR x2 x3 is our own choice, not taken from the paper.

## Unresolved issues

- The paper's explicit list and ordering of the 35 f-controlled phase gates and which CZ pairs it merges into two-target gates are unknown; the implementation enumerates them via ANF coefficients instead.
- The paper's phase convention for the two-target controlled-phase gate is not given; a different convention would change eq_5.
- Physical realization in circuit QED (qutrit level usage, pulse sequences, numerical fidelities) is out of scope and not implemented.

## Equation mapping

- `eq_1`: implemented; _append_oracle (docstring 'eq_1 / eq_4'). The diagonal +/-1 phase oracle is realized as the product of commuting diagonal gates; the global phase (-1)^{a0} is kept via qc.global_phase.
- `eq_2`: implemented; build_circuit (comments 'eq_2: first/second Hadamard layer') and _check_promise. Hadamard layers before and after the oracle are appended when include_hadamards is true; measurement and the classical decision rule are left to the runner, and the constant-or-balanced promise is optionally validated.
- `eq_3`: implemented; _anf_from_truth_table and _anf_from_dict. GF(2) Moebius transform computes the ANF from a truth table; any monomial of degree >= 3 raises ValueError since it is outside the Z/CZ/two-target-CZ gate set (balanced 3-bit functions never have one).
- `eq_4`: implemented; _append_oracle. Z_i for each linear coefficient, CZ_ij for each quadratic coefficient, global phase for a0.
- `eq_5`: implemented; _two_target_cz_gate and the merge loop in _append_oracle. Two-target controlled-phase gate defined as a named composite gate CZ_{c t1} CZ_{c t2}; pairs of CZs sharing a qubit are greedily merged into it when merge_two_target is true.
- `eq_6`: implemented; example_instance_json (anf linear=[1], quadratic=[[2,3]]). The tiny instance f = x1 XOR x2 x3 is the provided example; with one quadratic term no merging occurs, so the oracle is Z on q[2] and CZ on q[1],q[0].

## Specification changes

- eq_1, eq_6: Paper qubit i (leftmost = qubit 1) is mapped to Qiskit qubit n - i (little-endian) so that the Qiskit integer basis label equals x = 4x_1 + 2x_2 + x_3 used in the specification. Reason: Qiskit's qubit 0 is the least significant bit; this mapping preserves the diagonal ordering diag(1,1,1,-1,-1,-1,-1,1) stated in eq_6.
- eq_2: The returned object is the unitary H^{xn} U_f H^{xn} only; initial state |000>, measurement and the 000-vs-not decision rule are excluded. Hadamard layers may be disabled to obtain the bare oracle U_f. Reason: The deliverable must be a measurement-free operation; preparation and measurement are done by the runner.
- eq_3, eq_4: The code accepts any n in 1..12 and any ANF of degree <= 2 (not only n = 3 balanced functions); the constant-or-balanced promise is checked only when enforce_promise is true. Reason: Allows varying valid instance parameters while keeping the paper's gate set; for n = 3 the balanced functions are exactly covered and the 35-gate enumeration is reproduced by varying the ANF coefficients.
- eq_5: Merging of CZ pairs into two-target gates uses a greedy grouping by shared qubit (smallest-label control first); the two-target gate is a composite gate whose definition is two CZ gates. Reason: The paper's specific grouping is unknown; since all factors commute, any grouping gives the same unitary.
