# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Exact synthesis: given an n-qubit unitary U (n <= 2) whose entries lie in the ring Z[i, 1/sqrt(2)] (equivalently D[omega], omega = e^{i pi/4}), with entries written as (a + b sqrt2 + i(c + d sqrt2))/sqrt2^k, produce a Clifford+T circuit implementing U exactly, using at most one ancilla, with gate count O(k), via reduction of U to 1- and 2-level matrices in the style of Giles and Selinger.

Scope: Scoped to the smallest useful construction: the single-qubit case (n = 1, no ancilla) of denominator-exponent reduction by 2-level (here full 2x2) H and T^m operations, plus the general structure (determinant/ancilla condition, column-wise 2-level reduction) that the abstract implies for n = 2. Tiny explicit instance (assumption): U = T H, whose entries are 1/sqrt2^1 on the first row and omega/sqrt2 = (1 + i)/sqrt2^2 on the second row, so k = 2 in the abstract's normal form; the algorithm should return a circuit of O(k) gates equal to U (e.g. the two-gate word T H). Outside scope: the paper's specific new method for implementing 2-level operators on two qubits in Clifford+T, the exact constant in the O(k) bound, the precise ancilla-handling construction, and any comparison with Giles-Selinger gate counts.

## Symbols

- $n$: number of data qubits acted on by U; domain: \{1,2\}
- $\omega$: primitive 8th root of unity, \omega = e^{i\pi/4} = (1+i)/\sqrt{2}; domain: \mathbb{C}
- $\mathbb{Z}[\omega]$: ring of cyclotomic integers a + b\omega + c\omega^2 + d\omega^3; the ring of numerators; domain: subring of \mathbb{C}
- $\mathcal{D}[\omega]$: ring \mathbb{Z}[i,\tfrac{1}{\sqrt{2}}] = \mathbb{Z}[\omega, \tfrac{1}{\sqrt{2}}] in which the entries of U lie; domain: subring of \mathbb{C}
- $U$: target unitary operator on n qubits with entries in \mathcal{D}[\omega]; domain: U_{2^n}(\mathcal{D}[\omega])
- $u_{jl}$: entry of U in row j, column l; domain: \mathcal{D}[\omega]
- $a,b,c,d$: integer coefficients of the normal form of an entry; domain: \mathbb{Z}
- $k$: denominator exponent (power of \sqrt{2}) of U; the least such k is the least denominator exponent (lde); domain: \mathbb{Z}_{\geq 0}
- $x_j$: numerator of the j-th entry of a column of U after clearing the common denominator \sqrt{2}^k; domain: \mathbb{Z}[\omega]
- $H$: Hadamard gate; domain: U_2(\mathcal{D}[\omega])
- $T$: T gate, diag(1, \omega); domain: U_2(\mathcal{D}[\omega])
- $G_{[j,l]}$: 2-level operator acting as the 2x2 matrix G on basis states |j\rangle, |l\rangle and as identity elsewhere; domain: U_{2^n}(\mathcal{D}[\omega])
- $N(U)$: number of Clifford+T gates in the synthesized circuit for U; domain: \mathbb{Z}_{\geq 0}
- $m$: integer exponent of \omega in a determinant or phase; domain: \{0,\dots,7\}

## eq_1: Ring normal form of matrix entries

$$
u_{jl} = \frac{a + b\sqrt{2} + i\,(c + d\sqrt{2})}{\sqrt{2}^{\,k}}, \quad a,b,c,d \in \mathbb{Z},\; k \in \mathbb{Z}_{\geq 0}, \quad u_{jl} \in \mathbb{Z}[i,\tfrac{1}{\sqrt{2}}] = \mathbb{Z}[\omega,\tfrac{1}{\sqrt{2}}]
$$

Every entry of the target operator U is of this form with a common denominator exponent k; the equality of rings follows from omega = (1+i)/sqrt2 and i = omega^2.

Provenance: `abstract_explicit`. Stated directly in the abstract; the identification with Z[omega,1/sqrt2] is elementary algebra.

Abstract evidence: with entries in $\mathbb{Z}[i,\frac{1}{\sqrt{2}}]$, i.e., of the form $\frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{k}}$

Equation assumptions:

- k is taken as the least denominator exponent common to all entries of U (the abstract does not say whether k is minimal).

## eq_2: Unitarity constraint on a column with denominator exponent k

$$
u_{jl} = \frac{x_j}{\sqrt{2}^{\,k}},\; x_j \in \mathbb{Z}[\omega] \quad \Longrightarrow \quad \sum_{j=0}^{2^n-1} x_j^{\dagger} x_j = 2^{k}
$$

