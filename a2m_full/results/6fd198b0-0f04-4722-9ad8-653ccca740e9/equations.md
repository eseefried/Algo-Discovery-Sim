# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Exact synthesis of an n<=2 qubit unitary U with entries in Z[i,1/sqrt2] (form (a+b sqrt2+i(c+d sqrt2))/sqrt2^k) into a Clifford+T circuit of O(k) gates using at most one ancilla, via Giles-Selinger decomposition into 1- and 2-level matrices.

Scope: Smallest useful instance: a 4x4 (n=2) unitary over Z[i,1/sqrt2] given explicitly with known sde k. Build the column-reduction into two-level matrices (classically), then compile each two-level matrix into Clifford+T gates (X, CX, H, S, T, Tdg, Toffoli decomposed) and verify via statevector/unitary comparison up to global phase. Out of scope: the paper's own optimized constants, its precise ancilla scheme for odd-determinant cases, the proof of O(k), and n>2.

## Symbols

- $U$: target unitary; domain: U(2^n), n<=2, entries in Z[i,1/sqrt2]
- $k$: least denominator exponent: smallest k with sqrt2^k U having entries in Z[omega]; domain: nonnegative integer
- $\omega$: primitive 8th root of unity e^{i\pi/4}, so T=diag(1,omega); domain: complex unit
- $E_{(j,l)}$: two-level unitary acting nontrivially only on basis states j,l; domain: 2x2 unitary block embedded in U(2^n)
- $v$: column of sqrt2^k U with entries in Z[omega]; domain: Z[omega]^{2^n}
- $m$: number of two-level factors; domain: integer, m<=6 for dim 4 and m<=28 for dim 8 per sketch (an assumed bound)

## eq_1: Ring form of entries

$$
u_{rs}=\frac{a+b\sqrt2+i(c+d\sqrt2)}{\sqrt2^{\,k}},\quad a,b,c,d\in\mathbb Z
$$

Entries of U lie in Z[i,1/sqrt2] with denominator exponent k.

Provenance: `abstract_explicit`. Stated directly in the abstract as the entry form.

Abstract evidence: of the form $\frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{k}}$

Equation assumptions:

- a,b,c,d are integers per entry

## eq_2: Two-level decomposition

$$
U=E_m E_{m-1}\cdots E_1 \ \ (\text{each } E_t \text{ a 1- or 2-level matrix})
$$

U is a product of 1- and 2-level matrices, obtained by reducing columns one at a time to standard basis vectors, with the last diagonal entries being powers of omega.

Provenance: `abstract_explicit`. The abstract names this decomposition. The ordering and the reduction to basis vectors follow Giles-Selinger from background knowledge.

Abstract evidence: decomposition into $1$- and $2$-level matrices which was first proposed by Giles and Selinger

Equation assumptions:

- Factors are listed in the order they are applied to U^dagger, then inverted

## eq_3: Gate-count bound

$$
\text{gates}(U)=O(k)\ \text{with at most one ancilla}
$$

Total Clifford+T gate count is linear in k.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: This method achieves a bound of $O(k)$ gates using at most one ancilla

Equation assumptions:

- n<=2

## eq_4: Single-column sde reduction step

$$
v\mapsto E v,\quad E=\begin{pmatrix}\alpha&\beta\\ \gamma&\delta\end{pmatrix}\in\{H\text{-type}\cdot\mathrm{diag}(\omega^p,\omega^q),\ X\text{-type}\},\ \ \mathrm{sde}(Ev)<\mathrm{sde}(v)
$$

A pair of entries (v_j,v_l) is lowered in sde by a phase correction by powers of omega and a Hadamard-like step, until the column is a basis vector times a power of omega.

Provenance: `assumption`. Recalled Giles-Selinger-style arithmetic; the exact case analysis (residues mod sqrt2) is not given in the abstract and is not reproduced here.

Equation assumptions:

- Pair choice and residue case analysis are left to the implementer

## eq_5: Embedding a 2-level matrix as a controlled single-qubit gate

$$
E_{(j,l)}=P^{\dagger}\,\mathrm{C}^{(n-1)}_{\text{pattern}}(W)\,P,\quad W\in U(2),\ W \text{ in the exact Clifford+T group}
$$

A Gray-code permutation P of X/CX gates makes the indices j,l adjacent, differing in one bit, so E acts as a single-qubit W on that target controlled by the remaining bits.

Provenance: `standard_background`. Standard construction for compiling two-level matrices.

Equation assumptions:

- For n=2 there is one control; W is synthesized by a Matsumoto-Amano/KMM normal form with O(k) gates

## Registers

- q: n (<=2) qubits; data qubits, little-endian: basis index = q1*2+q0
- anc: 0 or 1 qubits; optional ancilla starting and ending in |0>, used to realize controlled operations or fix a phase/determinant obstruction

## Initial state

Verification only: unitary or statevector comparison of the circuit against U on basis states, with ancilla in |0>.

## Classical postprocessing

Exact Z[omega] arithmetic for the column reduction and normal-form synthesis; compare the simulated unitary (ancilla-projected) with U up to global phase.

## Algorithm steps

1. Classically reduce each column of sqrt2^k U to a basis vector using two-level matrices over Z[omega] (sde-lowering H-type steps, omega-phase and X-type swap steps), recording the factors. (eq_1, eq_2, eq_4)
2. Invert and order the recorded two-level factors so their product is U, up to a final diagonal of omega powers, which is realized with T/S/Z gates and controlled phases. (eq_2)
3. Compile each factor: conjugate by X/CX to make the indices adjacent, synthesize the single-qubit W exactly in Clifford+T, and implement the control with a Toffoli or controlled-H/T identity, using the ancilla if needed (returned to |0>). (eq_5)
4. Concatenate all compiled factors; the total count is O(k) because the number of factors is bounded by a constant. (eq_3)

## Assumptions

- The input is an explicit exact matrix with ring entries and known k
- Dimension is at most 4 for the main circuit, with one ancilla extending to 8
- The global phase, a power of omega, is tracked classically or ignored
- Gate set is H, S, T, X, CX, with Toffoli decomposed into Clifford+T
- Each controlled two-level gate costs O(k) T gates
- The factor-count bounds (6 and 28) come from the task sketch, not the abstract

## Missing information

- Exact case analysis of the sde-reduction rules
- Exact ancilla construction and when it is needed
- Explicit Clifford+T circuits for controlled W
- Concrete constants in the O(k) bound
- Handling of phases and determinants not realizable without an ancilla
