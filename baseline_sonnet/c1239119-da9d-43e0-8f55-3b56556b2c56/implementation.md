# Equation to Qiskit

Exact bit-flip oracle U_f|x>|y> = |x>|y xor f(x)> for a Boolean function f given as a truth table, or as the n-bit OR (eq_5). Construction: H on the target, a diagonal phase exp(i*pi*y*f(x)) built from the Walsh-parity expansion of f, then H on the target again. Each parity term uses CNOTs onto one qubit of S, a controlled-phase to the target, and CNOT uncomputation. Constant depth, the MBQC translation and unbounded fan-out are not implemented. Depth here grows with the number of nonzero Walsh coefficients.

Source equation run: `f611d44c-b4c6-49cd-b2a6-3362967ac77a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x_0 (least significant input bit)
- qubit 1: x_1
- qubit 2: x_2
- qubit 3: target y (computational basis, y -> y xor f(x))
- no ancilla qubits; input index x = sum_i x_i 2^i

## Assumptions

- Input index convention: x_i is on qubit i, so truth_table[x] uses x = sum x_i 2^i.
- Target is qubit n; no ancillas are used.
- n is capped at 11 so the total qubit count stays at most 12.

## Unresolved issues

- The paper's constant-depth MBQC construction is not reconstructed; this circuit's depth scales with the number of nonzero Walsh coefficients.
- The exact constant-depth OR implementation is not reproduced.
- Fan-out and the MBQC equivalence are not modelled.

## Equation mapping

- `eq_1`: implemented; build_circuit (whole circuit). The circuit acts as |x>|y> -> |x>|y xor f(x)> for any truth table or for OR.
- `eq_2`: implemented; build_circuit: qc.h(y) before and after the phase block. Implemented in corrected form: Hadamards on the target conjugate sum_x |x><x| (x) Z^{f(x)}. The stated form, with a bare diagonal phase on x and no target dependence, is the phase-kickback form and does not equal U_f.
- `eq_3`: implemented; _walsh and the coefficient loop in build_circuit. The Walsh coefficients of (-1)^f give the exact identity f(x) = f(0) + sum_{S nonempty} ghat(S) x_S. This drives the controlled-phase angles pi*ghat(S) on the parity x_S.
- `eq_4`: background; no code location. The paper's Z-rotation-on-parity elementary gate is not used literally. Parities are computed in place with CNOTs and the phase is applied with a controlled-phase to the target. The paper's angle schedule is unspecified.
- `eq_5`: implemented; _truth_table: function == 'or' branch. OR(x) = 1 xor prod(1 xor x_i) is 0 only at x = 0, giving the truth table [0,1,...,1].

## Specification changes

- eq_2: Replaced the diagonal phase operator on x alone by the target-controlled form sum_x |x><x| (x) Z^{f(x)}, conjugated by H on the target. Reason: The original expression is not equal to the bit-flip oracle U_f.
- eq_3, eq_4: Used the real-valued parity expansion f(x) = f(0) + sum ghat(S) x_S with controlled-phase gates onto the target, rather than Rz rotations on parity qubits. Reason: This gives an exact, ancilla-free gate-model oracle from the stated Walsh background.
- eq_1, eq_2, eq_3, eq_4, eq_5: Narrowed scope to a standard-gate circuit-model oracle for a truth-table function (including OR). The constant-depth property, MBQC pattern, unbounded fan-out and ancilla-based construction are not implemented. Reason: The abstract does not give the constant-depth construction, angle schedule or MBQC pattern.