Clearing the common denominator of column l of a unitary U gives numerators x_j in Z[omega] whose squared moduli sum exactly to 2^k (exact equality, not approximation).

Provenance: `standard_background`. Columns of a unitary are unit vectors; multiplying by sqrt2^k gives this identity. This is the starting point of the Kliuchnikov-Maslov-Mosca and Giles-Selinger exact-synthesis arguments.

Equation assumptions:

- x^dagger denotes complex conjugation (the ring automorphism omega -> omega^{-1}).

## eq_3: Residue (parity) lemma for numerators

$$
x \equiv 0 \pmod{\sqrt{2}} \iff x^{\dagger}x \equiv 0 \pmod{2}, \qquad k \geq 1 \;\Rightarrow\; \#\{\,j : x_j \not\equiv 0 \pmod{\sqrt{2}}\,\} \equiv 0 \pmod{2}
$$

Reducing eq_2 modulo 2 shows that, when k >= 1, the number of column entries whose numerator is not divisible by sqrt2 is even, so such entries can be paired; if all entries are divisible by sqrt2 then k can be lowered by one directly. For n = 1 this means either both entries are divisible by sqrt2 or neither is.

Provenance: `standard_background`. Standard lemma underlying the 2-level reduction of Giles and Selinger (and the single-qubit algorithm of Kliuchnikov, Maslov and Mosca); recalled from knowledge, not from the paper.

Equation assumptions:

- Giles-Selinger additionally refine the residues modulo 2 into classes to pair entries so that eq_4 applies; the pairing rule used by the new method is not given in the abstract.

## eq_4: One 2-level reduction step lowering the denominator exponent

$$
T^{m}_{[j,l]} :\; \begin{pmatrix} x \\ y \end{pmatrix} \mapsto \begin{pmatrix} x \\ \omega^{m} y \end{pmatrix},\qquad x \equiv \omega^{m} y \pmod{2} \;\Rightarrow\; H_{[j,l]} : \frac{1}{\sqrt{2}^{\,k}}\begin{pmatrix} x \\ \omega^{m}y \end{pmatrix} \mapsto \frac{1}{\sqrt{2}^{\,k-1}}\begin{pmatrix} (x+\omega^{m}y)/2 \\ (x-\omega^{m}y)/2 \end{pmatrix},\; \tfrac{x \pm \omega^{m}y}{2} \in \mathbb{Z}[\omega]
$$

For a paired pair of entries (x, y) not divisible by sqrt2, a 2-level T^m (m in 0..7) is chosen so that the residues agree modulo 2; then a 2-level Hadamard makes both resulting numerators divisible by 2, which after absorbing one factor sqrt2 reduces the denominator exponent of that pair from k to k-1. Repeating over all pairs and then over all columns drives k to 0 using a bounded number of gates per unit decrease of k.

Provenance: `standard_background`. This is the Giles-Selinger / Kliuchnikov-Maslov-Mosca row-reduction mechanism that the abstract says its method builds on ('decomposition into 1- and 2-level matrices which was first proposed by Giles and Selinger'). The exact existence argument for m is part of that background, not re-derived here.

Equation assumptions:

- Existence of a suitable m for each pair follows from the residue classification of Z[omega]/(2); assumed as background.
- For n = 1 the 2-level operators are ordinary single-qubit H and T^m; for n = 2 they are 2-level (controlled-type) operators whose Clifford+T implementation is part of the paper's method and is not specified in the abstract.

## eq_5: Linear gate-count bound

$$
N(U) \leq C_n\, k + C_n' \quad \text{for } n \leq 2,\; \text{i.e. } N(U) = O(k)
$$

The total number of Clifford+T gates in the synthesized circuit grows at most linearly in the denominator exponent k, with constants depending only on n in {1,2}. Each reduction step (eq_4) costs a bounded number of gates and lowers k by one on a pair; since the number of columns and pairs is bounded for n <= 2, the total is O(k).

Provenance: `abstract_explicit`. The bound is claimed in the abstract; the constants C_n, C_n' are not given and are not reconstructed here.

Abstract evidence: This method achieves a bound of $O(k)$ gates using at most one ancilla

Equation assumptions:

- Gate count is measured in the Clifford+T gate set (plus possibly a global phase); the abstract does not fix the gate-counting convention.

## eq_6: Determinant condition and the role of one ancilla (n = 2)

$$
\det U = \omega^{m} \;\; (U \in U_4(\mathcal{D}[\omega])), \qquad \det(\text{2-qubit Clifford+}T\text{ circuit}) \in \{1,i,-1,-i\}, \qquad m \text{ odd} \;\Rightarrow\; \text{synthesize } U' = |0\rangle\langle 0| \otimes U + |1\rangle\langle 1| \otimes U \text{ on } 3 \text{ qubits}
$$

