# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Learn a hidden n-bit parity function f_s(x)=s·x mod 2 from a quantum example oracle whose output qubits are depolarized at constant rate, versus classical noisy examples (LPN).

Scope: Smallest useful construction: standard noiseless quantum parity learning via a quantum example state and Hadamard transform, plus a depolarizing channel on the output qubits, for a tiny assumed instance n=3, s=101. The paper's specific noisy-learning algorithm, its complexity bounds, and the LPN hardness/separation arguments are outside this scope.

## Symbols

- $n$: number of input bits; domain: positive integer
- $s$: hidden parity string; domain: {0,1}^n
- $f_s(x)$: parity function s·x mod 2; domain: {0,1}
- $\eta$: depolarizing rate at oracle output; domain: (0,1]
- $\mathcal{D}_\eta$: single-qubit depolarizing channel; domain: CPTP map
- $|\psi_s\rangle$: quantum example state; domain: (C^2)^{\otimes(n+1)}

## eq_1: Parity function

$$
f_s(x)=s\cdot x \bmod 2=\bigoplus_{i=1}^n s_i x_i
$$

Target concept class of n-bit parities.

Provenance: `abstract_inferred`. Parity functions are defined by a hidden string s; the explicit form is standard.

Abstract evidence: learning the class of $n$-bit parity functions

Equation assumptions:

- Parity is s·x mod 2 with no affine offset

## eq_2: Quantum example state

$$
|\psi_s\rangle=\frac{1}{\sqrt{2^n}}\sum_{x\in\{0,1\}^n}|x\rangle|f_s(x)\rangle
$$

Assumed form of a uniform-superposition quantum example.

Provenance: `standard_background`. Standard quantum PAC example oracle for the uniform distribution; the abstract names a quantum example oracle without defining it.

Equation assumptions:

- Uniform input distribution

## eq_3: Noiseless Fourier sampling

$$
H^{\otimes n}\otimes H\,|\psi_s\rangle \;\Rightarrow\; \text{measuring the first } n \text{ qubits gives } s \text{ with probability } 1
$$

Hadamard transform on the n input qubits and the label qubit; the label-qubit measurement yields 1 with probability 1/2, and conditioning on 1 leaves the input register in |s>. Equivalent to Bernstein-Vazirani-style learning.

Provenance: `standard_background`. Background for noiseless quantum parity learning; the abstract says only that noiseless learning is easy.

Equation assumptions:

- Noiseless oracle
- Post-select on the label qubit being 1, or equivalently use the phase-state form

## eq_4: Depolarizing channel

$$
\mathcal{D}_\eta(\rho)=(1-\eta)\rho+\eta\,\frac{I}{2}
$$

Depolarizing noise applied to each oracle output qubit.

Provenance: `assumption`. The abstract states depolarizing at a constant nonzero rate; this parametrization is assumed.

Equation assumptions:

- Independent single-qubit channel on each output qubit
- Parametrization with eta in (0,1]

## eq_5: Classical noisy examples (LPN)

$$
(a,b)\text{ with } a\sim U(\{0,1\}^n),\; b=s\cdot a\oplus e,\; e\sim\mathrm{Bernoulli}(\epsilon)
$$

Classical examples with label noise, the LPN problem.

Provenance: `abstract_inferred`. Standard LPN definition; the noise rate epsilon is not given in the abstract.

Abstract evidence: the problem of learning from corresponding classical examples is the Learning Parity with Noise (LPN) problem

Equation assumptions:

- Uniform examples
- Constant noise rate epsilon in (0,1/2)

## Registers

- X: n (assumed 3) qubits; input register holding x
- B: 1 qubits; label qubit holding f_s(x)

## Initial state

Quantum example state |psi_s> (assumed uniform superposition) prepared by the oracle, then optionally depolarized.

## Measurement

Computational-basis measurement of all qubits after Hadamards (noiseless baseline only).

## Classical postprocessing

Noiseless: read s directly from X when B=1. Noisy case: the paper's postprocessing is not specified in the abstract, so it is omitted here.

## Algorithm steps

1. Query the quantum example oracle to obtain |psi_s> for the assumed instance n=3, s=101. (eq_1, eq_2)
2. Optionally apply depolarizing noise to the output qubits. (eq_4)
3. Apply Hadamards to all qubits and measure; in the noiseless case this reveals s. (eq_3)

## Assumptions

- Uniform quantum example oracle
- Tiny instance n=3, s=101 chosen for illustration
- Depolarizing parametrization in eq_4 assumed

## Missing information

- Paper's noisy quantum learning algorithm and how it handles depolarization
- Exact oracle definition and noise model details
- Sample and query complexity bounds and their dependence on the noise rate
- Details of the LPN separation and the quantum advantage resource estimate
