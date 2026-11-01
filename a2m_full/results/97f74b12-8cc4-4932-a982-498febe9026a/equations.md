# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Build an exact oracle U_f|x>|y> = |x>|y xor f(x)> for an explicit Boolean truth table f on n bits, using a phase-polynomial (Walsh-Hadamard/Fourier parity) expansion, parity ancillas and Z rotations, with a constant-depth structure when fan-out is treated as an elementary gate.

Scope: Tiny instance n=2 and f=OR(x0,x1), with the target y included. The circuit uses explicit parities and RZ/phase gates with no black-box queries. The paper's general MBQC-equivalence proof, the exact constant-depth fan-out realisation and the optimised ancilla counts are outside this scope.

## Symbols

- $n$: number of input bits; domain: positive integer, small (n=2 here)
- $x$: input bit string x_0..x_{n-1}; domain: {0,1}^n
- $f$: classical Boolean function given as a truth table; domain: {0,1}^n -> {0,1}
- $s$: parity mask selecting a subset of input bits; domain: {0,1}^n
- $s\cdot x$: parity of the selected bits, sum_i s_i x_i mod 2; domain: {0,1}
- $\alpha_s$: phase-polynomial coefficient: the phase pi f(x) = sum_s alpha_s (s.x mod 2); domain: real
- $y$: target bit; domain: {0,1}
- $a_s$: parity ancilla for mask s; domain: qubit initially |0>

## eq_1: Bit-flip oracle

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle
$$

Target oracle for a classical function.

Provenance: `abstract_inferred`. The abstract says the oracle implements a classical function; the XOR form is the standard definition of such an oracle.

Abstract evidence: any quantum oracle implementing a classical function

Equation assumptions:

- f is an explicit truth table

## eq_2: Phase oracle from bit-flip oracle

$$
U_f=(I\otimes H)\,\Big(\sum_x |x\rangle\langle x|\otimes Z^{f(x)}\Big)(I\otimes H),\quad Z^{f(x)}=e^{i\pi f(x) Z_y\text{-conjugate}}
$$

The oracle equals Hadamards on y around a diagonal operator that applies Z to y exactly when f(x)=1. The Z on y is a phase (-1)^{f(x) y}.

Provenance: `standard_background`. Standard identity H Z H = X, applied conditionally on f(x).

## eq_3: Phase polynomial of f*y

$$
\pi f(x)\,y=\sum_{s\in\{0,1\}^n\setminus 0}\alpha_s\,\big[(s\cdot x)\oplus y\big]-\ldots
$$

Replace this with the exact-form expansion in eq_4. Each term is a parity of selected x bits and y, realised as a phase on a parity ancilla.

Provenance: `assumption`. The sketch includes y in the parities. The exact general coefficients are computed classically from the truth table.

Equation assumptions:

- coefficients computed classically from the truth table

## eq_4: Walsh-Hadamard expansion of the integer phase

$$
(-1)^{f(x)}=\sum_{s}\hat F(s)\,(-1)^{s\cdot x},\quad \hat F(s)=2^{-n}\sum_x(-1)^{f(x)+s\cdot x}
$$

Walsh-Hadamard expansion of the phase function. Realising it as a product of RZ rotations on parity ancillas requires the phase-polynomial form eq_5.

Provenance: `standard_background`. Standard Fourier analysis on the Boolean cube. Relation to the paper's method is not confirmed.

## eq_5: Parity-sum form for the phase

$$
f(x)=\sum_{s\ne 0}c_s\,(s\cdot x \bmod 2),\; c_s=\frac{(-1)^{|s|+1}}{2^{|s|-1}}\ \text{ real-valued, with } (s\cdot x\bmod 2)=\tfrac12(1-(-1)^{s\cdot x})
$$

Real-valued parity expansion of f. Each parity bit p_s(x)=(s.x mod 2) gets a phase exp(i pi c_s p_s). Exact c_s come from solving f(x)=sum_s c_s p_s(x), which is a 2^n-by-2^n invertible system after adding the constant term. The OR closed form shown is not claimed to be correct for every n.

Provenance: `assumption`. The sketch states the Fourier expansion has 2^n-1 terms. The solution is reproducible by solving the linear system classically.

Equation assumptions:

- solve the linear system numerically for the c_s

## eq_6: Z-rotation on a parity ancilla

$$
R_Z(\theta_s)=\mathrm{diag}(1,e^{i\theta_s}),\ \theta_s=\pi c_s,\ \text{applied to } a_s \text{ holding } s\cdot x
$$

A phase gate on each parity ancilla gives total phase exp(i pi sum_s c_s p_s(x)) = (-1)^{f(x)}.

Provenance: `abstract_inferred`. The abstract names Z rotations and fan-out as the elementary gates.

Abstract evidence: arbitrary rotations along $Z$ axis and unbounded fan-outs are elementary operations

Equation assumptions:

- exact-angle phase gates

## Registers

- x: n (2) qubits; input bits
- y: 1 qubits; target; included in the parities for the controlled-Z-on-y step
- a: 2^n-1 (3 for n=2) parity ancillas, or 2^(n+1)-1 if y is included qubits; parity ancillas, returned to |0>

## Initial state

|x>|y>|0...0> for a computational basis input, or a superposition on x

## Measurement

For counts, measure y and optionally x only. Qiskit is little-endian: with measure(i,i), bits[::-1][i] is classical bit i. Check that the ancillas are |0> from the statevector.

## Classical postprocessing

Compare the measured y with y xor f(x) for each basis input, and check ancilla cleanliness.

## Algorithm steps

1. Classically compute the real coefficients c_s from the truth table of f. (eq_5)
2. Apply H on y. (eq_2)
3. Compute each parity s.x into ancilla a_s using CX gates (a fan-out of x_i to every ancilla whose mask contains i). For the controlled-on-y version, also include y in the masks. (eq_6)
4. Apply the phase gate with angle pi c_s on each ancilla a_s. In the controlled-on-y version use the parity of (s.x) xor y so the phase acts only as a Z-type kick on y. (eq_3, eq_6)
5. Uncompute the parity ancillas with the same CX layers, then apply H on y. (eq_1, eq_2)

## Assumptions

- Smallest case n=2, f=OR chosen by us because no scope was given.
- Fan-out is realised as CX gates, so simulated depth is not constant.
- Ancilla count is exponential in n.
- No black-box query is used.

## Missing information

- Exact constant-depth fan-out and parity gate construction and its MBQC equivalence.
- Exact formulation of the angle schedule for general f, in particular the controlled-on-y version, which the sketch leaves vague.
- How the paper reaches an exact OR with its specific angles.
