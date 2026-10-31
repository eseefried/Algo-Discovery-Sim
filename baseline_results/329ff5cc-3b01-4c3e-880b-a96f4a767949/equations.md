# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Decompose an arbitrary isometry V from m qubits to n qubits (n >= m), i.e. a 2^n x 2^m matrix with V^dagger V = I, into a circuit of single-qubit gates and C-not gates using as few C-nots as possible; the abstract claims a parameter-counting-type lower bound on the C-not count and explicit schemes achieving it up to roughly a factor of two in leading order.

Scope: Scoped to (i) the definition of an isometry and its realisation as an n-qubit unitary acting on n-m ancilla qubits initialised to |0>, (ii) a parameter-counting lower bound on the C-not count of the generic form 4k + (single-qubit parameters) >= dim(isometries), and (iii) one smallest useful construction: a column-by-column reduction of V to |0>^{(n-m)} (x) I, instantiated on the tiny instance m=1, n=2 with V|x> = (|0,x> + |1,x xor 1>)/sqrt(2). Outside scope (not reconstructable from the abstract): the exact lower-order terms of the paper's lower bound, the three explicit decomposition schemes and their precise C-not counts, the bespoke optimisations for small m and n, and the Stinespring-based decomposition of channels and POVMs.

## Symbols

- $m$: number of input qubits of the isometry; domain: non-negative integer, m <= n
- $n$: number of output qubits of the isometry (total circuit width); domain: positive integer
- $V$: isometry from m to n qubits; domain: complex 2^n x 2^m matrix with V^dagger V = I_{2^m}
- $U$: n-qubit unitary extension of V; domain: U(2^n)
- $k$: number of C-not gates in a decomposition; domain: non-negative integer
- $k_{\min}(m,n)$: minimal number of C-nots needed for a worst-case isometry from m to n qubits; domain: non-negative integer
- $G_j$: n-qubit unitary (built from single-qubit and C-not gates) that maps the j-th column of the current isometry to the basis state |j> while acting trivially on |0>,...,|j-1>; domain: U(2^n)
- $|q_1 q_2 \cdots q_n\rangle$: computational basis state of the n-qubit register; q_1 is the most significant bit, integer value sum_i q_i 2^{n-i}; domain: q_i in {0,1}
- $|x\rangle$: computational basis state of the m input qubits, x an integer encoded with the first input qubit most significant; domain: x in {0,...,2^m-1}

## eq_1: Isometry definition

$$
V \in \mathbb{C}^{2^n \times 2^m}, \qquad V^{\dagger} V = I_{2^m}, \qquad n \geq m
$$

An isometry from m to n qubits is a norm-preserving linear map; equivalently its 2^m columns are orthonormal vectors in the 2^n-dimensional output space. Unitaries (m=n) and state preparation (m=0) are special cases.

Provenance: `standard_background`. Standard definition of an isometry; the abstract names the object but does not write the relation.

## eq_2: Realisation of V by an n-qubit unitary with ancillas

$$
V = U\,\bigl(|0\rangle^{\otimes (n-m)} \otimes I_{2^m}\bigr), \quad \text{i.e.}\quad U\,|0\rangle^{\otimes (n-m)}|x\rangle = V|x\rangle \;\; \forall x \in \{0,\dots,2^m-1\}
$$

A circuit of single-qubit and C-not gates implements a unitary U on all n qubits; it implements V exactly when the n-m ancilla qubits (placed as the first, most significant qubits) start in |0>. Only the action of U on the subspace |0>^{(n-m)} (x) C^{2^m} is constrained; the remaining columns of U are free, which is what allows fewer gates than a full unitary.

Provenance: `abstract_inferred`. Gate sequences are unitary on n qubits, so decomposing an isometry means finding a unitary that agrees with V on the ancilla-|0> subspace; register ordering with ancillas first is a convention chosen here.

Abstract evidence: the decomposition of arbitrary isometries into a sequence of single-qubit and Controlled-not (C-not) gates

Equation assumptions:

- Ancilla qubits are the first n-m qubits (most significant) and are initialised to |0>.

## eq_3: Real-parameter count of isometries (modulo global phase)