A 2-qubit unitary over D[omega] has determinant a unit of modulus 1, i.e. a power of omega, while ancilla-free 2-qubit Clifford+T circuits only realize determinants that are powers of i (T tensor I has determinant omega^2 = i). When det U is an odd power of omega, one ancilla qubit (left in its initial state) is needed; for n = 1 no ancilla is needed since single-qubit H and T realize all powers of omega as determinants.

Provenance: `standard_background`. Explains why the abstract's method needs 'at most one ancilla'; recalled from the Giles-Selinger characterization of ancilla-free Clifford+T operators. The specific way the paper handles the ancilla is not given in the abstract.

Equation assumptions:

- The ancilla is assumed to be initialized to |0> and returned to |0> (the abstract does not specify the ancilla convention).
- The form of U' shown is one standard choice; the paper's embedding may differ.

## Registers

- data: n (n in {1,2}; n = 1 in the scoped instance) qubits; qubits on which the target operator U acts
- ancilla: 0 or 1 qubits; optional ancilla, used only when n = 2 and det U is an odd power of omega (eq_6); not needed for the scoped n = 1 instance

## Initial state

Not applicable in the usual sense: the task is exact operator synthesis, so the output circuit C must satisfy C = U on the data register for every input state (up to the gate-counting convention for global phase); if an ancilla is used, C acts as U on the data register whenever the ancilla is |0> and returns the ancilla to |0>.

## Classical postprocessing

The entire method is a classical algorithm whose output is a Clifford+T gate list; no quantum measurement or statistical postprocessing is involved. For the scoped instance U = T H (k = 2), the expected output is a Clifford+T word equal to U with gate count O(k), e.g. the two-gate word T H (this expected output is an unverified sanity check, not a paper result).

## Algorithm steps

1. Classical preprocessing: write every entry of U in the normal form of eq_1 and determine the common (least) denominator exponent k; if n = 2 compute det U = omega^m and, if m is odd, adjoin one ancilla and replace U by the 3-qubit operator U' of eq_6. (eq_1, eq_6)
2. Column reduction: for the current first unreduced column, clear the denominator to get numerators x_j in Z[omega] satisfying eq_2; if all x_j are divisible by sqrt2, lower k by one; otherwise pair the entries not divisible by sqrt2 (an even number by eq_3). (eq_2, eq_3)
3. For each pair (j,l), apply a 2-level T^m_{[j,l]} followed by a 2-level H_{[j,l]} as in eq_4 (recording the gates), lowering the denominator exponent of that pair by one; repeat until the column has k = 0, at which point it is a unit basis vector times a power of omega, fixed by 1-level T^m and a permutation (X/CNOT-type) operator. Then recurse on the remaining columns (the reduced matrix stays unitary over D[omega]). (eq_4, eq_3)
4. Circuit assembly: when U has been reduced to the identity, the recorded 1- and 2-level operators G_1, ..., G_r satisfy G_r ... G_1 U = I, so U = G_1^dagger ... G_r^dagger; expand each 1- or 2-level operator into Clifford+T gates (trivial for n = 1; the n = 2 expansion is the paper's contribution and is not reconstructed) and output the gate list, which has length O(k) by eq_5. (eq_4, eq_5)

## Assumptions

- No experiment_scope was supplied; the single-qubit (n = 1) case with the tiny instance U = T H (k = 2 in the abstract's normal form) was chosen as the smallest useful construction.
- The denominator exponent k in the O(k) bound is taken to be the least denominator exponent of U.
- The reduction mechanism (eqs. 2-4) is reconstructed from standard Giles-Selinger / Kliuchnikov-Maslov-Mosca background, which the abstract cites as the basis of its method; the paper's new ingredients are not reproduced.
- Ancilla initialized to and returned to |0>; global phase treated as free.
- Gate counts are in the Clifford+T gate set {H, S, T, CNOT} (and their inverses/powers), with no fixed counting convention taken from the abstract.

## Missing information

- The paper's specific new method for realizing 2-level H and T operators on two qubits in Clifford+T (which is what distinguishes it from Giles-Selinger) is not described in the abstract.
- Explicit constants in the O(k) gate bound and the gate-counting convention (total gates vs. T-count).
- The precise pairing/residue rule used to choose the 2-level operations and the exponent m in eq_4 for n = 2.
- How and when the single ancilla is introduced and discharged, and whether the ancilla is required for all n = 2 operators or only those with odd-power-of-omega determinant.
- Whether k denotes the least denominator exponent or any valid exponent, and whether entries are first normalized.
