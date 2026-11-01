# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Perform arithmetic (addition, weighted sum / inner product) on a quantum computer in the Fourier (transform) domain using QFT-based adders and multipliers, with modular/non-modular and signed-integer variants.

Scope: Smallest useful construction: a Draper-style QFT adder (modular addition of a classical constant or register) and its extension to a weighted sum accumulating sum_j w_j x_j in the phase domain, with a tiny instance of n=3 target qubits and two inputs. Outside scope: the paper's specific circuit variants, signed-integer handling details, controlled versions, the weighted-average method (including any division/normalization), and resource counts.

## Symbols

- $n$: number of qubits in the accumulator register; domain: positive integer
- $N$: modulus 2^n; domain: positive integer
- $a,b$: integers encoded in computational basis; domain: 0 \le a,b < N
- $\mathrm{QFT}$: quantum Fourier transform on n qubits; domain: unitary on (\mathbb{C}^2)^{\otimes n}
- $x_j$: data input values held in registers; domain: integers in [0,2^m)
- $w_j$: weights (classical or quantum); domain: integers
- $S$: weighted sum \sum_j w_j x_j; domain: integer

## eq_1: QFT definition

$$
\mathrm{QFT}|b\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{2\pi i bk/N}|k\rangle
$$

QFT of a computational basis state, defining the transform domain.

Provenance: `standard_background`. Standard definition; the abstract only names the QFT.

Equation assumptions:

- N=2^n

## eq_2: Phase-domain addition

$$
|\phi(b)\rangle\mapsto \frac{1}{\sqrt{N}}\sum_{k}e^{2\pi i (a+b)k/N}|k\rangle=|\phi(a+b \bmod N)\rangle
$$

Adding a in the Fourier domain via phase rotations gives a+b modulo N; exact equality in the modular sense.

Provenance: `standard_background`. Draper adder background; the abstract mentions QFT adders but gives no formulas.

Equation assumptions:

- Phases applied as single-qubit (controlled) rotations by 2\pi a/2^{l}

## eq_3: Full adder circuit

$$
|b\rangle\xrightarrow{\mathrm{QFT}}|\phi(b)\rangle\xrightarrow{\Phi_{\mathrm{ADD}}(a)}|\phi(a+b)\rangle\xrightarrow{\mathrm{QFT}^{-1}}|(a+b)\bmod N\rangle
$$

QFT adder pipeline.

Provenance: `standard_background`. Standard Draper adder structure.

Equation assumptions:

- Non-modular result requires an extra carry qubit, i.e. n larger than bit length of a+b

## eq_4: Weighted sum accumulation

$$
|0\rangle_{\phi}\mapsto|\phi(S \bmod N)\rangle,\quad S=\sum_j w_jx_j,\quad \text{phase }\exp\!\Big(\tfrac{2\pi i k}{N}\sum_j w_jx_j\Big)
$$

Controlled phase rotations by bits of x_j scaled by w_j accumulate the weighted sum in the accumulator, modulo N. This is the inner product of vectors w and x.

Provenance: `abstract_inferred`. The inner-product interpretation implies accumulating sum_j w_j x_j; the specific phase implementation is the standard multiplier construction, not confirmed by the abstract.

Abstract evidence: One of the circuits, the controlled weighted sum, can be interpreted as a circuit to compute the inner product of two data vectors.

Equation assumptions:

- Integer w_j,x_j
- N large enough to avoid wraparound if exact S is desired

## Registers

- acc: n (instance: 3) qubits; accumulator held in Fourier basis, holds result modulo 2^n
- x: m per input (instance: 2 inputs, 2 qubits each) qubits; input data register(s)

## Initial state

acc in |0>^n (then QFT applied), x registers in computational basis encoding of x_j, big-endian assumed, unsigned integers

## Measurement

Measure acc in the computational basis to read S mod 2^n.

## Classical postprocessing

Interpret outcome as an integer; two's-complement reinterpretation would be needed for signed results (not specified by the abstract). Any weighted average would require separate division by the sum of weights, not an exact result from this circuit.

## Algorithm steps

1. Apply QFT to acc register. (eq_1)
2. For each input j and each bit of x_j, apply controlled phase rotations on acc scaled by w_j 2^l to accumulate the weighted sum in the phase domain. (eq_2, eq_4)
3. Apply inverse QFT to acc to return to the computational basis, holding S mod N. (eq_3)

## Assumptions

- No scope was provided; chose Draper-style adder plus weighted-sum accumulation as the smallest construction.
- Instance: n=3, two 2-bit inputs, small integer weights.
- Details of the paper's variants were not available from the abstract.

## Missing information

- Exact circuits and rotation schedules of the paper's adders and multipliers
- Signed-integer encoding and handling
- Controlled weighted-sum construction details
- Method for computing the weighted average in the transform domain
- Whether weights are classical or quantum
