# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantum property testing of monotonicity of f:{0,1}^n->{0,1} with one-sided error: accept monotone f with certainty, reject eps-far f with bounded error, using Otilde(n^{1/4} eps^{-1/2}) queries. The abstract gives only the query complexity and the testing guarantee, not the algorithm.

Scope: Formalize the testing problem, the eps-farness definition, the claimed query bound, and a tiny explicit instance (n=2) with a phase-oracle query model. The paper's actual algorithm (e.g. how violating edges or pairs are found with quantum search) is outside scope and not reconstructed. The comparison with the randomized algorithm is also outside scope.

## Symbols

- $n$: number of input bits; domain: positive integer
- $f$: Boolean function under test; domain: {0,1}^n -> {0,1}
- $\varepsilon$: farness parameter; domain: (0,1]
- $x \preceq y$: coordinatewise partial order, x_i<=y_i for all i; domain: x,y in {0,1}^n
- $\mathcal{M}$: set of monotone functions on {0,1}^n; domain: subset of functions {0,1}^n->{0,1}
- $\mathrm{dist}(f,g)$: normalized Hamming distance between f and g; domain: [0,1]
- $O_f$: quantum query oracle for f; domain: unitary on n+1 qubits
- $Q$: number of oracle queries; domain: nonnegative integer

## eq_1: Monotonicity

$$
f\in\mathcal{M}\iff \forall x,y\in\{0,1\}^n:\ x\preceq y\Rightarrow f(x)\le f(y)
$$

Definition of a monotone Boolean function.

Provenance: `standard_background`. Standard definition of the property being tested; the abstract only names monotone functions.

Equation assumptions:

- Coordinatewise partial order on the hypercube

## eq_2: Epsilon-farness

$$
\mathrm{dist}(f,g)=2^{-n}\left|\{x:f(x)\ne g(x)\}\right|,\quad f\ \varepsilon\text{-far}\iff \min_{g\in\mathcal{M}}\mathrm{dist}(f,g)\ge\varepsilon
$$

Standard definition of being eps-far from monotone.

Provenance: `standard_background`. The abstract uses eps-far without defining it; normalized Hamming distance is the standard convention.

Equation assumptions:

- Uniform-distribution normalized Hamming distance

## eq_3: Testing guarantee

$$
f\in\mathcal{M}\Rightarrow \Pr[\text{accept}]=1;\quad f\ \varepsilon\text{-far}\Rightarrow \Pr[\text{reject}]\ge 2/3
$$

Accept/reject behaviour of the tester. One-sided error is read from 'accepts a monotone function'; the 2/3 constant is the usual bounded-error choice.

Provenance: `abstract_inferred`. Inferred from the abstract's accept/reject statement with bounded error; the constant 2/3 is an assumption.

Abstract evidence: accepts a monotone function, and rejects a function that is $\varepsilon$-far from being monotone

Equation assumptions:

- Acceptance of monotone f is with certainty
- Rejection probability at least 2/3

## eq_4: Query complexity

$$
Q=\widetilde{O}\left(n^{1/4}\varepsilon^{-1/2}\right)
$$

Claimed number of quantum queries to f.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: makes $\widetilde{O}(n^{1/4}\varepsilon^{-1/2})$ queries to a function

## eq_5: Phase query oracle

$$
O_f|x\rangle|b\rangle=|x\rangle|b\oplus f(x)\rangle,\quad x\in\{0,1\}^n,\ b\in\{0,1\}
$$

Standard quantum query access model for f.

Provenance: `standard_background`. The abstract says 'queries to a function'; this is the usual quantum oracle model, not stated in the abstract.

Equation assumptions:

- Standard bit-flip oracle access

## Registers

- x: n qubits; input register holding the query point
- b: 1 qubits; output/answer qubit for oracle f(x)

## Algorithm steps

1. Specify the testing problem and the oracle model for f. (eq_1, eq_2, eq_5)
2. Require the tester to satisfy the accept/reject guarantee while using the claimed query count. The internal quantum subroutines are not given in the abstract. (eq_3, eq_4)

## Assumptions

- The standard hypercube partial order and normalized Hamming distance define monotonicity and eps-farness.
- The 2/3 success constant is the conventional bounded-error choice.
- A tiny instance such as n=2 could be used for later validation but no circuit is specified here.

## Missing information

- The actual quantum algorithm, e.g. its subroutines for finding monotonicity violations.
- How the tilde hides polylog factors in n and 1/eps.
- Any state preparation, amplitude amplification, or search schedule.
- Measurement and decision rule details.
- The randomized baseline's exact complexity.
