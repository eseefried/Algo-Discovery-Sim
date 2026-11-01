# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate the mean value of a black-box function f over N inputs on a quantum computer; the abstract also mentions a median-approximation algorithm over an arbitrary distance function, but gives no details.

Scope: Only a generic textbook baseline for mean estimation on a tiny instance: amplitude estimation of the acceptance probability, which equals the mean for f with values in [0,1]. The abstract's novel optimal algorithm, the Aharonov-variant algorithm, and the median algorithm are outside this scope and not reconstructed.

## Symbols

- $N=2^n$: number of inputs; domain: positive integer power of 2
- $f$: black-box function; domain: f:{0,...,N-1}->[0,1]
- $\mu$: mean value of f; domain: [0,1]
- $\epsilon$: additive error target; domain: (0,1)
- $\theta$: amplitude angle with sin^2(theta)=mu; domain: [0,\pi/2]
- $m$: number of phase estimation qubits; domain: positive integer

## eq_1: Mean value

$$
\mu=\frac{1}{N}\sum_{x=0}^{N-1} f(x)
$$

Quantity to approximate

Provenance: `abstract_inferred`. Standard definition of the mean value of f over a finite domain; the abstract does not state the domain or range.

Abstract evidence: approximate the mean value of a black-box function

Equation assumptions:

- Finite uniform domain of size N
- f takes values in [0,1]

## eq_2: State preparation oracle

$$
A|0\rangle^{n}|0\rangle=\frac{1}{\sqrt N}\sum_x |x\rangle\left(\sqrt{1-f(x)}|0\rangle+\sqrt{f(x)}|1\rangle\right)
$$

Encodes f(x) in the amplitude of a flag qubit

Provenance: `assumption`. Proposed standard construction; the paper's actual oracle model is unknown.

Equation assumptions:

- Controlled rotation by angle 2arcsin sqrt(f(x)) is available through the oracle

## eq_3: Success probability equals mean

$$
\sin^2\theta=\Pr[\text{flag}=1]=\mu
$$

Flag-1 probability equals the mean

Provenance: `standard_background`. Follows from eq_2 by direct computation.

Equation assumptions:

- eq_2 holds

## eq_4: Grover iterate eigenphases

$$
Q=-A S_0 A^{\dagger} S_{\chi},\quad Q\text{ has eigenvalues }e^{\pm 2i\theta}
$$

Amplitude-estimation operator whose phase encodes theta

Provenance: `standard_background`. Brassard-Hoyer-Mosca-Tapp amplitude estimation background.

Equation assumptions:

- S_chi flips the sign of flag=1
- S_0 flips the sign of the all-zero state

## eq_5: Error bound of amplitude estimation

$$
|\tilde\mu-\mu|\le \frac{2\pi\sqrt{\mu(1-\mu)}}{M}+\frac{\pi^2}{M^2},\; M=2^m
$$

Standard error bound with O(1/epsilon) uses of A, success probability at least 8/pi^2

Provenance: `standard_background`. Textbook amplitude estimation result, not the paper's claimed result.

Equation assumptions:

- Ideal noiseless execution

## Registers

- x: n qubits; input index register
- flag: 1 qubits; stores f(x) in amplitude
- phase: m qubits; phase estimation register for amplitude estimation

## Initial state

All-zero state |0>^m |0>^n |0>; assumed tiny instance n=2, N=4, f values chosen by the user.

## Measurement

Measure the phase register in the computational basis, giving integer y in {0,...,2^m-1}.

## Classical postprocessing

Compute tilde mu = sin^2(pi y / 2^m); this is an approximation to mu within the bound in eq_5, not an exact equality.

## Algorithm steps

1. Prepare uniform superposition over x and rotate the flag by f(x) using the oracle to form A|0>. (eq_2, eq_3)
2. Apply Hadamards on the phase register, controlled powers Q^(2^j), and the inverse QFT. (eq_4)
3. Measure the phase register to get y and estimate the mean. (eq_5)

## Assumptions

- Generic amplitude estimation is used as a baseline since the abstract gives no algorithm details
- f values in [0,1] with an amplitude-encoding oracle

## Missing information

- Details of the novel asymptotically optimal mean algorithm
- Details of the Aharonov-variant algorithm and its caveats
- Error model, oracle model, and complexity statements of the paper
- Median approximation algorithm and distance function formalism
