# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Estimate the influence of each variable x_i on an n-variable Boolean function f using one-shot runs of the Bernstein-Vazirani circuit, where Pr[y_i=1] equals the influence of x_i on f.

Scope: Single construction: the standard Bernstein-Vazirani circuit applied to a generic f:{0,1}^n->{0,1}, with the per-position output probability Pr[y_i=1] identified with the influence, and a sampling estimator. Tiny instance: n=2, f(x)=x_1 AND x_2 (an assumption). Out of scope: the junta-learning algorithms, their complexity and speedup comparison against Floess et al., and the paper's own error analysis.

## Symbols

- $n$: number of input variables; domain: positive integer
- $f$: Boolean function; domain: {0,1}^n -> {0,1}
- $\hat f(s)$: Fourier coefficient of (-1)^{f}; domain: real, s in {0,1}^n
- $y$: measured n-bit output string; domain: {0,1}^n
- $\mathrm{Inf}_i(f)$: influence of x_i on f; domain: [0,1]
- $N$: number of circuit runs for estimation; domain: positive integer

## eq_1: Output distribution of BV circuit

$$
\Pr[y=s]=\hat f(s)^2,\quad \hat f(s)=2^{-n}\sum_{x\in\{0,1\}^n}(-1)^{f(x)+s\cdot x}
$$

Measurement distribution after H^{\otimes n}, the phase oracle, then H^{\otimes n} on |0^n>.

Provenance: `standard_background`. Standard Fourier-sampling analysis of the Bernstein-Vazirani circuit; not stated in the abstract.

Equation assumptions:

- Phase oracle (-1)^{f(x)}
- Ancilla in |-> or equivalent phase kickback

## eq_2: Influence definition

$$
\mathrm{Inf}_i(f)=\Pr_{x}[f(x)\neq f(x\oplus e_i)]
$$

Standard influence of variable x_i with x uniform on {0,1}^n.

Provenance: `standard_background`. The abstract equates the 'dependence degree' with the influence, but it does not give the formula; this is the standard definition.

Equation assumptions:

- Uniform distribution over x

## eq_3: Probability of 1 at position i equals influence

$$
\Pr[y_i=1]=\sum_{s:\,s_i=1}\hat f(s)^2=\mathrm{Inf}_i(f)
$$

Marginal probability of a 1 in position i of the BV output equals the influence of x_i.

Provenance: `abstract_explicit`. The equality with influence is the abstract's claim. The middle expression follows from eq_1, and the equality with the influence definition is standard Fourier analysis.

Abstract evidence: the probability of getting a 1 in each position $i$ is equal to the dependence degree of $f$ on the variable $x_{i}$, i.e. the influence of $x_{i}$ on $f$

Equation assumptions:

- Influence is as in eq_2

## eq_4: Sampling estimator

$$
\widehat{\mathrm{Inf}}_i=\frac1N\sum_{k=1}^{N}y^{(k)}_i,\quad \Pr\big[|\widehat{\mathrm{Inf}}_i-\mathrm{Inf}_i(f)|\ge\epsilon\big]\le 2e^{-2N\epsilon^2}
$$

Empirical frequency of 1s at position i over N independent runs, with a Hoeffding bound.

Provenance: `abstract_inferred`. The approximation algorithm is presumed to be repeated sampling; the Hoeffding bound is a standard tool that I added, not the paper's own analysis.

Abstract evidence: we give an approximation algorithm to evaluate the influence of any variable on a Boolean function

Equation assumptions:

- Independent runs
- Paper's actual algorithm and error bound unknown

## eq_5: Tiny instance

$$
f(x_1,x_2)=x_1x_2\Rightarrow \hat f(s)^2=\tfrac14\ \forall s,\ \Pr[y_i=1]=\tfrac12=\mathrm{Inf}_i(f)
$$

For AND on 2 bits, (-1)^f has all four squared Fourier coefficients equal to 1/4, so each position is 1 with probability 1/2.

Provenance: `assumption`. Chosen as a small checkable example; it is consistent with eq_2, since flipping x_i changes f for exactly half of the inputs.

Equation assumptions:

- f is AND on 2 variables

## Registers

- x: n qubits; input register, measured to give y; bit i corresponds to x_i (ordering assumed)
- anc: 1 qubits; phase-kickback ancilla in |-> (or use a direct phase oracle)

## Initial state

|0>^{\otimes n} on x, and |1> on anc (made into |-> by a Hadamard)

## Measurement

Computational-basis measurement of the n-qubit input register; the ancilla is not measured.

## Classical postprocessing

For each i, compute the fraction of runs with y_i=1 as the influence estimate; the choice of N follows from the desired epsilon.

## Algorithm steps

1. Apply H^{\otimes n} to x and prepare the ancilla in |->. (no equation reference)
2. Apply the oracle U_f: |x>|b> -> |x>|b xor f(x)>, which gives the phase (-1)^{f(x)} on x. (eq_1)
3. Apply H^{\otimes n} to x and measure it to obtain y. (eq_1, eq_3)
4. Repeat N times and average the i-th bits to estimate the influence. (eq_4)

## Assumptions

- Scope and the tiny instance (AND on 2 bits) are my own choices
- Standard phase-kickback oracle
- Bit i of y corresponds to variable x_i
- Hoeffding-based N is my addition, not from the abstract

## Missing information

- The paper's exact proof and formula for the dependence degree
- The paper's approximation algorithm and its error and complexity bounds
- The junta-learning algorithms and their success probabilities
- Details of the speedup comparison against Floess et al.
