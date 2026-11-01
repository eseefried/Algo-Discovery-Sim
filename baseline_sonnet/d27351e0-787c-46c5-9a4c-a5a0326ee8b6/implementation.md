# Equation to Qiskit

Two-query affine identification circuit on n+1 qubits. Query 1 is a controlled phase oracle for f(x)=a.x xor b, applied to x=|0^n> with a control qubit in |+>. Phase kickback followed by H writes b onto the control qubit. Query 2 is the standard Bernstein-Vazirani circuit H^n U_f H^n on the input register, which writes a onto it. The ideal output on |0^(n+1)> is (-1)^b |b>_c |a>_x. The incompletely-defined-function case and the 2/3 bound are out of scope.

Source equation run: `934bd222-8bce-455d-a381-36355c3b0b64`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: input register x; qubit i carries bit i of a (qubit 0 is least significant)
- qubit n: control/offset qubit c; ends in |b>
- expected ideal output on |0^(n+1)>: (-1)^b |b>_c |a>_x; for the example n=2, a=[1,0] (a_0=1), b=1, the basis state is c=1, x1=0, x0=1, i.e. index 5 in Qiskit ordering

## Assumptions

- Phase-oracle model with the oracle fixed by hidden a and b, supplied in the instance
- Input state |0^(n+1)> is prepared by the runner
- a[i] is the coefficient of qubit i, little-endian
- n is limited to 1..11, so there are at most 12 qubits in total

## Unresolved issues

- The paper's actual two-query algorithm and oracle model are unknown
- Incompletely defined function classes and the 2/3 success probability are not modeled

## Equation mapping

- `eq_1`: implemented; _parse and build_circuit (a, b parameters define f). The affine form is realized through the oracle gates built from a and b; b=0 gives a linear function.
- `eq_2`: implemented; _phase_oracle and _controlled_phase_oracle. Phase oracle (-1)^{f(x)} built from Z gates (a.x part) and a global phase or control-qubit Z (b part).
- `eq_3`: implemented; build_circuit, H^n then _phase_oracle then H^n on register x. One-query BV step yielding (-1)^b|a>; the global phase is included explicitly via circuit global_phase.
- `eq_4`: implemented; build_circuit, first block (H on control, _controlled_phase_oracle, H on control). The offset b=f(0^n) is read out into the control qubit by a controlled phase-oracle query on x=|0^n>.
- `eq_5`: out_of_scope; no code location. The bounded-error 2/3 criterion concerns incompletely defined functions, which are not implemented; this circuit is deterministic for fully specified functions.

## Specification changes

- eq_3, eq_4: Query order reversed relative to the specification steps: the controlled offset query is applied first, while the input register is still |0^n>, and the BV query is applied second. Reason: Evaluating f(0^n) needs x=|0^n>, but BV leaves x in |a>. The circuit must also avoid resets, so the offset query goes first.
- eq_4: The second-query construction is my own phase-kickback design with one extra control qubit, not the paper's two-query algorithm. Reason: The abstract does not give the paper's construction, and the specification marked it as a placeholder.
- eq_2, eq_3: The oracle is compiled from the parameters (a, b) into Z/CZ gates and a phase instead of a lookup table of f, and global phase (-1)^b is tracked explicitly. Reason: The circuit must be built from standard gates without dense unitaries. Tracking the global phase keeps the ideal output state exact.
- eq_5: Scope narrowed to fully specified affine/linear functions; incompletely defined functions and the 2/3 bounded-error analysis are not implemented. Reason: The classes of partial functions are not specified in the abstract.
