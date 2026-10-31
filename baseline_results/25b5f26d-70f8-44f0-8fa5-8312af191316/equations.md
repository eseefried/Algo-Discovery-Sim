# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Decompose an n-qubit diagonal Hermitian quantum gate D (a diagonal unitary with all diagonal entries in {+1,-1}) into a product of multiple-controlled Z gates (Z, CZ, CCZ, ...), by mapping D to a binary vector over GF(2) and expressing that vector in the basis formed by the binary representations of the multiple-controlled Z gates.

Scope: Scoped to: (i) the characterization of diagonal Hermitian gates as D = sum_x (-1)^{f(x)} |x><x| with a Boolean function f, (ii) a binary (GF(2)) representation of such gates in which gate multiplication becomes XOR, (iii) the fact that the multiple-controlled Z gates correspond to the monomial (algebraic-normal-form) basis of Boolean functions, (iv) the resulting exact decomposition via Mobius inversion, and (v) one tiny explicit instance (n = 2, D = diag(1,-1,-1,-1) = Z_1 Z_2 CZ_{12}). Outside scope: the paper's exact definition/encoding conventions for the binary representation, the further decomposition of multiple-controlled Z gates into the CZ-plus-single-qubit library, the cost model, the optimization procedure, and the reported experimental cost comparisons against prior multiplexed-R_z decompositions.

## Symbols

- $n$: number of qubits acted on by the diagonal gate; domain: positive integer
- $x=(x_1,\dots,x_n)$: computational-basis bit string; qubit 1 is the most significant bit, integer index idx(x)=\sum_{i=1}^{n} x_i 2^{n-i}; domain: \{0,1\}^n
- $D$: diagonal Hermitian (hence also unitary, D^2=I) gate to be decomposed; domain: 2^n \times 2^n diagonal matrix with entries in \{+1,-1\}
- $f$: Boolean function encoding the signs of D, d_x=(-1)^{f(x)}; domain: f:\{0,1\}^n\to\{0,1\}
- $b(D)$: binary representation of D: the truth table of f as a vector; domain: \mathrm{GF}(2)^{2^n}
- $S$: subset of qubit indices on which a multiple-controlled Z gate acts (|S|=1: Z, |S|=2: CZ, |S|=3: CCZ, ...); domain: S\subseteq [n]=\{1,\dots,n\}
- $C^{S}Z$: multiple-controlled Z gate applying phase -1 exactly when all qubits in S are 1; domain: 2^n\times 2^n diagonal unitary
- $m_S$: monomial Boolean function m_S(x)=\prod_{i\in S}x_i (m_\emptyset\equiv 1); binary representation of C^{S}Z; domain: \mathrm{GF}(2)^{2^n}
- $a_S$: coefficient of m_S in the GF(2) expansion of f (algebraic normal form coefficient); domain: \{0,1\}
- $1_T$: bit string with x_i=1 for i\in T and x_i=0 otherwise; domain: \{0,1\}^n

## eq_1: Diagonal Hermitian gate as a sign function

$$
D=\sum_{x\in\{0,1\}^n}(-1)^{f(x)}\,|x\rangle\langle x|,\qquad f:\{0,1\}^n\to\{0,1\},\qquad D^2=I
$$

A diagonal gate that is both unitary and Hermitian has real diagonal entries of modulus 1, i.e. each entry is +1 or -1, so it is fully specified by a Boolean function f.

Provenance: `abstract_inferred`. Diagonal unitary entries have |d_x|=1; Hermiticity forces d_x real; hence d_x in {+1,-1} and d_x=(-1)^{f(x)}.

Abstract evidence: a special class of diagonal quantum gates, namely diagonal Hermitian quantum gates

Equation assumptions:

- Gates are considered as exact matrices; global phase is tracked separately via the constant term (see eq_4).

## eq_2: Binary representation and its homomorphism property

$$
b(D)=\big(f(0),f(1),\dots,f(2^n-1)\big)\in\mathrm{GF}(2)^{2^n},\qquad b(D_1D_2)=b(D_1)\oplus b(D_2)
$$

The binary representation is the truth table of f indexed by idx(x). Because (-1)^{f_1(x)}(-1)^{f_2(x)}=(-1)^{f_1(x)\oplus f_2(x)}, multiplying diagonal Hermitian gates corresponds to XOR of their binary representations, giving a GF(2) vector space.

Provenance: `abstract_inferred`. The abstract introduces a binary representation forming a vector space; the natural choice consistent with eq_1 is the truth table of f with XOR as addition. The paper's exact indexing convention is not given, so the idx(x) ordering above is a stated convention.

Abstract evidence: a binary representation for the diagonal Hermitian gates is introduced

Equation assumptions:

- Truth-table encoding with qubit 1 as most significant bit is a chosen convention, not sourced from the abstract.

## eq_3: Multiple-controlled Z gate and its binary representation

$$
C^{S}Z=\sum_{x}(-1)^{\prod_{i\in S}x_i}|x\rangle\langle x|=I-2\,|1_S\rangle\langle 1_S|\otimes I_{[n]\setminus S},\qquad b(C^{S}Z)=m_S,\;\; m_S(x)=\prod_{i\in S}x_i
$$

C^{S}Z applies -1 exactly when all qubits in S equal 1; its binary representation is the monomial m_S. S={i} gives Z_i, S={i,j} gives CZ_{ij}, |S|=3 gives CCZ.

Provenance: `standard_background`. Standard definition of multiple-controlled Z gates; they are symmetric in control/target so only the set S matters.

