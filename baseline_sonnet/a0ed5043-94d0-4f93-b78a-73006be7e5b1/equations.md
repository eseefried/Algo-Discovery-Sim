# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Optimal discrimination of group translates of a state under a unitary representation of a finite group, applied to GROUP MULTIPLICATION for two elements with one quantum query (success probability 2/|G|, generalizing Deutsch's algorithm).

Scope: Tiny instance: the generic optimal state-discrimination formulation for a group representation, plus the abstract's stated success probability 2/|G| for the two-element product. Group G=Z_2 is used as a sanity check where 2/|G|=1 (Deutsch). The explicit optimal state, query oracle construction, and the Hidden Conjugating Element algorithm are outside scope.

## Symbols

- $G$: finite group; domain: finite group, order |G|
- $\rho$: unitary representation of G; domain: homomorphism G -> U(H)
- $\mathcal{H}$: finite-dimensional Hilbert space; domain: C^d
- $|\psi\rangle$: state whose translates are to be distinguished; domain: unit vector in H
- $p_{succ}$: probability of correctly identifying the group element applied; domain: [0,1]
- $g,h$: group elements; domain: G

## eq_1: Translate family

$$
\{\rho(g)|\psi\rangle : g\in G\}
$$

Set of translates of the state under the group; the task is to choose |psi> maximizing the probability of distinguishing them.

Provenance: `abstract_inferred`. Directly describes the family of states being discriminated.

Abstract evidence: find a state whose translates under the group are distinguishable with the highest probability

Equation assumptions:

- Uniform prior over g

## eq_2: Optimal discrimination objective

$$
p_{succ}^{\mathrm{opt}}=\max_{|\psi\rangle}\max_{\{E_g\}}\frac{1}{|G|}\sum_{g\in G}\langle\psi|\rho(g)^\dagger E_g\rho(g)|\psi\rangle,\ E_g\ge0,\ \sum_g E_g=I
$$

Maximum success probability over states and POVMs under a uniform prior.

Provenance: `standard_background`. Standard minimum-error discrimination formulation; the paper's actual solution method is not given in the abstract.

Equation assumptions:

- Uniform prior over g
- Minimum-error discrimination

## eq_3: Two-element product success probability

$$
p_{succ}=\frac{2}{|G|}
$$

Success probability of the single-query algorithm for the product of two elements of G; stated as optimal.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: we give an algorithm to find the product of two elements of $G$ with a single quantum query with probability $2/|G|$

## eq_4: Deutsch special case

$$
G=\mathbb{Z}_2\Rightarrow p_{succ}=\frac{2}{2}=1
$$

For Z_2 the formula gives certainty, consistent with Deutsch's algorithm.

Provenance: `abstract_inferred`. Substituting |G|=2 in the stated probability.

Abstract evidence: This generalizes Deutsch’s Algorithm from $\hbox{\bbb Z}_{2}$ to an arbitrary finite group.

## eq_5: Hidden conjugating element oracle

$$
O_a:\ x\mapsto a x a^{-1},\ a\in G\text{ unknown}
$$

Oracle acts by conjugation by an unknown element a; the goal is to determine a.

Provenance: `abstract_inferred`. Formal reading of the verbal description; the quantum implementation is not specified. Note that a is determined only up to the center of G by conjugation alone, a caveat not discussed in the abstract.

Abstract evidence: the oracle acts by conjugating by an unknown element of the group

Equation assumptions:

- Classical action written as x -> a x a^{-1}

## Registers

- R: unknown (dimension of H) qubits; Register holding the probe state in representation space H; the query oracle encoding is not specified in the abstract.

## Initial state

An optimal state |psi> in H maximizing discrimination of its translates; its explicit form is not given in the abstract.

## Measurement

Optimal discriminating POVM {E_g} on the translated states; its explicit form is not given in the abstract.

## Algorithm steps

1. Choose a representation rho of G on H and find a state |psi> maximizing the translate-discrimination success probability. (eq_1, eq_2)
2. For the two-element product problem, use a single query and discriminate to obtain the product with probability 2/|G|. (eq_3, eq_4)
3. For the hidden conjugating element problem, apply the oracle once to the probe state and discriminate the resulting states. (eq_5)

## Assumptions

- Uniform prior over group elements
- Minimum-error discrimination as the figure of merit
- Z_2 used as the tiny sanity instance

## Missing information

- Explicit optimal state and measurement construction
- Representation used for the GROUP MULTIPLICATION query oracle
- Oracle encoding and circuit for the n-tuple problem
- Which groups admit probability-1 hidden conjugating element determination and the algorithm
- Proof of optimality of 2/|G|
