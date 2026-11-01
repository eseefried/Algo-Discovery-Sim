# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Compute the weighted sum S = sum_j w_j x_j (and, as a variant, the inner product sum_k x_k y_k) into an accumulator register using Draper QFT phase addition, then read the result by inverse QFT and measurement. The weighted average is obtained by classical division by sum_j w_j.

Scope: One smallest construction: a classical-weight weighted sum of k=2 unsigned n=2-bit inputs x_1,x_2 with small non-negative integer weights, in an accumulator of m=n+ceil(log2 k)+(weight headroom) qubits, with basis-state inputs. Signed inputs, the quantum-quantum inner product (CCP), the controlled version and the fixed-point average are described but treated as extensions. Not covered: the paper's exact circuit layouts, resource counts and modular-multiplier variants.

## Symbols

- $n$: bits per input register; domain: positive integer, e.g. 2
- $k$: number of inputs; domain: positive integer, e.g. 2
- $m$: accumulator qubit count; chosen so that no overflow occurs in non-modular mode; domain: positive integer, m >= ceil(log2(1+(2^n-1) sum_j |w_j|))
- $x_j$: j-th input integer, bits x_{j,i} with i=0 least significant; domain: 0..2^n-1 (unsigned) or two's complement
- $w_j$: classical integer weight; domain: integers
- $a$: accumulator computational-basis value, qubit l carries bit l (little-endian); domain: 0..2^m-1
- $\phi(a)$: QFT (no swaps) image of |a>; domain: m-qubit state
- $l$: accumulator qubit index; domain: 0..m-1

## eq_1: Fourier-basis accumulator state (no swaps)

$$
\mathrm{QFT}|a\rangle=\bigotimes_{l=0}^{m-1}\frac{|0\rangle+e^{2\pi i a/2^{l+1}}|1\rangle}{\sqrt2}
$$

Qubit l carries phase exp(2 pi i a/2^(l+1)) (up to qubit-order convention).

Provenance: `standard_background`. Standard QFT product form, as in the Draper adder; the sketch states this.

Equation assumptions:

- No swap gates
- Little-endian: qubit l has weight 2^l in a

## eq_2: Draper addition by controlled phases

$$
\prod_{i,l}CP_{x_i\to l}\!\left(\frac{2\pi\,2^{i}}{2^{l+1}}\right)\,|\phi(a)\rangle|x\rangle=|\phi(a+x \bmod 2^m)\rangle|x\rangle
$$

Controlled phases from each bit x_i onto each accumulator qubit l add x to a in the Fourier domain, modulo 2^m.

Provenance: `abstract_inferred`. The abstract only says QFT arithmetic with adders exists; the exact angles are the standard Draper construction.

Abstract evidence: The Quantum Fourier Transform offers an interesting way to perform arithmetic operations on a quantum computer.

Equation assumptions:

- Angles for angle>=2 pi can be reduced mod 2 pi

## eq_3: Weighted-sum phase angles

$$
\theta_{j,i,l}=\frac{2\pi\,w_j\,2^{i}}{2^{l+1}},\quad |\phi(0)\rangle\to|\phi(S \bmod 2^m)\rangle,\ S=\sum_j w_j x_j
$$

Multiplying each angle by the classical weight w_j accumulates the weighted sum; a negative w_j gives subtraction.

Provenance: `abstract_inferred`. The weighted sum in the transform domain follows from phase additivity; the explicit angle schedule is the standard multiply-by-constant extension.

Abstract evidence: we discuss a quantum method to compute the weighted average of a series of inputs in the transform domain

Equation assumptions:

- Integer weights, so that the angles are exact

## eq_4: Inner product via doubly controlled phases

$$
\theta_{i,j,l}=\frac{2\pi\,2^{i+j}}{2^{l+1}}\ \text{(CCP from } x_i,y_j\text{ to qubit }l),\quad a\to a+\sum_k x_k y_k \bmod 2^m
$$

Quantum-quantum multiply-accumulate; repeating over vector entries k gives the inner product.

Provenance: `abstract_inferred`. The inner-product reading of the controlled weighted sum implies product-of-bits controlled phases; this is the extension variant.

Abstract evidence: One of the circuits, the controlled weighted sum, can be interpreted as a circuit to compute the inner product of two data vectors.

Equation assumptions:

- Out of scope for the smallest instance

## eq_5: Readout and weighted average

$$
\mathrm{QFT}^{-1}|\phi(S \bmod 2^m)\rangle=|S \bmod 2^m\rangle,\quad \bar x=\frac{S}{\sum_j w_j}
$$

Inverse QFT then measurement gives S exactly if there is no overflow; the average is computed classically and is exact only as a rational. An integer quotient would be floor or rounded.

Provenance: `standard_background`. Inverse QFT is the exact inverse; the division is classical post-processing.

Equation assumptions:

- S < 2^m for non-modular mode
- Nonzero weight sum

## Registers

- x_j: n each, j=1..k qubits; input data, unchanged, used as controls
- A: m qubits; accumulator, starts |0>, ends holding S mod 2^m

## Initial state

A in |0...0>; each x_j in a computational basis state (or superposition); no ancillas.

## Measurement

Measure A (m bits) in the computational basis after inverse QFT. In Qiskit counts keys, the last character is accumulator bit 0 (qubit 0 is the least significant bit).

## Classical postprocessing

Read S as an integer from the bitstring; for signed mode, interpret in two's complement mod 2^m. Compute the average S/sum(w_j), exactly or as a rational, noting that floor or fixed-point truncation is approximate.

## Algorithm steps

1. Apply QFT without swaps to A. (eq_1)
2. For each j, i, l apply CP(theta_{j,i,l}) controlled by x_{j,i} on A qubit l; for signed inputs negate the angle of the MSB (weight -2^(n-1)). (eq_2, eq_3)
3. Apply inverse QFT (no swaps) to A and measure only A. (eq_5)
4. Classically divide S by the sum of weights for the weighted average. (eq_5)

## Assumptions

- Chosen instance: k=2, n=2, small non-negative weights, unsigned inputs, basis-state inputs.
- Qubits fit the cap: 2n+m, e.g. 4+5=9.
- The QFT swaps are omitted consistently in the QFT and inverse QFT.

## Missing information

- The paper's exact circuit layouts, gate counts and the fixed-point weighted-average scheme.
- How the controlled and signed variants are arranged in the paper.
- The qubit cap and the instances are not given.
