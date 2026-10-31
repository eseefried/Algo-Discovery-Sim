# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Given a unitary representation of a finite group G on a finite-dimensional Hilbert space, find a state whose G-translates are distinguishable with the highest probability. Apply this to quantum oracle problems: GROUP MULTIPLICATION (determine the product of an ordered tuple of group elements by querying elements; for two elements, a single quantum query succeeds with probability 2/|G|, which is optimal and generalizes Deutsch's algorithm from Z_2) and the HIDDEN CONJUGATING ELEMENT PROBLEM (oracle conjugates by an unknown group element; for many groups, e.g. dihedral and symmetric, the element is found with probability 1 using one query).

Scope: Abstract-level reconstruction of the problem statements and the success-probability claims; the optimal-state construction, circuits and measurements are not given in the abstract and are left to later parts.

## Symbols

- $G$: finite group; domain: finite group, order |G|
- $\rho$: unitary representation of G on Hilbert space H; domain: \rho: G \to U(H), dim H < \infty
- $|\psi\rangle$: state whose translates \rho(g)|\psi\rangle are to be distinguished; domain: unit vectors in H
- $p_{succ}$: success probability of the single-query algorithm for the product of two elements; domain: [0,1]

## eq_1: Product of two group elements: success probability

$$
p_{succ}=\frac{2}{|G|}
$$

Optimal single-query success probability for finding the product of two elements of G.

Provenance: `abstract_explicit`. Stated in the abstract; optimality is also claimed.

Abstract evidence: we give an algorithm to find the product of two elements of $G$ with a single quantum query with probability $2/|G|$

## Registers

- H_rep: dim H (unknown) qubits; Register holding the probe state |\psi\rangle, acted on by \rho(g) through the oracle

## Initial state

An optimal probe state |\psi\rangle in H maximizing the success probability of distinguishing the translates \rho(g)|\psi\rangle. The abstract does not give its explicit form.

## Measurement

A single discrimination measurement (a POVM on H) is applied to the post-query state \rho(g)|\psi\rangle to identify g (or the product/hidden element). The abstract states only that the optimal state maximizes distinguishability; the explicit POVM is not given. Expected success is 2/|G| for the product of two elements and 1 for the hidden conjugating element on e.g. dihedral and symmetric groups.

## Classical postprocessing

Map the measurement outcome to a group element label, and for group multiplication to the product of the two elements. No further processing is specified in the abstract.

## Algorithm steps

1. Prepare the optimal probe state |\psi\rangle in the representation space H. (no equation reference)
2. Make one oracle query, which applies \rho(g) for the unknown group-dependent element g (for the hidden conjugating element problem, the conjugation action). The state becomes \rho(g)|\psi\rangle. (no equation reference)
3. Distinguish the translates \rho(g)|\psi\rangle. For the product of two elements this succeeds with probability 2/|G|. (eq_1)

## Assumptions

- The oracle is modeled as applying a unitary representation \rho(g) of the queried or hidden group element to the probe state; this is a generic assumption, not the paper's explicit construction.
- Oracle modeled generically as applying \rho(g) to the probe state.
- Measurement is assumed to be an optimal discrimination POVM, whose form is not given in the abstract.

## Missing information

- Explicit construction of the optimal state
- Oracle definition and circuit details
- Explicit POVM for discrimination of translates
- Explicit representation used for each oracle problem (group multiplication versus conjugation).
- Outcome-to-answer mapping for the product of n elements.
