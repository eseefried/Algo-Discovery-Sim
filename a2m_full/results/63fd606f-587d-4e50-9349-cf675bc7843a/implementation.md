# Equation to Qiskit

Builds the first-query Bernstein-Vazirani circuit for an affine Boolean function f(x)=a.x xor b on n input qubits plus one target qubit: H^n on the input register, one XOR-oracle query U_f, then H^n. The oracle is made from CX gates (one per a_i=1) and an X on the target when b=1. The runner must prepare |0^n>|-> as input and measure. Under that input, the input register ends in |a> up to the global phase (-1)^b.

Source equation run: `ffeb6e3f-fdc0-4cb9-9c7f-8a89af2220d4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: input register x, qubit i holds x_i (little-endian, a[i] is the coefficient of x_i)
- qubit n: oracle target t; the runner should prepare it in |-> = (|0>-|1>)/sqrt2 for the BV phase-kickback
- expected input: |0^n> on qubits 0..n-1 and |-> on qubit n; expected output: input register in |a> with a_i on qubit i, up to global phase (-1)^b

## Assumptions

- Qubit i of the input register holds x_i, so a[i] is the coefficient of x_i and the output bit i is a[i] (Qiskit little-endian).
- Instance 'a' is a JSON list of n ints in {0,1}, and 'b' is an int in {0,1}.
- The runner prepares the target in |->.
- The function is fully defined on {0,1}^n.

## Unresolved issues

- The paper's actual second-query circuit is not specified and is not implemented.
- The classes of incompletely defined functions and the 2/3 bound are not implemented.
- The oracle behavior on undefined inputs is not specified.

## Equation mapping

- `eq_1`: implemented; build_circuit: CX(x[i], t) for a[i]=1 and X(t) if b=1 (the XOR oracle for f(x)=a.x xor b). The XOR oracle for an affine function is built from standard gates, with no dense unitary.
- `eq_2`: implemented; build_circuit: qc.h(x) before and after the oracle block. Implements H^n U_f H^n. With the runner-prepared |0^n>|-> input, the input register ends in (-1)^b|a>, so b appears only as a global phase.
- `eq_3`: out_of_scope; no code location. The second query reads f(0^n) from a computational-basis input. It is a separate circuit with a different input state and is not part of this single-construction scope.
- `eq_4`: out_of_scope; no code location. Classical postprocessing that computes b from s and f(x_0), and it needs a query at x_0. It is not a circuit construction here.
- `eq_5`: out_of_scope; no code location. Output distribution for incompletely defined functions. The promise class is unspecified and the oracle on undefined inputs is not defined, so it is not implemented.

## Specification changes

- eq_1, eq_2: Scope narrowed to the first-query circuit H^n U_f H^n for a fully defined affine f, with n up to 11 (12 qubits total). Reason: The task requires one explicit construction. The two-query decision procedure and the partial-domain case involve different input states, classical postprocessing and an unspecified promise class.
- eq_2: Preparation of the target in |-> (X then H on the target) and of |0^n> is left to the runner. The circuit contains no state preparation or measurement. Reason: The circuit must be an operation only, with inputs prepared by the runner.
- eq_3, eq_4, eq_5: These equations are not implemented and are classified as out_of_scope. Reason: They belong to the second query, classical postprocessing and the partial-domain analysis, not to the chosen construction.
- eq_1: The offset b is realized by an X on the target qubit, and a_i by CX gates from input qubit i to the target. Reason: Concrete gate-level realization of the XOR oracle for f(x)=a.x xor b.
