# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Unitary Permutation: given black-box unitaries U_1..U_n and a permutation sigma of {1..n}, implement U_{sigma(n)} ∘ ... ∘ U_{sigma(1)}. The abstract states complexity bounds (quantum switches and queries) but not the circuit constructions.

Scope: Specify the problem itself and the stated complexity bounds, plus a tiny assumed instance (n=3, sigma=(2,3,1)) to fix conventions. The switch-based and query-based circuit constructions, the lower-bound proofs, and the link to Karp's permutation-as-substring problem are outside scope because the abstract does not give them.

## Symbols

- $n$: number of unitary gates; domain: positive integer
- $U_i$: i-th unitary gate (black box); domain: unitary on a fixed d-dimensional system, i in {1..n}
- $\sigma$: permutation specifying the application order; domain: bijection on {1..n}
- $W_\sigma$: target unitary; domain: unitary on the system
- $S(n)$: number of quantum switches needed; domain: positive integer
- $Q(n)$: number of queries sufficient in the standard circuit model; domain: positive integer

## eq_1: Target unitary

$$
W_\sigma = U_{\sigma(n)}\circ\cdots\circ U_{\sigma(1)}
$$

Composition of the gates in the order given by sigma; U_{sigma(1)} is applied first.

Provenance: `abstract_explicit`. Stated directly as the goal of the problem.

Abstract evidence: U_{\sigma(n)}\circ\ldots\circ U_{\sigma(1)}

## eq_2: Switch complexity

$$
S(n)=n\log_2(n)+\Theta(n)
$$

Necessary and sufficient number of quantum switches.

Provenance: `abstract_explicit`. Claimed result in the abstract.

Abstract evidence: $n\log_{2}(n)+\Theta(n)$ quantum switches are necessary and sufficient

Equation assumptions:

- Switch model as in the cited prior work; its precise definition is not given.

## eq_3: Query upper bound

$$
Q(n)\le n^{2}-2n+4
$$

Number of calls sufficient in the standard circuit model.

Provenance: `abstract_explicit`. Claimed upper bound.

Abstract evidence: $n^{2}-2n+4$ calls are sufficient

## eq_4: Query lower bound

$$
Q(n)\ge n^{2}-o\left(n^{7/4+\epsilon}\right),\ \forall\epsilon>0
$$

Lower bound on queries under an additional unspecified assumption on the gate family.

Provenance: `abstract_explicit`. Claimed lower bound.

Abstract evidence: $n^{2}-o(n^{7/4+\epsilon})$ queries are required, for any $\epsilon>0$

Equation assumptions:

- The additional gate-family assumption is not specified in the abstract.

## eq_5: Toy instance

$$
n=3,\ \sigma=(1\mapsto2,\ 2\mapsto3,\ 3\mapsto1),\ W_\sigma=U_1\,U_3\,U_2
$$

Example fixing the ordering convention: U_2 is applied first, then U_3, then U_1.

Provenance: `assumption`. Tiny instance chosen to fix conventions.

Equation assumptions:

- Instance chosen by the reconstruction, not from the abstract.

## Registers

- system: unknown (a d-dimensional system acted on by the U_i) qubits; Register on which the gates are applied

## Algorithm steps

1. Define the target W_sigma by composing the gates in the order given by sigma. (eq_1)
2. Record the stated switch-model complexity and the query-model upper and lower bounds. (eq_2, eq_3, eq_4)
3. Fix conventions with the n=3 instance. (eq_5)

## Assumptions

- The toy instance is an assumed illustration.
- No circuit construction is reconstructed.

## Missing information

- Definition of the quantum switch model and its circuits
- Explicit query-model circuit achieving n^2-2n+4 calls
- Additional gate-family assumption for the lower bound
- Details of the reduction to the permutation-as-substring problem
- Proofs of all bounds