$$
\dim_{\mathbb{R}}\{V : V^{\dagger}V = I_{2^m}\}/U(1) = 2\cdot 2^{m+n} - 2^{2m} - 1
$$

A complex 2^n x 2^m matrix has 2^{m+n+1} real parameters; the Hermitian constraint V^dagger V = I removes 2^{2m} real parameters and an irrelevant global phase removes one more. For m=n this gives 4^n - 1 = dim SU(2^n) and for m=0 it gives 2^{n+1} - 2 (pure states up to phase).

Provenance: `standard_background`. Dimension of the Stiefel manifold of 2^m orthonormal vectors in C^{2^n}; consistent with the known unitary and state-preparation special cases.

## eq_4: Parameter-counting lower bound on the C-not count (generic form)

$$
4k + 3n \;\geq\; 2^{m+n+1} - 2^{2m} - 1 \quad\Longrightarrow\quad k_{\min}(m,n) \;\geq\; \left\lceil \tfrac{1}{4}\bigl(2^{m+n+1} - 2^{2m} - 3n - 1\bigr) \right\rceil
$$

An n-qubit circuit with k C-nots can be written with at most one single-qubit gate (3 real parameters modulo phase) per qubit initially plus at most two 2-parameter gates after each C-not (4 parameters per C-not), so it spans at most 4k + 3n real parameters. A worst-case isometry needs at least as many parameters as eq_3, giving the bound. Leading order is 2^{m+n-1} C-nots. For m=n this reproduces the known unitary bound ceil((4^n - 3n - 1)/4). The paper's actual bound may have slightly different lower-order terms (e.g. because single-qubit gates acting on ancillas in |0> contribute fewer parameters); only the leading order 2^{m+n-1} is asserted here with confidence.

Provenance: `abstract_inferred`. The abstract asserts a lower bound exists; the parameter-counting argument is the standard route (Shende-Markov-Bullock style) and is reconstructed here, not read from the paper.

Abstract evidence: We derive a theoretical lower bound on the number of C-not gates required to decompose an arbitrary isometry from $m$ to $n$ qubits

Equation assumptions:

- Each C-not contributes at most 4 real parameters and the initial layer at most 3 per qubit; the exact low-order constants of the paper are not known from the abstract.

## eq_5: Achievability up to a factor of about two (leading order)

$$
k_{\min}(m,n) \;\leq\; k_{\mathrm{scheme}}(m,n) \;\approx\; 2\cdot 2^{m+n-1} = 2^{m+n} \quad\text{(leading order)}
$$

The explicit decompositions achieve a C-not count whose leading term is about twice the lower bound's leading term 2^{m+n-1}, i.e. roughly 2^{m+n} C-nots for a generic isometry. Exact counts of the three schemes are not given in the abstract.

Provenance: `abstract_inferred`. Direct reading of the factor-of-two claim combined with the leading order of eq_4; the symbol k_scheme stands for whichever of the paper's three schemes is used.

Abstract evidence: give three explicit gate decompositions that achieve this bound up to a factor of about two in the leading order

Equation assumptions:

- The 'factor of about two' refers to the ratio of leading-order coefficients, as stated in the abstract.

## eq_6: Column-by-column reduction (chosen construction)

$$
G_{2^m-1} \cdots G_1 G_0\, V = |0\rangle^{\otimes (n-m)} \otimes I_{2^m}, \qquad G_j V_{j}|j\rangle = |j\rangle,\;\; G_j|i\rangle = |i\rangle \;(i<j), \qquad U = G_0^{\dagger} G_1^{\dagger}\cdots G_{2^m-1}^{\dagger}
$$

Process the columns of V in order: at stage j the current matrix V_j = G_{j-1}...G_0 V already has columns 0..j-1 equal to |0>,...,|j-1>; choose a gate sequence G_j (e.g. a cascade of uniformly controlled single-qubit gates, as in reverse state preparation, restricted so as not to disturb |0>,...,|j-1>) mapping column j to |j>. Here |j> denotes the n-qubit basis state whose integer value is j, so columns land exactly on |0>^{(n-m)} (x) |x>. Inverting the product yields the unitary U of eq_2. This is a proposed generic construction with the right leading order; it is not claimed to be identical to any of the paper's three schemes.

