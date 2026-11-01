# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Exact synthesis of an n-qubit (n<=2) unitary with entries in Z[i,1/sqrt2] into a Clifford+T circuit of O(k) gates with at most one ancilla, via decomposition into 1- and 2-level matrices (Giles-Selinger approach).

Scope: Only the algebraic ring/entry form, the unitarity constraint, and the generic two-level reduction step for one tiny instance (n=1 or 2, dimension N=2^n) are specified. The paper-specific new method, its O(k) gate-count proof, and the ancilla construction are outside scope.

## Symbols

- $n$: number of qubits; domain: integer, n<=2
- $N$: matrix dimension 2^n; domain: integer in {2,4}
- $U$: operator to synthesize; domain: N x N unitary over Z[i,1/sqrt2]
- $a,b,c,d$: integer coefficients of an entry; domain: integers
- $k$: denominator exponent of sqrt2; domain: nonnegative integer
- $E_j$: two-level matrix acting nontrivially on two basis indices; domain: unitary over the same ring

## eq_1: Entry form

$$
u=\frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{\,k}},\quad a,b,c,d\in\mathbb{Z}
$$

Form of each entry of U.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: of the form $\frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{k}}$

Equation assumptions:

- A common k is used for all entries.

## eq_2: Unitarity

$$
U^\dagger U=I_N
$$

Operator being decomposed must be unitary.

Provenance: `standard_background`. Quantum operators that are exactly synthesizable are unitary; the abstract does not state this explicitly.

## eq_3: Two-level decomposition

$$
U=E_1E_2\cdots E_m,\quad E_j \text{ acts nontrivially on two basis states}
$$

Factorization into 1- and 2-level matrices (1-level being diagonal phases).

Provenance: `abstract_inferred`. The abstract names this decomposition; the exact form is standard background and not given.

Abstract evidence: using decomposition into $1$- and $2$-level matrices which was first proposed by Giles and Selinger

Equation assumptions:

- 1-level matrices are diagonal phase factors.

## eq_4: Gate bound

$$
\#\text{gates}=O(k)
$$

Claimed gate count scaling for n<=2 with at most one ancilla.

Provenance: `abstract_explicit`. Stated in the abstract; constants are unspecified.

Abstract evidence: This method achieves a bound of $O(k)$ gates using at most one ancilla

## eq_5: Two-level elimination step

$$
E\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x'\\0\end{pmatrix}
$$

Generic step that zeroes one entry of a column using a 2x2 unitary over the ring.

Provenance: `assumption`. Generic Giles-Selinger-style reduction; the paper's specific reduction is not given.

Equation assumptions:

- The specific choice of E and its Clifford+T implementation are not known from the abstract.

## Registers

- data: n (<=2) qubits; qubits acted on by U
- ancilla: 0 or 1 qubits; optional helper qubit

## Algorithm steps

1. Check that entries have the form in eq_1 with common k and that U is unitary. (eq_1, eq_2)
2. Reduce U column by column using two-level elimination steps, leaving a 1-level diagonal. (eq_3, eq_5)
3. Implement each 1- and 2-level factor in Clifford+T, with at most one ancilla, for a total gate count O(k). (eq_4)

## Assumptions

- No instance is fixed beyond N=2^n with n<=2.
- Giles-Selinger two-level framework is used only as background.

## Missing information

- The paper's actual reduction and its choice of two-level matrices
- Clifford+T implementation of each factor
- Role and construction of the ancilla
- Proof and constants of the O(k) bound
- Handling of global phase
