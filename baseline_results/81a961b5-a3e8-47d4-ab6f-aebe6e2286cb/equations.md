# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

GROUP MULTIPLICATION for an ordered pair (g_1,g_2) in a finite group G: given one query to an oracle that returns elements of the tuple, output the product g_1 g_2. The abstract claims a single-query algorithm with success probability 2/|G| for any finite G (generalizing Deutsch's algorithm from Z_2) and that this is optimal.

Scope: One smallest useful construction: the n=2 GROUP MULTIPLICATION problem for the cyclic group G = Z_3 (N=3, the smallest group where the claimed probability 2/|G| = 2/3 is strictly below 1), using a character/Fourier-eigenstate construction on a 1-qubit index register and a Z_3 target register, followed by a 3-outcome rank-1 POVM on the index qubit. Verification target: for each of the 9 pairs (g_1,g_2) the output equals g_1+g_2 mod 3 with probability exactly 2/3. Out of scope: the paper's general theorem on maximally distinguishable translates for an arbitrary unitary representation, the construction for nonabelian G, the optimality proof, n>2 tuples, and the HIDDEN CONJUGATING ELEMENT problem.

## Symbols

- $G$: finite group; in the scoped instance G = \mathbb{Z}_N with N = 3, written additively; domain: finite group; here \mathbb{Z}_3 = \{0,1,2\}
- $N$: group order |G|; domain: positive integer; N = 3 in the instance
- $g_1, g_2$: hidden ordered pair of group elements held by the oracle; domain: \mathbb{Z}_N
- $i$: query index selecting which tuple element is accessed (index register value); domain: \{0,1\}
- $h$: target register value (group element); domain: \mathbb{Z}_N
- $\omega$: primitive N-th root of unity, \omega = e^{2\pi i/N}; domain: \mathbb{C}, |\omega| = 1
- $|\chi_k\rangle$: Fourier (character) state of the target register, eigenstate of the shift (regular-representation) action; domain: unit vector in \mathbb{C}^N, k \in \mathbb{Z}_N
- $m$: the answer g_1 + g_2 \bmod N (the group product); also the measurement outcome/guess; domain: \mathbb{Z}_N
- $|\theta_m\rangle$: index-qubit state carrying the relative phase \omega^{-m}; domain: unit vector in \mathbb{C}^2
- $E_m$: POVM element associated with guessing product m; domain: positive semidefinite 2\times 2 operator
- $O_{g_1,g_2}$: the quantum oracle for the hidden pair; domain: unitary on \mathbb{C}^2 \otimes \mathbb{C}^N

## eq_1: Oracle for GROUP MULTIPLICATION (n=2, additive Z_N)

$$
O_{g_1,g_2}\,|i\rangle|h\rangle = |i\rangle\,|h + g_i \bmod N\rangle, \qquad i \in \{0,1\},\; h \in \mathbb{Z}_N
$$

A single query lets the algorithm access element g_i of the tuple, applied to the target register by the (regular) group action; the index register is left unchanged.

Provenance: `assumption`. The abstract says the product is determined 'by querying elements of the tuple' but does not fix the oracle convention; the standard in-place group-action oracle (regular representation on C[G]) is assumed. For N=2 this is exactly the Deutsch oracle |i\rangle|h\rangle \to |i\rangle|h \oplus x_i\rangle.

Equation assumptions:

- Oracle acts by the group action (here addition mod N) on a target register indexed by G
- Index register uses i=0 for g_1 and i=1 for g_2

## eq_2: Fourier/character eigenstates of the shift action

$$
|\chi_k\rangle = \frac{1}{\sqrt{N}} \sum_{h \in \mathbb{Z}_N} \omega^{-kh} |h\rangle, \qquad |h\rangle \mapsto |h+g\rangle \;\Rightarrow\; |\chi_k\rangle \mapsto \omega^{kg}|\chi_k\rangle
$$

Shifting the target register by g multiplies the character state by the phase \omega^{kg} (phase kickback); exact equality.

Provenance: `standard_background`. Standard discrete Fourier transform / character theory of Z_N; for N=2, |\chi_1\rangle = |-\rangle, the Deutsch kickback state.

## eq_3: Initial state

$$
|\psi_0\rangle = \frac{1}{\sqrt{2}}\left(|0\rangle|\chi_{1}\rangle + |1\rangle|\chi_{-1}\rangle\right)
$$

Index qubit in uniform superposition, entangled with opposite-sign characters on the target so that the two branches pick up phases \omega^{g_1} and \omega^{-g_2} whose ratio depends only on g_1+g_2.

Provenance: `assumption`. A concrete choice of a state whose translates under the oracle group depend on the pair only through the product; it reproduces Deutsch's |+\rangle|-\rangle for N=2 (where \chi_1 = \chi_{-1}). The abstract's general recipe for choosing such a state is not available.

Equation assumptions:

- G cyclic so that a faithful character exists
- This is one valid construction, not necessarily the paper's

## eq_4: State after one query and uncomputing the target

$$
O_{g_1,g_2}|\psi_0\rangle = \frac{1}{\sqrt{2}}\left(\omega^{g_1}|0\rangle|\chi_{1}\rangle + \omega^{-g_2}|1\rangle|\chi_{-1}\rangle\right) \;\xrightarrow{U_{\mathrm{prep}}^{\dagger}}\; \omega^{g_1}\,|\theta_m\rangle|0\rangle, \quad |\theta_m\rangle = \frac{1}{\sqrt{2}}\left(|0\rangle + \omega^{-m}|1\rangle\right), \quad m = g_1 + g_2 \bmod N
$$

Exact: after kickback the relative phase is \omega^{-(g_1+g_2)}; uncomputing the controlled character preparation U_{prep} (U_{prep}|i\rangle|0\rangle = |i\rangle|\chi_{(-1)^i}\rangle) disentangles the target, leaving the answer m encoded as one of N equiangular index-qubit states.

Provenance: `abstract_inferred`. Inferred from the claim that the algorithm generalizes Deutsch's algorithm: the Deutsch mechanism (phase kickback then interference on the index register) extended with Z_N characters yields a state depending only on the product m. Follows from eq_1-eq_3 by direct computation.

Abstract evidence: This generalizes Deutsch’s Algorithm from $\hbox{\bbb Z}_{2}$ to an arbitrary finite group.

Equation assumptions:

- Oracle convention of eq_1
- Initial state of eq_3

## eq_5: Optimal N-outcome POVM on the index qubit

$$
E_m = \frac{2}{N}\,|\theta_m\rangle\langle\theta_m|, \quad m \in \mathbb{Z}_N, \qquad \sum_{m} E_m = \frac{2}{N}\cdot\frac{N}{2} I_2 = I_2
$$

Rank-1 POVM distinguishing the N equiangular states |\theta_m\rangle in a 2-dimensional space; completeness uses \sum_m \omega^{m} = 0. For N=3 this is the trine measurement, implementable via a Naimark dilation with one ancilla qubit. For N=2 it is the projective Hadamard-basis measurement.

Provenance: `standard_background`. Standard result for a group-covariant ensemble generated by a unitary with distinct eigenvalues in dimension d: the square-root (pretty good) measurement is optimal with success probability d/N, here d=2.

## eq_6: Success probability

$$
P_{\mathrm{succ}} = \langle\theta_m|E_m|\theta_m\rangle = \frac{2}{N} = \frac{2}{|G|}, \qquad P_{\mathrm{succ}} = \tfrac{2}{3} \text{ for } G = \mathbb{Z}_3,\; P_{\mathrm{succ}} = 1 \text{ for } G = \mathbb{Z}_2
$$

Exact success probability of outputting m = g_1 g_2 after a single query, identical for every hidden pair; matches the abstract's claimed value.

Provenance: `abstract_explicit`. The value 2/|G| is stated in the abstract; the scoped construction attains it for cyclic G by eq_4-eq_5. The abstract's optimality claim is not reconstructed here.

Abstract evidence: find the product of two elements of $G$ with a single quantum query with probability $2/|G|$

Equation assumptions:

- Attainment shown only for the cyclic instance; the abstract claims it for any finite G

## Registers

- index: 1 qubit qubits; query index i \in \{0,1\} selecting g_1 or g_2; carries the answer phase after the query
- target: \lceil \log_2 N \rceil = 2 qubits for N=3 (basis states |0\rangle,|1\rangle,|2\rangle used; |3\rangle unused) qubits; group-element register h \in \mathbb{Z}_N on which the oracle acts by addition mod N; h encoded as an unsigned binary integer
- ancilla: 1 qubit qubits; optional ancilla for the Naimark dilation implementing the 3-outcome POVM E_m on the index qubit

## Initial state

|\psi_0\rangle = \frac{1}{\sqrt{2}}(|0\rangle|\chi_1\rangle + |1\rangle|\chi_{-1}\rangle), prepared from |0\rangle_{index}|0\rangle_{target} by H on the index qubit followed by the controlled character preparation U_{prep} (QFT-type map |0\rangle \mapsto |\chi_{\pm 1}\rangle on the target, sign controlled by the index). Ancilla starts in |0\rangle.

## Measurement

POVM \{E_m = (2/N)|\theta_m\rangle\langle\theta_m|\}_{m \in \mathbb{Z}_N} on the index qubit (trine measurement for N=3, implemented by an isometry into index+ancilla followed by computational-basis measurement; exact dilation gates are a circuit-stage choice). The target register is returned to |0\rangle and need not be measured.

## Classical postprocessing

Output the measurement outcome m directly as the guess for the product g_1 g_2 (= g_1 + g_2 mod 3). Expected per-pair success probability is exactly 2/3 for all 9 pairs (g_1,g_2) in Z_3 x Z_3; verification consists of checking this frequency for each pair.

## Algorithm steps

1. Prepare the index qubit in |+\rangle and apply U_{prep} to put the target in |\chi_1\rangle on the i=0 branch and |\chi_{-1}\rangle on the i=1 branch. (eq_2, eq_3)
2. Apply the oracle O_{g_1,g_2} once; phase kickback gives branch phases \omega^{g_1} and \omega^{-g_2}. (eq_1, eq_2, eq_4)
3. Apply U_{prep}^{\dagger} to return the target to |0\rangle, leaving the index qubit in |\theta_m\rangle with m = g_1 + g_2 \bmod N (global phase irrelevant). (eq_4)
4. Perform the N-outcome POVM \{E_m\} on the index qubit (for N=3 via a Naimark dilation using the ancilla) and record outcome m. (eq_5, eq_6)

## Assumptions

- No experiment_scope was supplied; the scoped instance (G = Z_3, n = 2, single query) was chosen as the smallest case where the claimed 2/|G| probability is nontrivial.
- The oracle is assumed to act in place by the regular group action |i\rangle|h\rangle \to |i\rangle|h + g_i\rangle; the paper's exact oracle convention is unknown.
- The character-based initial state and POVM are one construction attaining 2/|G| for cyclic groups; they are not claimed to be the paper's general construction.
- Target register integer encoding: h \in \{0,1,2\} as 2-bit unsigned binary; the basis state |3\rangle is unused and must not be populated.
- Group written additively; 'product' means addition mod N in the instance.

## Missing information

- The paper's general theorem: how to find, for an arbitrary unitary representation of a finite group, a state whose translates are maximally distinguishable (the core abstract contribution).
- The explicit single-query construction attaining 2/|G| for nonabelian G (characters alone do not suffice; the regular-representation decomposition into irreps is presumably used).
- The optimality proof that 2/|G| cannot be exceeded with one query.
- The definition and solution of the HIDDEN CONJUGATING ELEMENT problem (oracle h \mapsto g h g^{-1}) and the conditions on G (e.g., dihedral, symmetric) under which probability 1 is achieved with one query.
- Treatment of n > 2 tuples and multi-query bounds for GROUP MULTIPLICATION.
- The paper's precise oracle model for GROUP MULTIPLICATION.
