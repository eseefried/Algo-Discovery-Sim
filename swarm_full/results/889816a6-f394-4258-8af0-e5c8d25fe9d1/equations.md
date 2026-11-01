# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reconstruct QFT-based (Draper-style) quantum arithmetic: adders and multipliers, modular and non-modular, with signed integers, including a controlled weighted sum that computes a weighted average or inner product of data vectors in the transform domain.

Scope: Small finite instance: QFT adder of a classical constant or register into a register, and a controlled weighted sum as an inner-product accumulator. Only the abstract's qualitative claims are supported; circuit details are background or assumed.

## Symbols

- $n$: number of qubits in the target register; domain: positive integer
- $a, b$: integer operands; domain: integers mod 2^n (two's complement for signed)
- $\mathrm{QFT}$: quantum Fourier transform on n qubits; domain: unitary on 2^n-dim space
- $w_i, x_i$: weights and data inputs of the weighted sum; domain: integers

## eq_1: QFT definition

$$
\mathrm{QFT}|b\rangle=\frac{1}{\sqrt{2^n}}\sum_{k=0}^{2^n-1}e^{2\pi i bk/2^n}|k\rangle
$$

Fourier-basis encoding of integer b

Provenance: `standard_background`. Standard QFT definition underlying QFT arithmetic; the abstract only names the QFT.

Equation assumptions:

- Standard convention for the QFT

## eq_2: QFT addition

$$
\mathrm{QFT}^{-1}\,\Phi(a)\,\mathrm{QFT}|b\rangle=|(a+b)\bmod 2^n\rangle
$$

Addition by phase rotations in the transform domain

Provenance: `standard_background`. Standard Draper adder; the abstract says QFT adders are reviewed but gives no formula.

Equation assumptions:

- Phi(a) is the diagonal phase-rotation unitary with entries exp(2 pi i a k/2^n)

## eq_3: Controlled weighted sum

$$
|x\rangle|0\rangle\mapsto|x\rangle\left|\textstyle\sum_i w_i x_i \bmod 2^n\right\rangle
$$

Inner product of weight vector and data vector accumulated in the output register

Provenance: `abstract_inferred`. The abstract states the inner-product interpretation; the exact form is inferred.

Abstract evidence: the controlled weighted sum, can be interpreted as a circuit to compute the inner product of two data vectors

Equation assumptions:

- Modular arithmetic mod 2^n
- Weights classical

## Registers

- x: m*n qubits (m data inputs of n qubits each, assumed) qubits; data register holding inputs x_i, used as controls
- acc: n qubits; accumulator register for the sum, held in Fourier basis during accumulation

## Initial state

|x>|0>^n with x a computational-basis data input and acc initialized to zero (assumed)

## Measurement

After the inverse QFT, measure acc (n qubits) in the computational basis. For a computational-basis input the outcome is deterministic and encodes S = sum w_i x_i mod 2^n. For superposed inputs, outcomes are sampled according to input amplitudes, and x can be measured jointly. Shot count is assumed and unspecified.

## Classical postprocessing

Convert the bitstring to an integer S in [0,2^n); for signed values use two's complement. The result is valid only if 2^n exceeds the range of the true sum. For a weighted average, divide S by the sum of weights (or shift if weights are pre-scaled to sum to 2^k); this is an assumed procedure. For superposed inputs, histogram over shots.

## Algorithm steps

1. Apply QFT on the accumulator register acc to enter the transform domain. (eq_1)
2. For each i and each bit j of x_i, apply a controlled phase rotation on acc by angle 2*pi*w_i*2^j/2^n, controlled on bit j of x_i, so the phase accumulates sum w_i x_i (assumed Draper-style construction). (eq_2, eq_3)
3. Apply inverse QFT on acc to return to the computational basis, giving |x>|sum w_i x_i mod 2^n>, i.e. the inner product. (eq_1, eq_3)

## Assumptions

- Draper-style QFT adder underlies the paper's circuits
- Finite small n for illustration
- Weights w_i are classical constants compiled into rotation angles
- Signed integers use two's complement mod 2^n
- Weighted average needs separate normalization, e.g. weights pre-scaled to sum to a power of 2 (assumed)
- Measurement is in the computational basis of acc after the inverse QFT; shot count unspecified
- Overflow is avoided by choosing n large enough for the true sum range
- Multiplier and modular variants are not reconstructed; only the weighted-sum instance is covered

## Missing information

- Exact circuits for modular, signed, and multiplier variants
- Weighted-average normalization procedure
- Gate-level details of the controlled weighted sum and modular variants are not in the abstract
- The abstract does not describe measurement or readout, nor whether the weighted average is read in the transform domain or after the inverse QFT
- The abstract gives no shot counts or error analysis