## eq_4: Monomials form a GF(2) basis (expansion of f)

$$
f(x)=\bigoplus_{S\subseteq[n]}a_S\,m_S(x),\qquad a_S\in\{0,1\},\qquad \{m_S\}_{S\subseteq[n]}\ \text{is a basis of}\ \mathrm{GF}(2)^{2^n}
$$

Every Boolean function has a unique algebraic normal form over GF(2); the 2^n monomials are linearly independent and span the space of all binary representations. The nonempty-S monomials are the binary representations of the multiple-controlled Z gates; S=empty corresponds to the global phase -I.

Provenance: `abstract_explicit`. The abstract states the basis property; the ANF/monomial basis is the standard realization of it given eq_2 and eq_3.

Abstract evidence: the binary representations of multiple-controlled $Z$ gates form a basis for the vector space that is produced by the binary representations of all diagonal Hermitian quantum gates

Equation assumptions:

- The constant monomial m_empty (global phase -I) is either included as a trivial 'zero-controlled Z' element or the decomposition is taken up to global phase; the abstract does not say which.

## eq_5: Coefficient extraction (Mobius inversion over GF(2))

$$
a_S=\bigoplus_{T\subseteq S}f(1_T)
$$

Exact formula for the unique ANF coefficients: a_S is the XOR of f over all bit strings whose support is a subset of S. Equivalent to solving the linear system over GF(2) for the coordinates of b(D) in the monomial basis.

Provenance: `standard_background`. Standard Mobius transform for the algebraic normal form of Boolean functions; computable in O(n 2^n) XOR operations via the fast transform.

## eq_6: Decomposition of D into multiple-controlled Z gates

$$
D=(-1)^{a_\emptyset}\prod_{\emptyset\neq S\subseteq[n],\ a_S=1}C^{S}Z\qquad(\text{exact equality; factors commute})
$$

Writing b(D) in the monomial basis (eq_4, eq_5) and mapping back through eq_2 and eq_3 yields D exactly as a product of the multiple-controlled Z gates whose coefficient a_S equals 1, times a global sign.

Provenance: `abstract_inferred`. Direct consequence of eq_2 (products map to XOR), eq_3 (basis elements are C^S Z) and eq_4; all factors are diagonal so order is irrelevant.

Abstract evidence: the problem of decomposing a given diagonal Hermitian gate is mapped to the problem of writing its binary representation in the specific basis mentioned above

Equation assumptions:

- Gate count equals the Hamming weight of (a_S)_{S\neq\emptyset}; whether the paper further optimizes beyond this unique expansion (e.g. via the CZ-based library) is not determinable from the abstract.

## eq_7: Tiny explicit instance (n = 2)

$$
D=\mathrm{diag}(1,-1,-1,-1),\quad f(x_1,x_2)=x_1\oplus x_2\oplus x_1x_2,\quad a_{\{1\}}=a_{\{2\}}=a_{\{1,2\}}=1,\ a_\emptyset=0,\quad D=Z_1\,Z_2\,CZ_{12}
$$

Truth table f(00)=0, f(01)=1, f(10)=1, f(11)=1. Mobius inversion gives all three nonconstant coefficients equal to 1, so D = Z on qubit 1, Z on qubit 2, and CZ on both. Check: diag(1,-1,-1,1) * diag(1,1,1,-1) = diag(1,-1,-1,-1).

Provenance: `assumption`. Chosen as the smallest instance in which all three two-qubit basis elements appear; verified by direct matrix multiplication of 4x4 diagonals.

Equation assumptions:

- Instance chosen by the reconstructor; not taken from the paper.

## Registers

- q: n (instance: 2) qubits; data register on which the diagonal Hermitian gate D acts; qubit 1 is the most significant bit of the index idx(x)

## Classical postprocessing

The entire decomposition is classical preprocessing: computing the ANF coefficients a_S of the truth table of f (eq_5) and emitting the corresponding gate list (eq_6). No quantum measurement or quantum postprocessing is involved; correctness can be checked classically by multiplying the emitted diagonal matrices.

## Algorithm steps

1. Read the Boolean sign function f from the diagonal of D: f(x)=0 if d_x=+1 and f(x)=1 if d_x=-1; form the binary representation b(D). (eq_1, eq_2)
2. Classically compute the GF(2) coordinates a_S of b(D) in the monomial basis by Mobius inversion (fast XOR transform). (eq_4, eq_5)
3. Emit one multiple-controlled Z gate C^{S}Z for every nonempty S with a_S=1 (in any order, since all factors are diagonal); record a_empty as a global sign. (eq_3, eq_6)
4. Instance: for D=diag(1,-1,-1,-1) on 2 qubits, emit Z_1, Z_2, CZ_{12}. (eq_7)

## Assumptions

- Binary representation is taken to be the truth table of f over GF(2) with qubit 1 as the most significant bit; the paper's exact encoding may differ.
- Global phase (-I, the empty monomial) is tracked as a sign and not realized as a gate.
- The decomposition in eq_6 is the unique ANF expansion; any further cost optimization or alternative choice of representatives in the paper is not reconstructed.
- Instance n=2, D=diag(1,-1,-1,-1) chosen by the reconstructor as the smallest useful example.

## Missing information

- Exact definition and ordering conventions of the paper's binary representation.
- How multiple-controlled Z gates (|S|>=3) are further decomposed into the CZ-plus-single-qubit library and the resulting cost model.
- The optimization procedure and the quantitative experimental cost comparisons with the previous multiplexed-R_z-based decomposition.
- Whether the paper treats gates exactly or up to global phase.
