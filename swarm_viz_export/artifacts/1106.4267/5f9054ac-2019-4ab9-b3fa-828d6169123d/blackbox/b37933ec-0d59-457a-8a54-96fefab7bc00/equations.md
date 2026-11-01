# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate the mean a=(1/N)sum_x f(x) of a bounded function f:{0,...,N-1}->[0,1] with standard quantum amplitude estimation, with f compiled from an explicit classical table into controlled rotations. This is a standard-background stand-in for the abstract's mean-estimation goal.

Scope: Tiny explicit instance (assumed): N=4, n=2 index qubits, 1 ancilla qubit, t phase qubits. Only the amplitude-estimation unitary is built, with no measurement. The paper's novel optimal algorithm, the Aharonov-variant algorithm and the median-finding algorithm are out of scope. No black-box query complexity is certified.

## Symbols

- $N=2^n$: number of domain points; domain: positive integer power of 2
- $f(x)$: bounded function value, given as an explicit classical table; domain: [0,1]
- $a$: mean of f, the target quantity; domain: [0,1]
- $\theta$: angle with sin^2(theta)=a; domain: [0,\pi/2]
- $t$: number of phase-estimation qubits; domain: positive integer
- $y$: integer read from the phase register; domain: {0,...,2^t-1}
- $A$: state-preparation unitary: Hadamards on the index register followed by U_f; domain: unitary on n+1 qubits
- $Q$: Grover iterate of amplitude estimation; domain: unitary on n+1 qubits

## eq_1: Oracle rotation

$$
U_f|x\rangle|0\rangle=|x\rangle\left(\sqrt{1-f(x)}|0\rangle+\sqrt{f(x)}|1\rangle\right),\quad R_y(2\arcsin\sqrt{f(x)})
$$

Controlled Y-rotation on the ancilla for each index x, with angles taken from the explicit table.

Provenance: `assumption`. Proposed standard construction for encoding the mean as an amplitude. The abstract does not specify it.

Equation assumptions:

- f is given explicitly and compiled into gates
- the oracle is not opaque

## eq_2: State preparation

$$
A|0\rangle=\frac{1}{\sqrt N}\sum_x|x\rangle\left(\sqrt{1-f(x)}|0\rangle+\sqrt{f(x)}|1\rangle\right),\quad a=\|(I\otimes|1\rangle\langle1|)A|0\rangle\|^2=\frac1N\sum_x f(x)
$$

The probability of ancilla=1 equals the mean of f.

Provenance: `standard_background`. Direct computation from eq_1 and the uniform superposition.

Equation assumptions:

- N is a power of 2

## eq_3: Grover iterate

$$
Q=-A S_0 A^\dagger S_\chi,\quad S_\chi=I\otimes Z_{anc},\quad S_0=I-2|0\rangle\langle0|,\quad Q\text{ has eigenphases }e^{\pm i2\theta},\ \sin^2\theta=a
$$

Amplitude-amplification iterate. Its eigenphases encode the mean a.

Provenance: `standard_background`. Standard amplitude estimation (Brassard et al.).

Equation assumptions:

- global sign conventions are fixed as written; S_chi marks the ancilla=1 component

## eq_4: Phase estimation circuit

$$
U_{AE}=(QFT_{2^t}^{-1}\otimes I)\left(\sum_{k=0}^{2^t-1}|k\rangle\langle k|\otimes Q^k\right)(H^{\otimes t}\otimes A)
$$

Unitary acting on the phase register and the n+1 system qubits, starting from |0>. Controlled-Q^(2^j) is controlled by phase qubit j.

Provenance: `standard_background`. Standard amplitude estimation circuit.

Equation assumptions:

- the phase register is little-endian, so qubit j has weight 2^j
- the inverse QFT matches this convention

## eq_5: Decoding and error

$$
\hat a=\sin^2(\pi y/2^t),\quad |\hat a-a|\le\frac{2\pi\sqrt{a(1-a)}}{2^t}+\frac{\pi^2}{4^t}\text{ with probability}\ge 8/\pi^2
$$

Classical decoding of the measured y and the standard error bound.

Provenance: `standard_background`. Standard amplitude estimation theorem. It gives O(1/epsilon) applications of A for additive error epsilon.

Equation assumptions:

- the bound applies to ideal simulation
- the paper's own algorithm may use a different method

## Registers

- idx: n=log2 N (2 in the tiny instance) qubits; index register, initialised with Hadamards
- anc: 1 qubits; ancilla holding the f-amplitude flag
- phase: t (3 assumed) qubits; phase-estimation register

## Initial state

All qubits in |0>, ordered phase, idx, anc.

## Measurement

Not part of the circuit. Measure the phase register in the computational basis and read y.

## Classical postprocessing

a_hat = sin^2(pi*y/2^t). Both y and 2^t-y give the same estimate.

## Algorithm steps

1. Apply H on the phase register. Apply H on idx, then U_f (controlled R_y on anc for each x) to build A. (eq_1, eq_2)
2. Build Q = -A S_0 A^dagger S_chi. (eq_3)
3. Apply controlled-Q^(2^j) from phase qubit j, for j=0..t-1. (eq_3, eq_4)
4. Apply the inverse QFT on the phase register. (eq_4)
5. Outside the unitary, measure the phase register to get y and compute a_hat. (eq_5)

## Assumptions

- Choice of standard amplitude estimation as the construction, and N=4, t=3 as the tiny instance, is mine.
- f values are compiled into gates, so the circuit is not black-box and no query complexity is certified.

## Missing information

- The paper's novel asymptotically optimal algorithm is not specified in the abstract.
- The Aharonov-variant algorithm is not specified.
- The median algorithm over an arbitrary distance function is not specified.