Provenance: `assumption`. Smallest useful explicit construction consistent with eq_2; the abstract does not describe the internal structure of its decompositions.

Equation assumptions:

- Each G_j is itself decomposed into single-qubit and C-not gates by standard uniformly-controlled-gate / state-preparation techniques, whose counts are not specified here.

## eq_7: Tiny explicit instance m=1, n=2

$$
V|x\rangle = \tfrac{1}{\sqrt{2}}\bigl(|0,x\rangle + |1,x\oplus 1\rangle\bigr),\quad x\in\{0,1\}; \qquad U = \mathrm{CNOT}_{1\to 2}\,(H \otimes I), \qquad U|0\rangle|x\rangle = V|x\rangle
$$

Columns V|0> = (|00>+|11>)/sqrt2 and V|1> = (|01>+|10>)/sqrt2 are orthonormal, so V is an isometry from 1 to 2 qubits. With ancilla qubit 1 in |0> and input qubit 2 in |x>, a Hadamard on qubit 1 followed by a C-not from qubit 1 to qubit 2 implements V exactly with one C-not. This particular V is not a worst case, so the single C-not does not contradict the worst-case lower bound of eq_4 (which for m=1,n=2 evaluates to ceil(5/4)=2 under the stated parameter-count assumptions).

Provenance: `assumption`. Chosen as the smallest non-trivial illustrative instance; verified by direct action on basis states.

Equation assumptions:

- Qubit ordering |q_1 q_2> with q_1 the ancilla (most significant) and q_2 the input.

## Registers

- ancilla: n-m qubits; Ancilla qubits initialised to |0>, occupying the first (most significant) positions; they supply the extra output dimensions of the isometry.
- input: m qubits; Input qubits carrying the state |psi> on which the isometry acts; after the circuit, all n qubits jointly hold V|psi>.

## Initial state

|0\rangle^{\otimes (n-m)} \otimes |\psi\rangle, with |\psi\rangle an arbitrary m-qubit state (for the tiny instance: |0\rangle \otimes |x\rangle, x in {0,1}).

## Algorithm steps

1. Specify the target isometry V (2^n x 2^m, V^dagger V = I) and fix register ordering: ancillas first, input qubits last, integer encoding most-significant-first. (eq_1, eq_2)
2. Evaluate the parameter-counting lower bound on the worst-case C-not count to know the target scale (leading order 2^{m+n-1}). (eq_3, eq_4)
3. Classically compute a decomposition: reduce V column by column to |0>^{(n-m)} (x) I with gate sequences G_0,...,G_{2^m-1}, each built from single-qubit and C-not gates; set U = G_0^dagger ... G_{2^m-1}^dagger (expected roughly 2^{m+n} C-nots in leading order for generic V). (eq_6, eq_5)
4. Prepare the ancilla qubits in |0> and the input qubits in |psi>, then apply the gate sequence for U; the register now holds V|psi>. For the tiny instance apply H on qubit 1 then CNOT from qubit 1 to qubit 2. (eq_2, eq_7)

## Assumptions

- No experiment_scope was supplied; the reconstruction chose the column-by-column construction and the instance m=1, n=2 as the single smallest useful target.
- Ancilla qubits are the first n-m qubits (most significant) and start in |0>; integer labels of basis states use most-significant-first encoding.
- The lower bound is reconstructed by generic parameter counting (4 real parameters per C-not, 3 per initial single-qubit gate); the paper's exact lower-order terms may differ.
- Equality signs in eq_2, eq_6 and eq_7 denote exact equality of the isometry (up to a global phase); eq_5 is an approximate leading-order statement only.

## Missing information

- Exact statement (including lower-order terms) of the paper's lower bound on the C-not count for isometries from m to n qubits.
- Descriptions and exact C-not counts of the three explicit decomposition schemes mentioned in the abstract.
- Details of the bespoke optimisations for small m and n and the resulting C-not counts.
- The construction that applies the isometry decomposition to arbitrary quantum operations and POVMs via Stinespring's theorem, including ancilla counts.
- Whether the paper counts single-qubit gates or measures any other cost besides C-nots.
