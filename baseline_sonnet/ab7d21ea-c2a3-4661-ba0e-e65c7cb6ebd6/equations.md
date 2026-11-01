# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Given N=p1 p2 and a coprime to N, find the order r (smallest r with a^r mod N = 1) via quantum order finding, then extract factors via gcds, including the case of odd r when a is a perfect square, which the abstract identifies as sometimes giving factors.

Scope: Minimal scoped construction: the classical number-theoretic relations of order-based factoring (even r, and odd r with square coprime a), plus the standard textbook phase-estimation form of order finding on the tiny instance N=15, a=4 (odd-order-type case with square coprime; order 2 is even, so a 4-style example is only illustrative). Outside the scope: the paper's two specific techniques (not discarding odd orders; searching for new order-finding relations after failure), the success-probability analysis, and any quantitative improvement estimates.

## Symbols

- $N$: number to factor, N=p_1 p_2; domain: positive integer, composite
- $a$: randomly chosen base coprime to N; domain: integer, 1<a<N, gcd(a,N)=1
- $r$: multiplicative order of a modulo N; domain: positive integer
- $b$: square root of a when a=b^2 is a perfect square; domain: positive integer
- $n$: number of counting qubits; domain: positive integer, 2^n >= N^2 (standard choice)
- $\varphi$: phase s/r estimated by phase estimation; domain: [0,1)
- $U_a$: modular multiplication unitary |y> -> |ay mod N>; domain: unitary on ceil(log2 N) qubits

## eq_1: Order definition

$$
r=\min\{k\in\mathbb{Z}_{>0}:a^{k}\equiv 1 \pmod N\},\quad \gcd(a,N)=1
$$

Definition of the order to be found by the QOFA.

Provenance: `abstract_explicit`. The abstract defines the order this way.

Abstract evidence: the smallest integer, $r$, satisfying $a^{r}\mod N=1$

## eq_2: Factors from even order

$$
p_1=\gcd(a^{r/2}-1,N),\quad p_2=\gcd(a^{r/2}+1,N)
$$

Factor extraction given even r; succeeds with probability at least 1/2 over random a, and may fail for some a (trivial factors).

Provenance: `abstract_explicit`. Stated in the abstract; the success probability is also stated there.

Abstract evidence: $p_{1}=\gcd(a^{\frac{r}{2}}-1,N)$ and $p_{2}=\gcd(a^{\frac{r}{2}}+1,N)$

Equation assumptions:

- r even
- a^{r/2} not congruent to -1 mod N for nontrivial factors

## eq_3: Odd order with square coprime

$$
a=b^{2},\ r\ \text{odd}\ \Rightarrow\ a^{r/2}=b^{r}\in\mathbb{Z},\quad p_{1,2}\ \text{candidates}=\gcd(b^{r}\mp1,N)
$$

If a is a perfect square, a^{r/2}=b^r is an integer even for odd r, so the gcd formulas can be evaluated; the factors are only sometimes nontrivial.

Provenance: `abstract_inferred`. Inferred from this claim: for a=b^2, a^{r/2}=b^r is an integer. The detailed form is my inference, not the paper's.

Abstract evidence: the factors can sometimes be found from odd orders if the coprime is square

Equation assumptions:

- a is a perfect square b^2
- nontriviality of gcds is not guaranteed

## eq_4: Phase estimation output for order finding

$$
\frac{1}{2^{n}}\sum_{x=0}^{2^{n}-1}\sum_{y=0}^{2^{n}-1}e^{2\pi i xy/2^{n}}|y\rangle|a^{x}\bmod N\rangle \ \Rightarrow\ \frac{y}{2^{n}}\approx\frac{s}{r}
$$

Textbook QOFA: measured y/2^n approximates s/r for random s in {0..r-1}; r recovered by continued fractions. Approximation, not exact equality, unless r divides 2^n.

Provenance: `standard_background`. Standard Shor order-finding background; the abstract does not give these details.

Equation assumptions:

- Standard QFT-based phase estimation
- 2^n >= N^2

## eq_5: Continued fraction recovery

$$
\left|\frac{y}{2^{n}}-\frac{s}{r}\right|\le\frac{1}{2^{n+1}}\ \Rightarrow\ \frac{s}{r}\ \text{is a continued-fraction convergent of}\ \frac{y}{2^{n}}
$$

Classical postprocessing to get a candidate r (denominator, possibly a divisor of r if gcd(s,r)>1).

Provenance: `standard_background`. Standard background; the paper's own relaxation/new-relation techniques are not reconstructed.

Equation assumptions:

- 2^n >= 2r^2 roughly

## Registers

- counting: n qubits (assumed 2^n >= N^2) qubits; phase estimation register holding x, then y after the QFT
- work: ceil(log2 N) qubits qubits; holds a^x mod N

## Initial state

|0>^{⊗n}|1> (counting register all zeros, work register encoding integer 1 in binary, little-endian assumed), then Hadamards on counting register.

## Measurement

Measure the counting register in the computational basis to obtain y; the work register may be left unmeasured.

## Classical postprocessing

Continued fraction expansion of y/2^n, order verification, then the gcd computations of eq_2 or eq_3; repeat with new a on failure.

## Algorithm steps

1. Choose a coprime to N (check gcd(a,N)=1); note whether a is a perfect square. (eq_1)
2. Prepare uniform superposition on counting register and apply controlled modular exponentiation to the work register. (eq_4)
3. Apply inverse QFT to the counting register and measure it to obtain y. (eq_4)
4. Use continued fractions on y/2^n to obtain candidate r; verify a^r mod N = 1. (eq_5, eq_1)
5. If r even, compute gcds; if r odd and a=b^2, compute gcds with b^r; otherwise relaunch with a different a. (eq_2, eq_3)

## Assumptions

- The scope is restricted to the standard QOFA plus the odd-order/square-coprime relation; the paper's two techniques are not reconstructed.
- Counting register size 2^n >= N^2 is a standard choice, not from the abstract.
- A tiny instance such as N=15 is suggested only for later testing; the abstract specifies none.

## Missing information

- The precise method for retrieving the order from odd-order runs and for finding new order-finding relations after failure.
- Quantitative success probability improvement and efficiency equivalence derivation.
- The specific circuits or instances used in the paper.
