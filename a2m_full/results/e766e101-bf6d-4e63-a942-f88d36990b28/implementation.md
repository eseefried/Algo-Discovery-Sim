# Equation to Qiskit

Exact bit-flip oracle U_f|x>|y> = |x>|y xor f(x)> for a user-supplied truth table (n<=6 inputs, 12-qubit cap). It is built as H_y . diag(exp(i*pi*f(x)*y)) . H_y. The phase pi*f(x)*y is produced from the real parity expansion f(x) = f(0) + sum_{s!=0} F(s) (s.x mod 2), where F is the Walsh coefficient. Parities of weight>=2 are computed by CX fan-in onto clean ancillas, and a y-controlled phase gate with angle pi*c_s is applied on each parity (directly on x_i for weight-1 masks). The ancillas are then uncomputed. Only masks with nonzero coefficient get an ancilla. The default example is OR on 2 bits.

Source equation run: `97f74b12-8cc4-4932-a982-498febe9026a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = x_0 (least significant bit of x; truth_table index x = sum_i x_i 2^i)
- qubits 1..n-1 = x_1..x_{n-1}
- qubit n = y (target)
- qubits n+1.. = clean parity ancillas, one per mask s with weight>=2 and nonzero coefficient, in increasing mask order (returned to |0>)
- example n=2, f=OR: qubits 0,1 = x_0,x_1; qubit 2 = y; qubit 3 = ancilla for mask 0b11

## Assumptions

- f is given as an explicit truth table indexed by x = sum_i x_i 2^i, matching Qiskit little-endian order.
- Parity ancillas are supplied in |0> by the runner.
- Default example is OR on 2 bits.
- Controlled-phase gates with exact angles are available as elementary gates.

## Unresolved issues

- The exact constant-depth fan-out and MBQC construction from the paper is not reproduced.
- The gate depth here grows with n and with the number of nonzero Walsh coefficients, and the ancilla count is exponential in n for dense functions.
- The 12-qubit cap rejects functions needing too many parity ancillas, e.g. OR on 4 inputs needs 4+1+11=16 qubits.

## Equation mapping

- `eq_1`: implemented; build_circuit (overall operation). The full circuit realises |x>|y> -> |x>|y xor f(x)> with ancillas restored to |0>.
- `eq_2`: implemented; build_circuit: qc.h(y) before and after the phase block. H on y conjugates the diagonal phase exp(i*pi*f(x)*y) into the conditional X. The latex 'Z_y-conjugate' exponent is garbled, so the standard identity H Z H = X is used.
- `eq_3`: implemented; build_circuit: loop of qc.cp(theta, y, ...) and qc.p(pi, y). The garbled equation is replaced by the exact expansion pi*f(x)*y = pi*y*(f(0) + sum_{s!=0} c_s p_s(x)). Each term is a phase on |y=1, p_s=1> (a controlled-phase gate), instead of putting y inside the parities.
- `eq_4`: implemented; _coeffs. The Walsh-Hadamard coefficients F(s) are computed classically from the truth table.
- `eq_5`: implemented; _coeffs and build_circuit (parity ancilla CX fan-in). The real parity expansion is f(x) = f(0) + sum_{s!=0} F(s) p_s(x). The coefficients are computed from the Walsh transform instead of the stated OR closed form, which is incorrect (for n=2 OR it gives c_s=1 for |s|=1, but the exact value is 1/2).
- `eq_6`: implemented; build_circuit: qc.cp(theta, y, ancilla or x_i). The phase angle is theta_s = pi*c_s on the parity qubit, with phase diag(1,e^{i theta}) (not an RZ with a global phase). It is controlled on y so the total phase is exp(i*pi*f(x)*y).

## Specification changes

- eq_3: The garbled y-parity expansion is replaced by y-controlled phases on x-parity qubits, plus a constant term f(0) applied as a phase gate on y. Reason: This is the exact decomposition, and it avoids extra ancillas that would hold parities including y.
- eq_5: The coefficients c_s = F(s) (s!=0) and c_0 = f(0) are computed numerically from the truth table; the stated OR closed form is not used. The constant term is included. Reason: The stated closed form is incorrect. For OR on n=2 the correct coefficients are c_01=c_10=c_11=1/2 and c_0=0.
- eq_6: The phase gate is y-controlled (controlled-phase) rather than a bare phase on the ancilla. Reason: A bare phase would give (-1)^{f(x)} independent of y. The oracle needs the phase only when y=1.
- eq_1, eq_6: The scope is narrowed to a general explicit truth table with n<=6 and at most 12 total qubits. Fan-out is realised as CX gates, so the depth is not constant. There is no MBQC and no constant-depth fan-out. Reason: The spec lists the MBQC equivalence and constant-depth fan-out as out of scope or missing.
- eq_5: Ancillas are allocated only for masks with weight>=2 and nonzero coefficient. Weight-1 masks use the x qubit directly. Reason: This reduces qubit count while keeping the construction exact.
