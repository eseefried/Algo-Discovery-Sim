# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Two-qubit Simon problem: given an opaque oracle U_f|x>|y>=|x>|y xor f(x)> with f:{0,1}^2->{0,1}^2 satisfying f(x)=f(x') iff x' in {x, x xor s}, recover the hidden s in {00,01,10,11}. Method: collapse-first ordering with a final Hadamard on the x register, sampled a few times, then GF(2) postprocessing.

Scope: Logical 2-qubit Simon on 4 qubits (x: q0,q1; f-register: q2,q3), no ancilla needed for the sampling circuit. Excludes the one-way cluster-state implementation, the photonic experiment, the n-qubit resource analysis, and the swap-test/comparison verification, which is only loosely described in the sketch.

## Symbols

- $x$: input bitstring (x1 x0), q0 is bit 0; domain: {0,1}^2
- $f$: Simon function; domain: {0,1}^2 -> {0,1}^2
- $s$: hidden period; domain: {0,1}^2
- $y$: measured x-register string after Hadamards; domain: {0,1}^2
- $x_0$: input value selected by the output measurement; domain: {0,1}^2
- $U_f$: opaque oracle, one query per sample; domain: unitary on 4 qubits
- $m$: number of samples; domain: integer, 2 to 4 (more for s=0 confidence)

## eq_1: Oracle action and superposition

$$
U_f\left(H^{\otimes 2}|00\rangle\right)|00\rangle=\frac12\sum_{x\in\{0,1\}^2}|x\rangle|f(x)\rangle
$$

State after one oracle query on the uniform superposition.

Provenance: `standard_background`. Standard Simon oracle definition with the oracle form given in the task assumptions.

Equation assumptions:

- Oracle maps |x>|y> to |x>|y xor f(x)>

## eq_2: Collapse after output measurement

$$
|\psi_{x_0}\rangle=\frac{1}{\sqrt2}\left(|x_0\rangle+|x_0\oplus s\rangle\right)
$$

Measuring the f-register gives some f value, leaving the x register in the pair state (a single basis state if s=0).

Provenance: `standard_background`. Follows from the 2-to-1 promise; measuring the output register commutes with the final Hadamards on x, so the statistics match the standard circuit.

Equation assumptions:

- s != 0 for the pair state; x_0 uniform

## eq_3: Hadamard readout distribution

$$
P(y)=\begin{cases}\frac{2}{2^{2}}\,\delta_{y\cdot s,0}=\frac12\,\delta_{y\cdot s,0} & s\neq 0\\ \frac14 & s=0\end{cases}
$$

Distribution of y after H on x. Support is {y: y.s=0 mod 2}. Expected supports: s=11 -> {00,11}; s=01 -> {00,10}; s=10 -> {00,01}; s=00 -> all four.

Provenance: `standard_background`. Standard Simon sampling result; it matches the sketch's expected distributions.

Equation assumptions:

- Little-endian parsing: y_i = bits[::-1][i], with the string written y1 y0 and s·y = s0 y0 xor s1 y1

## eq_4: Linear constraint

$$
y\cdot s=\bigoplus_{i=0}^{1} y_i s_i=0 \pmod 2
$$

Each sample gives a linear constraint on s.

Provenance: `standard_background`. Standard Simon postprocessing; the abstract only says the algorithm is solved.

## eq_5: Brute-force decoding

$$
\hat s=\begin{cases}s'\neq 0 \text{ such that } y^{(k)}\cdot s'=0\ \forall k & \text{if exactly one such } s' \text{ exists}\\ 00 & \text{otherwise}\end{cases}
$$

Test the 3 nonzero candidates against all m samples. If none is consistent, or if more than one is consistent (all y=00 or too few independent samples), report 00 or request more samples. A final check of f(x) versus f(x xor s) can resolve s=0 versus nonzero, at the cost of two more queries.

Provenance: `assumption`. Postprocessing from the sketch, with the ambiguity rule made explicit.

Equation assumptions:

- The ambiguity rule is an interpretation of the sketch
- s=0 is detected only probabilistically from samples unless the verification step is used

## Registers

- x: 2 (q0,q1) qubits; input register; Hadamards then measured to give y
- f: 2 (q2,q3) qubits; oracle output register; measured to collapse x
- anc: 1 (q4), optional qubits; unused in the sampling circuit; reserved for the verification comparison

## Initial state

|0000> on q0..q3 (ancilla q4 in |0> if present)

## Measurement

Measure q0,q1 after H into 2 classical bits (little-endian). The q2,q3 measurement is optional and does not change the x statistics.

## Classical postprocessing

Collect the distinct y values, then run the brute-force consistency test of eq_5 over s in {01,10,11} with parity y0 s0 xor y1 s1.

## Algorithm steps

1. Apply H to q0,q1. (eq_1)
2. Place the opaque U_f once on (q0,q1,q2,q3), with x as controls and q2,q3 as target register. (eq_1)
3. Measure q2,q3 (or defer; statistics are equal). This collapses x. (eq_2)
4. Apply H to q0,q1 and measure them into classical bits 0,1. Parse counts with bits[::-1][i] as bit i, and discard the f-register bits from the key if they are measured. (eq_3)
5. Repeat for m samples (one query per sample). Decode s from the constraints. (eq_4, eq_5)

## Assumptions

- Choose the 2-qubit instance with qubit cap >= 5
- Mid-circuit measurement of the f-register is equivalent to deferred measurement
- The final Hadamard on x is the same as in the standard Simon circuit; the sketch's 'collapse-first' ordering does not change the statistics
- Swap-test and Hadamard-test ancilla parts of the sketch are not needed for sampling and are not specified here

## Missing information

- Exact verification circuit (ancilla comparison of f(x) and f(x xor s)) is unspecified
- The abstract gives no cluster-state measurement angles, so the one-way implementation is not reconstructed
- Number of samples for a target success probability is not specified
