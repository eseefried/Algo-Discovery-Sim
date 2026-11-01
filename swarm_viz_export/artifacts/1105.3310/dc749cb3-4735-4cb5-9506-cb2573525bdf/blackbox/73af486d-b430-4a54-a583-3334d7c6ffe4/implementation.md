# Equation to Qiskit

Naive 10-qubit Bernstein-Vazirani-style circuit for n=3, d=2, q=2. The 7 coefficients of f are compiled into Z gates and H layers map the phase pattern to a computational basis state that encodes the coefficients. No oracle queries are made and no query-complexity claim is made. The controlled-phase step in the specification was corrected to uncontrolled Z gates.

Source equation run: `7f875245-3cfd-42e6-a395-31a42bc8da6c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0: a0 -> c_0
- q1: a1 -> c_1
- q2: a2 -> c_2
- q3: a3 -> c_3
- q4: block 1 variable x2 -> c_12
- q5: block 1 variable x3 -> c_13
- q6: block 2 variable x1 -> c_12 (redundant copy)
- q7: block 2 variable x3 -> c_23
- q8: block 3 variable x1 -> c_13 (redundant copy)
- q9: block 3 variable x2 -> c_23 (redundant copy)
- Qiskit little-endian: qubit 0 is least significant; output is a computational basis state

## Assumptions

- Instance keys are 'coefficients' (dict from monomial string to 0 or 1) and optionally n=3, d=2, q=2.
- Monomial keys are '0','1','2','3','12','13','23', and missing keys mean 0.
- Redundant copies of pairwise coefficients agree because they are compiled from the same classical value.
- No input-state preparation is done in the circuit. The runner is assumed to supply |0...0>.

## Unresolved issues

- The paper's actual quantum algorithm (exact O(n^(d-1)) queries, state orthogonality construction) is not reconstructed.
- General q, n and d are not supported.
- The circuit uses hard-coded coefficients rather than black-box queries, so it demonstrates no query advantage.

## Equation mapping

- `eq_1`: implemented; _read_coefficients (parses and validates the 7 coefficients of the degree<=2 monomials; missing keys mean 0). The polynomial is represented by its coefficient dictionary and compiled into gates; f is never evaluated as an oracle.
- `eq_2`: implemented; build_circuit, derivative-phase loop (comment eq_2/eq_3). The derivative coefficients c_i and c_ij determine which Z gates are applied on ancilla a_i and block i.
- `eq_3`: implemented; build_circuit, derivative-phase loop. The diagonal phase (-1)^(l.x') is compiled as Z on x'[j] when c_ij=1. The constant part c_i is a Z on a_i, which is a corrected treatment.
- `eq_4`: implemented; build_circuit, first and last H layers around the Z gates. H, then the phase Z^(c_i) on a_i and Z^(l_j) on x'_j, then H gives |c_i>|l^(i)> exactly. The spec's controlled form was corrected.
- `eq_5`: implemented; build_circuit, 'eq_5' comment (Z on qubit 0 if c_0=1). H Z^{c_0} H |0> = |c_0> on qubit 0, a classical shortcut because c_0 is compiled in.

## Specification changes

- eq_3, eq_4: Replaced CZ(a_i, x_i[j]) controlled phases with uncontrolled Z(x_i[j]) for c_ij=1, keeping Z(a_i) for c_i=1. Reason: With a_i and x' both in |+>, the controlled phase (-1)^{b(c_i + l.x')} gives (1/sqrt2) sum_b (-1)^{b c_i}|b>|b l> after H on x'. Final H on a_i does not give the basis state |c_i>|l>, so the stated identity fails for l != 0. The correct BV phase is the linear function h(b,y)=b c_i + l.y, which is uncontrolled.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to n=3, d=2, q=2 with coefficients compiled into gates. Reason: This is a naive functional reconstruction, not the paper's exact O(n^(d-1)) query algorithm. It makes no query-complexity claim.
