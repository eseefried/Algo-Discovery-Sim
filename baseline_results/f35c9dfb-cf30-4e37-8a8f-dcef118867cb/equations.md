# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Compute, on a quantum computer, the weighted sum S = sum_j w_j x_j of a series of inputs x_j (held in qubits) with classical integer weights w_j, by applying controlled phase rotations to an accumulator register held in the Quantum Fourier Transform (Fourier/transform) domain, so that after an inverse QFT the accumulator holds (a_0 + S) mod 2^n. The abstract also interprets this 'controlled weighted sum' as an inner-product circuit and mentions a weighted-average variant.

Scope: No experiment_scope was supplied, so a single smallest useful construction is chosen (assumption): the QFT-domain controlled weighted sum (Draper-style phase addition with classical weights, controlled on single-qubit inputs) on a tiny explicit instance: m = 2 input qubits x = (x_1, x_2) with classical weights w = (1, 2), an n = 3 qubit accumulator initialised to a_0 = 0, arithmetic modulo 2^3 = 8. Test case x = (1,1) should output S = 3 = |011>. Outside scope: QFT multipliers, non-modular (overflow-free) variants, signed-integer (two's complement) handling, the exact transform-domain division used for the weighted average, and any paper-specific circuit optimisations.

## Symbols

- $n$: number of qubits in the accumulator register; arithmetic is modulo 2^n; domain: positive integer; instance n = 3
- $a$: integer value stored in the accumulator, big-endian encoding a = \sum_{l=1}^{n} a_l 2^{n-l} with qubit l = 1 the most significant bit; domain: \{0,\dots,2^n-1\}
- $m$: number of single-qubit inputs; domain: positive integer; instance m = 2
- $x_j$: j-th input bit, stored in input qubit j; domain: \{0,1\}, j = 1..m
- $w_j$: classical integer weight attached to input j; domain: \mathbb{Z}; instance w = (1,2)
- $S$: weighted sum \sum_j w_j x_j (also the inner product w \cdot x); domain: \mathbb{Z}
- $W$: total weight \sum_j w_j used in the weighted average; domain: positive integer
- $R_l(c)$: single-qubit phase gate diag(1, e^{2\pi i c/2^{l}}) acting on accumulator qubit l; domain: c \in \mathbb{Z} (or rational for rescaled variants), l = 1..n
- $\Phi(c)$: tensor product of phase gates implementing addition of classical c in the Fourier domain; domain: unitary on n qubits

## eq_1: QFT with product (per-qubit) form

$$
\mathrm{QFT}\,|a\rangle = \frac{1}{\sqrt{2^n}}\sum_{k=0}^{2^n-1} e^{2\pi i a k/2^n}|k\rangle = \bigotimes_{l=1}^{n}\frac{1}{\sqrt{2}}\left(|0\rangle + e^{2\pi i a/2^{l}}|1\rangle\right)
$$

Definition of the n-qubit QFT and its factorised form; the l-th factor (after the conventional qubit reversal) carries the phase 2\pi a/2^l, which is what makes phase-based arithmetic possible.

Provenance: `standard_background`. Standard QFT definition and product decomposition (Nielsen & Chuang-style); the factor ordering matches the big-endian encoding fixed in the symbols.

Equation assumptions:

- Big-endian encoding a = \sum_l a_l 2^{n-l}; the output qubit order of the QFT circuit is taken so that factor l corresponds to phase 2\pi a/2^l.

## eq_2: Fourier-domain addition of a classical constant (Draper adder)

$$
\Phi(c) = \bigotimes_{l=1}^{n} R_l(c),\quad R_l(c)=\mathrm{diag}\left(1, e^{2\pi i c/2^{l}}\right),\quad \Phi(c)\,\mathrm{QFT}|a\rangle = \mathrm{QFT}\,|(a+c) \bmod 2^n\rangle
$$

Multiplying each Fourier factor by e^{2\pi i c/2^l} shifts the encoded integer by c; the equality is exact and the result is reduced modulo 2^n because e^{2\pi i (a+c)/2^l} is 2^l-periodic and 2^l divides 2^n.

Provenance: `standard_background`. Draper's QFT adder with a classical addend: phases add, so the Fourier-encoded integer adds modulo 2^n. This is the 'existing Quantum Fourier Transform adder' the abstract says is reviewed, recalled from background rather than from the paper.

Equation assumptions:

- Addend c is classical; no overflow qubit, so the result is modular (non-modular variants in the paper are out of scope).

## eq_3: Controlled weighted sum in the Fourier domain

$$
\left(\prod_{j=1}^{m} C_{x_j}\!\left[\Phi(w_j)\right]\right)\,|x_1\dots x_m\rangle\otimes\mathrm{QFT}|a_0\rangle = |x_1\dots x_m\rangle\otimes\mathrm{QFT}\,\Big|\big(a_0 + \sum_{j=1}^{m} w_j x_j\big) \bmod 2^n\Big\rangle
$$

Each input qubit x_j controls the phase-addition block \Phi(w_j); because the blocks are diagonal and commute, the accumulator receives exactly S = \sum_j w_j x_j (mod 2^n). Inputs in superposition give the corresponding superposition of sums (linearity).

Provenance: `abstract_inferred`. Inferred from the abstract's 'controlled weighted sum' computed 'in the transform domain': controlling the Draper constant-adder of eq_2 on an input qubit adds w_j only when x_j = 1, and composing over j yields the weighted sum. The paper's exact gate arrangement is unknown.

Abstract evidence: One of the circuits, the controlled weighted sum

Equation assumptions:

- Inputs are single qubits (bits); multi-qubit integer inputs would require controlled-\Phi(w_j 2^{t}) for each input bit t, which is a straightforward extension not instantiated here.
- Weights are classical integers compiled into the rotation angles.

## eq_4: Inner-product interpretation and tiny instance

$$
S = \sum_{j=1}^{m} w_j x_j = w\cdot x;\qquad n=3,\ w=(1,2),\ x=(1,1),\ a_0=0 \Rightarrow S = 3,\ \text{output } |011\rangle
$$

The weighted sum of bits is the inner product of the weight vector with the input bit vector; the explicit instance gives a deterministic check value.

Provenance: `abstract_inferred`. Directly follows from the abstract's statement that the controlled weighted sum computes an inner product; the specific instance values are a chosen assumption.

Abstract evidence: can be interpreted as a circuit to compute the inner product of two data vectors

Equation assumptions:

- Instance parameters (n=3, m=2, w=(1,2), x=(1,1), a_0=0) are chosen here, not taken from the paper.
- With one data vector classical (w) and the other quantum (x); the paper's version may allow both vectors to be quantum.

## eq_5: Weighted average by phase rescaling (exact only when W divides S)

$$
\left(\prod_{j} C_{x_j}\!\left[\Phi\!\left(\tfrac{w_j}{W}\right)\right]\right)\mathrm{QFT}|0\rangle = \bigotimes_{l=1}^{n}\tfrac{1}{\sqrt2}\left(|0\rangle + e^{2\pi i (S/W)/2^{l}}|1\rangle\right),\quad W=\sum_j w_j;\qquad \mathrm{QFT}^{-1}(\cdot) = \left|\tfrac{S}{W}\right\rangle \iff W \mid S
$$

Dividing all rotation angles by the total weight encodes the rational S/W as a Fourier phase. The inverse QFT returns the computational basis state |S/W> exactly only if S/W is an integer; otherwise the output is a spread distribution peaked near S/W (an approximation, not an exact integer average or quotient).

Provenance: `abstract_inferred`. The abstract claims a transform-domain weighted-average method but gives no construction; rescaling the phases is the natural transform-domain candidate, offered as an inference. The exact/approximate distinction is stated explicitly because division is generally not exact on integers.

Abstract evidence: a quantum method to compute the weighted average of a series of inputs in the transform domain

Equation assumptions:

- The paper's actual weighted-average construction may differ (e.g., different normalisation or rounding convention); this equation is a plausible reconstruction only.
- W > 0 and S/W within [0, 2^n) so no modular wrap is involved.

## Registers

- acc: n = 3 qubits; accumulator holding the (Fourier-encoded) integer a; big-endian, qubit 1 = MSB
- inp: m = 2 qubits; input qubits x_1, x_2 acting as controls for the weighted phase additions

## Initial state

|x_1 x_2\rangle_{inp} \otimes |000\rangle_{acc} with x prepared as a computational basis state (instance x = (1,1)); the accumulator starts at a_0 = 0.

## Measurement

Measure all n accumulator qubits in the computational basis; read the bitstring big-endian as the integer (a_0 + S) mod 2^n. For basis-state inputs the outcome is deterministic (instance: |011> = 3 with probability 1, up to gate noise). Input qubits are unchanged and need not be measured.

## Classical postprocessing

Decode the measured bitstring as an integer with qubit 1 as MSB; compare with the classically computed w\cdot x mod 2^n (instance: 3). For the weighted-average variant, estimate S/W from the measured peak and treat non-integer cases as approximate.

## Algorithm steps

1. Prepare the input register in |x_1 x_2> (X gates on the qubits with x_j = 1) and the accumulator in |000>. (no equation reference)
2. Apply the QFT to the accumulator so that it holds QFT|0> (equal superposition with trivial phases). (eq_1)
3. For each input j = 1..m, apply the block \Phi(w_j) = \bigotimes_l R_l(w_j) to the accumulator controlled on input qubit x_j (controlled phase gates diag(1,1,1,e^{2\pi i w_j/2^l}) on pairs (x_j, acc_l)); rotations with angle equal to a multiple of 2\pi may be dropped. (eq_2, eq_3)
4. Apply the inverse QFT to the accumulator, returning it to the computational basis state |(a_0 + S) mod 2^n>. (eq_1, eq_3)
5. (Optional weighted-average variant, out of the core scope) replace the angles w_j by w_j/W before the inverse QFT; the result is exact only when W divides S. (eq_5)

## Assumptions

- No experiment_scope was given; the controlled weighted sum (inner-product) circuit on n=3, m=2, w=(1,2), x=(1,1) was chosen as the single smallest useful construction.
- Arithmetic is modular (mod 2^n); the abstract's non-modular and signed-integer extensions are not reconstructed.
- Inputs are single bits and weights are classical; the abstract does not state the data types used for the two 'data vectors'.
- Big-endian integer encoding and the standard QFT convention are fixed by this specification, not by the paper.
- QFT precision is exact (no approximate-QFT truncation of small rotations).

## Missing information

- Exact circuits of the paper's modified adders/multipliers and how they achieve non-modular (overflow-aware) arithmetic.
- How signed integers are represented (e.g., two's complement) and handled in the Fourier domain.
- The precise construction and normalisation of the weighted-average method, including how division by the total weight is realised and whether the output is rounded, truncated, or left as a phase.
- Whether both vectors in the inner-product interpretation can be quantum registers, and the gate count / depth of the paper's circuits.
- The QFT multiplier constructions reviewed in the abstract.
