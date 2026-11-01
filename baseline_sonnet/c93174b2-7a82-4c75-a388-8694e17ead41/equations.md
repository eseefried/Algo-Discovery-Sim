# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Model how imperfect gate operations (systematic, random, combined errors) affect the success of Shor's factoring algorithm for a number N. The abstract gives only qualitative conclusions, so only a generic background error model on a tiny instance can be reconstructed.

Scope: Single tiny instance (assumed N=15, a=7) of the order-finding core with an assumed rotation-angle error model on the controlled-phase gates of the QFT. The paper's actual error models, threshold formula, and numerical results are outside scope and not reconstructed.

## Symbols

- $N$: Integer to be factored; domain: positive composite integer; assumed N=15
- $a$: Base coprime to N; domain: 1<a<N, gcd(a,N)=1; assumed a=7
- $r$: Multiplicative order of a modulo N; domain: positive integer
- $t$: Number of counting qubits; domain: positive integer; assumed t=8
- $Q$: Counting register dimension 2^t; domain: positive integer
- $\theta_k$: Ideal controlled-phase angle 2\pi/2^k; domain: real
- $\epsilon$: Systematic angle error, same for all gates; domain: real
- $\delta_j$: Random angle error of gate j, e.g. zero-mean with variance \sigma^2; domain: real
- $U_a$: Modular multiplication unitary |y> -> |ay mod N>; domain: unitary on n=ceil(log2 N) qubits

## eq_1: Order definition

$$
a^r \equiv 1 \pmod N,\quad r=\min\{k>0\}
$$

Order finding target of Shor's algorithm.

Provenance: `standard_background`. Standard Shor background; the abstract names the algorithm only.

Equation assumptions:

- gcd(a,N)=1

## eq_2: Ideal output state before measurement

$$
\frac{1}{Q}\sum_{x=0}^{Q-1}\sum_{y=0}^{Q-1} e^{2\pi i xy/Q}|y\rangle|a^x \bmod N\rangle
$$

State after modular exponentiation and ideal QFT on the counting register.

Provenance: `standard_background`. Textbook Shor construction.

Equation assumptions:

- Register ordering: counting register first, work register second; integers in binary, MSB first

## eq_3: Perturbed gate model

$$
\tilde\theta_{k,j}=\theta_k+\epsilon+\delta_j,\quad \mathbb{E}[\delta_j]=0,\ \mathrm{Var}[\delta_j]=\sigma^2
$$

Assumed model: systematic error adds constant epsilon; random error adds independent noise delta_j; combined has both.

Provenance: `assumption`. The abstract names the three error categories but gives no parametrization; this is a proposed model.

Equation assumptions:

- Errors act on controlled-phase angles of the QFT
- Gaussian or similar independent noise

## eq_4: Success probability

$$
P_{\mathrm{succ}}(\epsilon,\sigma)=\sum_{y\in\mathcal{G}}\Pr(y\mid\tilde\theta),\quad \mathcal{G}=\{y:\ |y/Q-s/r|\le 1/(2Q)\text{ for some }s\}
$$

Probability of measuring a counting value that yields r by continued fractions, under the perturbed gates.

Provenance: `assumption`. Proposed figure of merit to compare robustness; the paper's own metric is unknown.

Equation assumptions:

- Threshold defined as the error level where P_succ drops below a chosen value

## eq_5: Factor extraction

$$
p,q=\gcd(a^{r/2}\pm1,N)
$$

Nontrivial factors from an even order r with a^{r/2} not congruent to -1 mod N.

Provenance: `standard_background`. Standard classical postprocessing.

Equation assumptions:

- r even and a^{r/2}\not\equiv -1 \pmod N

## Registers

- counting: t=8 qubits; Phase estimation register measured after QFT
- work: 4 qubits; Holds a^x mod N for N=15

## Initial state

Counting register in |0>^{t} then Hadamards to uniform superposition; work register |1>.

## Measurement

Computational-basis measurement of the counting register.

## Classical postprocessing

Continued-fraction expansion of y/Q to get r, then gcd computation for factors (eq_5).

## Algorithm steps

1. Prepare uniform superposition on the counting register and set the work register to |1>. (no equation reference)
2. Apply controlled modular exponentiation (ideal) to get sum_x |x>|a^x mod N>. (eq_2)
3. Apply the QFT with perturbed controlled-phase angles according to the assumed error model. (eq_3)
4. Measure the counting register and evaluate the success probability over error parameters to find a threshold. (eq_4)
5. Recover r by continued fractions and compute factors. (eq_1, eq_5)

## Assumptions

- N=15, a=7 (r=4), t=8 chosen as the tiny instance
- Errors are confined to QFT phase gates; modular exponentiation assumed ideal
- The error model and success metric are proposals, not from the abstract

## Missing information

- Actual error model parametrization of the paper
- Which gates are affected and how errors enter
- The threshold formula as a function of N
- Quantitative results and scaling of robustness
- Circuit implementation used for modular exponentiation
