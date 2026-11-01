# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a unitary rep R of a finite group G, find a state |psi> whose translates R(g)|psi> are best distinguishable. Apply this to Group Multiplication for two elements (one query, success 2/|G|, generalizing Deutsch) and to the Hidden Conjugating Element problem (one query, success 1 for suitable groups). The tiny instance is Z_2 Deutsch, with S_3 conjugation as an optional extension.

Scope: Scope: (1) the general optimal-state and success-probability formula from rep theory, (2) the Z_2 Deutsch instance as the smallest concrete circuit, (3) the conjugation problem on S_3 (center-free, 6 basis states, 3 qubits) as an optional second instance. Outside scope: a general Fourier-transform circuit for arbitrary G, the optimality proof for 2/|G|, the n-tuple Group Multiplication problem, and the explicit query protocol for general G in group multiplication.

## Symbols

- $G$: finite group; domain: finite set, order |G|
- $R$: unitary representation of G on Hilbert space H; domain: R: G -> U(H)
- $\rho$: irreducible representation label; domain: irreps of G
- $d_\rho$: dimension of irrep rho; domain: positive integer
- $m_\rho$: multiplicity of rho in R; domain: nonnegative integer
- $|\Phi_\rho\rangle$: maximally entangled state between V_rho and a multiplicity space of dimension min(d_rho,m_rho); domain: unit vector
- $P_{succ}$: probability of correctly identifying g from R(g)|psi>; domain: [0,1]

## eq_1: Optimal state

$$
|\psi\rangle=\sum_\rho \sqrt{\frac{d_\rho\min(d_\rho,m_\rho)}{|G|}}\,|\Phi_\rho\rangle
$$

State maximizing the translate-discrimination success probability. Its norm is 1 only when the weights sum to 1, which holds when R contains every irrep; otherwise normalise the weights.

Provenance: `standard_background`. Recalled from the sketch and from known results on optimal discrimination of group-covariant states. The abstract only says such a state can be found.

Equation assumptions:

- Irreps and multiplicities computed classically
- Normalisation caveat above

## eq_2: Optimal success probability

$$
P_{succ}=\frac{1}{|G|}\sum_\rho d_\rho\min(d_\rho,m_\rho)
$$

Maximum probability of discriminating the |G| translates. It equals 1 when the sum equals |G|.

Provenance: `standard_background`. Recalled from the sketch. The abstract says the state with the highest probability can be found but gives no formula.

Equation assumptions:

- Uniform prior over g in G

## eq_3: Group multiplication success

$$
P_{succ}^{\text{mult}}=\frac{2}{|G|}
$$

Optimal one-query success probability for the product of two group elements. For Z_2 it is 1, as in Deutsch's algorithm.

Provenance: `abstract_explicit`. Stated directly in the abstract. Optimality is also claimed there.

Abstract evidence: we give an algorithm to find the product of two elements of $G$ with a single quantum query with probability $2/|G|$

## eq_4: Deutsch instance

$$
O_a|x\rangle=|x+a\bmod 2\rangle,\quad O_a|-\rangle=(-1)^a|-\rangle,\quad H(-1)^{a}|-\rangle\text{ on a control }|+\rangle\to|a\rangle
$$

Z_2 case. The query acts on |-> in the target and the phase (-1)^a is kicked back to a |+> control. The Hadamard basis then reads a. For Deutsch, a is the XOR of the oracle's two values (the product a+b), which is the quantity learned in one query. In the simplest group-multiplication form there is a single oracle with hidden a, queried once.

Provenance: `abstract_inferred`. Inferred from the claim that the algorithm generalizes Deutsch. The explicit circuit is standard background.

Abstract evidence: This generalizes Deutsch’s Algorithm from $\hbox{\bbb Z}_{2}$ to an arbitrary finite group.

Equation assumptions:

- Phase-kickback form of the oracle on 1 control and 1 target qubit

## eq_5: Conjugation oracle

$$
C_g|x\rangle=|g x g^{-1}\rangle,\quad \sum_\rho d_\rho\min(d_\rho,m_\rho)=|G|\Rightarrow P_{succ}=1
$$

The oracle acts by conjugation. The condition gives perfect discrimination of g, but only modulo the center Z(G), since C_g depends only on gZ(G).

Provenance: `abstract_inferred`. Inferred by combining the abstract claim with eq_2. The center caveat is my own addition from the sketch and the structure of the problem.

Abstract evidence: We show that for many groups, including dihedral and symmetric groups, the unknown element can be determined with probability $1$ using a single quantum query.

Equation assumptions:

- Center-free group such as S_3, or identification of g mod Z(G)
- Conjugation rep on the |G|-dimensional register

## Registers

- query: ceil(log2|G|) qubits, 1 for Z_2, 3 for S_3 qubits; holds the group-labelled state psi; the oracle is applied here
- control: 1 qubit (Z_2 Deutsch only) qubits; receives the kicked-back phase and is measured

## Initial state

All qubits |0>. Group elements are encoded as basis states |index(x)> with the index in little-endian binary, so the register value is bits read as an integer with the last character of the counts key being qubit 0.

## Measurement

Measure the query register (and the control for Z_2) in the computational basis after the inverse rotation. The outcome labels the guessed group element.

## Classical postprocessing

Map bitstring to group element index with bits[::-1]. For conjugation, report g modulo the center.

## Algorithm steps

1. Classically decompose R into irreps and compute d_rho and m_rho. Build psi from eq_1 using standard gates (e.g. a small rotation and CNOT synthesis, not initialize). (eq_1, eq_2)
2. Apply the placeholder oracle exactly once (right-multiplication by the hidden element, or conjugation). (eq_4, eq_5)
3. Apply the unitary mapping the translates to orthogonal basis states. For Z_2 this is H, and for general G it is the inverse group Fourier transform together with the basis change that undoes the state preparation. (eq_4)
4. Measure the register in the computational basis and map the bitstring to a group element, respecting little-endian order. (eq_3, eq_5)

## Assumptions

- Smallest instance chosen: Z_2 Deutsch, with S_3 conjugation as an optional second instance
- Oracle is a permutation unitary on a group-labelled register
- The G-Fourier transform is built offline for small G from standard gates
- Single query to one of the two elements in the group multiplication problem

## Missing information

- Explicit protocol for the group multiplication query with general G, including how the second element is handled
- Explicit circuit for the group Fourier transform for non-abelian G
- Whether the 2/|G| strategy uses the regular representation or a different one, since the abstract does not say
- Proof details of optimality
