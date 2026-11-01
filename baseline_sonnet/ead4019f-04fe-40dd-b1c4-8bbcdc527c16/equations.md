# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Fixed-point amplitude amplification: given a state preparation A with |psi>=A|0>=sqrt(lambda)|good>+sqrt(1-lambda)|bad>, and only a lower bound lambda_0 <= lambda, boost success probability to at least 1-delta^2 (adjustable failure bound) for all lambda in a range, using O(1/sqrt(lambda_0)) oracle queries (quadratic speedup).

Scope: Background-only reconstruction of the standard amplitude amplification setting and the failure-probability criterion, plus a tiny explicit Grover-iterate instance (one step, lambda=1/4). The paper's specific fixed-point construction with quadratic speedup (its phase schedule and range-optimality guarantee) is outside scope and not reconstructed.

## Symbols

- $\lambda$: initial overlap fraction (success probability) of target states in the initial state; domain: (0,1]
- $\lambda_0$: known lower bound on lambda; domain: (0,\lambda]
- $\delta^2$: adjustable bound on failure probability; domain: (0,1)
- $L$: number of oracle queries (amplification steps); domain: nonnegative integers
- $\theta$: angle with sin^2(theta)=lambda; domain: (0,\pi/2]
- $|\psi\rangle$: initial state A|0>; domain: normalized state
- $|g\rangle,|b\rangle$: normalized good and bad components; domain: orthonormal states
- $G$: standard Grover/amplification iterate; domain: unitary

## eq_1: Initial decomposition

$$
|\psi\rangle=A|0\rangle=\sqrt{\lambda}\,|g\rangle+\sqrt{1-\lambda}\,|b\rangle=\sin\theta\,|g\rangle+\cos\theta\,|b\rangle
$$

Initial state split into target and non-target parts with fraction lambda

Provenance: `abstract_inferred`. The abstract defines lambda as the target fraction; the amplitude form is the standard interpretation.

Abstract evidence: what fraction $\lambda$ of the initial state is comprised of the target states

Equation assumptions:

- lambda is a probability (squared amplitude)

## eq_2: Standard Grover iterate

$$
G=-A S_0 A^{\dagger} S_g,\quad S_g=I-2|g\rangle\langle g|\text{ (oracle)},\quad S_0=I-2|0\rangle\langle 0|
$$

Standard amplitude amplification iterate, one oracle query per application

Provenance: `standard_background`. Textbook amplitude amplification; not the paper's fixed-point operator.

Equation assumptions:

- Oracle marks good states by phase flip

## eq_3: Standard amplification success probability

$$
P_L=\sin^2\big((2L+1)\theta\big),\ \sin^2\theta=\lambda
$$

Success probability after L Grover iterations; oscillates and overshoots if lambda is unknown

Provenance: `standard_background`. Standard result; illustrates why plain Grover is hard to use without knowing lambda.

Equation assumptions:

- Exact Grover iterate with pi phases

## eq_4: Fixed-point requirement

$$
1-P_L(\lambda)\le\delta^2\quad\forall\,\lambda\in[\lambda_0,1],\ L=O(\lambda_0^{-1/2}\log(1/\delta))
$$

Target property: failure bound satisfied for all lambda above the lower bound, with a quadratic-speedup query count. The log(1/delta) scaling is a typical form, not claimed by the abstract.

Provenance: `abstract_inferred`. Abstract states adjustable failure bound and quadratic advantage with a lower bound on lambda; the exact query count and range are not given.

Abstract evidence: need only a reliable lower bound on this fraction

Equation assumptions:

- Range [lambda_0,1] and query scaling form are assumed, not stated; the abstract claims the broadest possible range for a given query count

## eq_5: Tiny instance

$$
\lambda=1/4\Rightarrow\theta=\pi/6,\ P_1=\sin^2(\pi/2)=1
$$

One standard Grover iteration on an instance with lambda=1/4 gives success probability 1

Provenance: `assumption`. Smallest illustrative instance for later circuit generation.

Equation assumptions:

- Chosen purely as an illustrative instance

## Registers

- search: n (symbolic) qubits; holds the state A|0>, oracle acts on it
- oracle_flag: unknown qubits; possible ancilla for marking, not specified in the abstract

## Initial state

A|0> on the search register (assumed).

## Measurement

Measure the search register (or oracle flag) in the computational basis and test for a target state.

## Algorithm steps

1. Prepare |psi>=A|0>. (eq_1)
2. Apply the standard iterate G; the paper's fixed-point scheme would replace it with a specific unspecified schedule. (eq_2, eq_3)
3. Check the requirement against the failure bound over the lambda range. (eq_4)
4. Tiny instance check with lambda=1/4. (eq_5)

## Assumptions

- Standard amplitude amplification setting with oracle S_g and preparation A
- Tiny instance lambda=1/4 chosen as illustration
- The paper's actual fixed-point construction is not reconstructed

## Missing information

- Phase schedule or modified iterate for fixed-point amplification with quadratic speedup
- Exact query count as a function of lambda_0 and delta
- Exact range of lambda guaranteed and the optimality argument
- Oracle and ancilla layout
