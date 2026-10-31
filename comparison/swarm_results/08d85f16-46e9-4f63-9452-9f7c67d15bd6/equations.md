# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reconstruct the abstract's scope: review Quantum Fourier Transform (QFT) adders and multipliers, extend them to modular, non-modular, and signed-integer arithmetic, and use the transform domain for weighted averages and inner products of data vectors.

Scope: Abstract-level reconstruction of QFT-based arithmetic primitives (adder, weighted sum, inner product) for a small finite instance with N = 2^n; no full circuit, multiplier, signed-integer encoding, or experimental details are reconstructed.

## Symbols

- $N$: Dimension of the finite computational basis, assumed N = 2^n; domain: positive integers
- $x$: Integer input encoded in a register; domain: {0,...,N-1}
- $a$: Integer addend encoded as a phase rotation; domain: {0,...,N-1}
- $w_i$: Weight of the i-th input in a weighted average; domain: real numbers
- $x_i$: i-th data input in a series; domain: real numbers

## eq_1: QFT action on a basis state

$$
\mathrm{QFT}|x\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{2\pi i xk/N}|k\rangle
$$

Standard definition of the quantum Fourier transform on a computational basis state.

Provenance: `standard_background`. Standard textbook definition of the QFT; not stated in the abstract.

Equation assumptions:

- N = 2^n for an n-qubit register

## eq_2: Phase-encoded addition in transform domain

$$
|k\rangle\mapsto e^{2\pi i ak/N}|k\rangle \Rightarrow \mathrm{QFT}^{\dagger}\left(e^{2\pi i ak/N}\right)\mathrm{QFT}|x\rangle=|x+a \bmod N\rangle
$$

Standard Fourier-domain adder identity underlying QFT-based addition modulo N.

Provenance: `standard_background`. Standard identity behind QFT adders; the abstract mentions QFT adders but not this formula.

Equation assumptions:

- Phase rotations are applied to the Fourier-transformed register

## eq_3: Weighted average of inputs

$$
\bar{x}=\frac{\sum_{i} w_i x_i}{\sum_{i} w_i}
$$

Classical weighted average that the abstract says is computed in the transform domain.

Provenance: `abstract_inferred`. The abstract names the weighted average target; the explicit formula is the standard definition and is inferred.

Abstract evidence: a quantum method to compute the weighted average of a series of inputs in the transform domain

Equation assumptions:

- Weights are not all zero

## eq_4: Inner product of data vectors

$$
\langle \mathbf{a},\mathbf{b}\rangle=\sum_{i}a_i b_i
$$

Inner product computed by the controlled weighted sum circuit, per the abstract's interpretation.

Provenance: `abstract_inferred`. The abstract gives the inner-product interpretation; the explicit sum form is the standard definition and is inferred.

Abstract evidence: the controlled weighted sum, can be interpreted as a circuit to compute the inner product of two data vectors

Equation assumptions:

- Vectors a and b have equal finite length

## Registers

- x: n qubits; Data register holding the input x in the computational basis, transformed by QFT and returned to the computational basis as x+a mod N
- ctrl: 1 qubits; Assumed control qubit for the controlled weighted sum variant; not specified by the abstract

## Initial state

|x> on the n-qubit data register with x in {0,...,N-1}, and the control qubit in |+> for the controlled variant (assumed)

## Measurement

Computational-basis measurement of the data register after the inverse QFT, repeated over shots to estimate the output distribution; the exact measurement protocol for the weighted average and inner product is not specified by the abstract.

## Classical postprocessing

Classical postprocessing would convert measured outcomes into the estimated modular sum and, for the weighted average, divide by the sum of weights; the exact estimator and its normalization are not specified by the abstract.

## Algorithm steps

1. Apply QFT to the data register to move |x> into the Fourier basis. (eq_1)
2. Apply Fourier-domain phase rotations parameterized by the addend a, which add a modulo N in the transform domain. (eq_2)
3. Apply inverse QFT to return the register to the computational basis, yielding |x+a mod N>. (eq_2)
4. For the weighted average, accumulate weighted phase contributions w_i x_i in the transform domain and target the normalized sum given by the weighted average formula; the exact accumulation circuit is not specified by the abstract. (eq_3)
5. For the controlled weighted sum, condition the accumulation on the control qubit so the resulting sum corresponds to the inner product of the two data vectors; the exact encoding is not specified by the abstract. (eq_4)

## Assumptions

- Finite instance with N = 2^n
- Equations other than those quoted from the abstract are standard background, not claims of the paper
- Control register and measurement protocol are assumed generic constructions, not the paper's circuits
- Measurement and postprocessing are generic reconstructions and not the paper's protocol
- Control register used for the controlled weighted sum is an assumption
- Signed-integer and multiplier constructions are not reconstructed here
- Audit reviewed only the abstract and supplied ledger state; no full paper was consulted
- Equations eq_1 and eq_2 are generic background, not paper-specific claims

## Missing information

- Exact circuit constructions and register sizes for the adders, multipliers, and weighted sum
- Precise handling of modular and signed-integer encodings
- Measurement and postprocessing protocol for the weighted average and inner product
- Full paper details on circuit depth, error, and resource costs are not available from the abstract
- Estimator normalization for weighted average and inner product outputs
- Number of shots and error analysis for the measurement protocol
- Whether the paper's multipliers and signed-integer constructions match the generic reconstruction
