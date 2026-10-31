# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Characterize which self-inverse reversible functions f on n bits (involutions in S_{2^n}) can be realized by a palindromic reversible circuit, i.e., a gate sequence equal to its own reverse, and give a tiny explicit palindromic realization.

Scope: Finite scope chosen here (no experiment_scope supplied): n-line reversible circuits over the library of NOT, CNOT and multiple-controlled Toffoli gates (all involutive), the formal definition of palindromic circuits, the structural consequence f = C g C^{-1}, a candidate cycle-type criterion derived from it, and one explicit instance on n=3 lines (the transposition swapping |000> and |111>, realized by a 9-gate palindrome). Outside scope: the paper's exact statement/proof of the realizability theorem, the constructions using an extra circuit line, and the constructions using quantum (non-permutation) gates for non-realizable involutions; the abstract gives no details of these.

## Symbols

- $n$: number of circuit lines / Boolean variables; domain: positive integer; instance uses n=3
- $x=(x_1,\dots,x_n)$: basis state of the n lines, encoded as integer \sum_{i=1}^{n} x_i 2^{i-1} (line 1 is the least significant bit); domain: \{0,1\}^n \cong \{0,\dots,2^n-1\}
- $f$: reversible function, a bijection on \{0,1\}^n, identified with a permutation in S_{2^n}; domain: S_{2^n}
- $S_{2^n}$: symmetric group on the 2^n basis states; domain: finite group of order (2^n)!
- $G=(g_1,\dots,g_k)$: reversible circuit as an ordered gate list, g_1 applied first; domain: finite sequence of gates from the library
- $G^R$: reverse circuit (g_k,\dots,g_1); domain: finite gate sequence
- $T_{c}$: Toffoli gate with c control lines (c=0 is NOT, c=1 is CNOT) and one target line; domain: involutive permutation of \{0,1\}^n
- $t(f)$: number of disjoint transpositions (2-cycles) in the cycle decomposition of the involution f; domain: integer in \{0,\dots,2^{n-1}\}
- $C$: conjugating permutation realized by the first half of an odd-length palindrome; domain: S_{2^n}

## eq_1: Self-inverse reversible functions are involutions of S_{2^n}

$$
f \in S_{2^n},\quad f \circ f = \mathrm{id} \iff f = f^{-1} \iff f^2 = e
$$

A reversible function on n variables is a permutation of the 2^n basis states; it is self-inverse exactly when it is an involution (including the identity).

Provenance: `abstract_explicit`. Direct restatement of the abstract's identification of self-inverse functions with involutions.

Abstract evidence: involutions in the symmetric group $S_{2^{n}}$ which are isomorphic to self-inverse reversible function on $n$ variables

Equation assumptions:

- Basis states encoded as integers via x \mapsto \sum_i x_i 2^{i-1}.

## eq_2: Circuit function, reverse circuit, and palindromic condition

$$
f_G = g_k \circ \cdots \circ g_1,\qquad f_{G^R} = g_1 \circ \cdots \circ g_k = f_G^{-1}\ (\text{if } g_i^2=e),\qquad G \text{ palindromic} \iff g_i = g_{k+1-i}\ \forall i
$$

The circuit computes the composition of its gates; with involutive gates the reverse circuit computes the inverse function; a palindromic circuit is one identical to its reverse, hence realizes a self-inverse function.

Provenance: `abstract_inferred`. Formalization of 'equal to their reverse circuit'; the inverse property uses the standard fact that NOT/CNOT/Toffoli gates are involutions.

Abstract evidence: reversible circuits that are equal to their reverse circuit, which are called palindromic circuits

Equation assumptions:

- Gate library consists of involutive gates (NOT, CNOT, multiple-controlled Toffoli).

## eq_3: Structure of palindromic circuits

$$
k=2m+1:\ f_G = C \circ g_{m+1} \circ C^{-1},\ C = g_m \circ \cdots \circ g_1;\qquad k=2m:\ f_G = \mathrm{id}
$$

An odd-length palindrome realizes a conjugate of its single middle gate; an even-length palindrome over involutive gates realizes the identity.

Provenance: `standard_background`. Follows algebraically from eq_2: the second half of the palindrome is the inverse of the first half when all gates are involutions.

Equation assumptions:

- Involutive gate library as in eq_2.

## eq_4: Cycle type of a Toffoli gate

$$
T_c \text{ on } n \text{ lines} = \prod_{j=1}^{2^{\,n-1-c}} (a_j\ b_j),\quad\text{so } t(T_c) = 2^{\,n-1-c},\ 0 \le c \le n-1
$$

A Toffoli gate with c controls flips the target on exactly 2^{n-1-c} input pairs that differ only in the target bit; it is a product of that many disjoint transpositions. Conjugation by C preserves cycle type.

Provenance: `standard_background`. Standard counting of inputs satisfying the control condition; conjugacy classes of S_N are determined by cycle type.

Equation assumptions:

- Controls may be positive or negative; this does not change the cycle type.

## eq_5: Candidate realizability criterion (derived, not taken from the paper)

$$
f \text{ realizable as palindromic circuit} \iff t(f) \in \{0\} \cup \{2^{j} : 0 \le j \le n-1\}
$$

Combining eq_3 and eq_4: palindromic circuits over Toffoli gates realize exactly the identity and the conjugates of single Toffoli gates, i.e., involutions whose number of transpositions is a power of two not exceeding 2^{n-1}. Sufficiency uses that NOT/CNOT/Toffoli generate all of S_{2^n}, so any f of matching cycle type is some conjugate C T_c C^{-1}.

Provenance: `assumption`. This is the criterion implied by eq_3-eq_4 under the involutive-Toffoli gate library; the abstract only says the class is 'precisely determined' and the paper's actual statement is not available here.

Equation assumptions:

- Gate library is exactly NOT/CNOT/multiple-controlled Toffoli (no ancilla, no quantum gates).
- Generation of S_{2^n} by this library for n \ge 3 (and S_4 for n=2) is used for sufficiency.

## eq_6: Tiny instance: n=3, f=(000\ 111) as a 9-gate palindrome

$$
f=(000\ 111)=C\,T_{1,2\to 3}\,C^{-1},\ C = X_1 X_2\,\mathrm{CNOT}_{3\to1}\mathrm{CNOT}_{3\to2};\quad G=(X_1,X_2,\mathrm{CNOT}_{3\to1},\mathrm{CNOT}_{3\to2},T_{1,2\to3},\mathrm{CNOT}_{3\to2},\mathrm{CNOT}_{3\to1},X_2,X_1)
$$

The Toffoli T_{1,2->3} swaps 110 and 111; C maps 110->000 and 111->111, so C T C^{-1} swaps 000 and 111 and fixes all other states. The gate list is its own reverse. By contrast, an involution such as (001\ 010)(011\ 100)(101\ 110) with t(f)=3 violates eq_5 and would need the paper's extra-line or quantum constructions.

Provenance: `assumption`. Explicit small example constructed from eq_3; checked by hand on the inputs 000, 111 and 001 under the stated bit encoding.

Equation assumptions:

- Bit string written as x_1x_2x_3 with line 1 leftmost in the string; gates applied left to right.

## Registers

- lines: n (instance: 3) qubits; the n reversible circuit lines carrying the input x and, after the circuit, f(x)

## Initial state

Computational basis state |x_1 x_2 ... x_n> for the input x to be mapped; no ancilla lines in the chosen scope.

## Classical postprocessing

Verification only: apply the circuit to each of the 2^n basis inputs (classical simulation of permutation gates) and check that the resulting truth table equals f and that the gate list equals its reverse.

## Algorithm steps

1. Given an involution f (eq_1), compute its cycle decomposition and the number of transpositions t(f). (eq_1)
2. Decide realizability with the cycle-type criterion: t(f) must be 0 or a power of two 2^j with j <= n-1 (derived criterion, see assumptions). (eq_4, eq_5)
3. If realizable with t(f)=2^{n-1-c}, pick a Toffoli gate T_c with the same cycle type and find a permutation C with f = C T_c C^{-1}; synthesize C as a Toffoli-gate circuit (g_1,...,g_m). (eq_3, eq_4)
4. Output the palindrome G = (g_1,...,g_m, T_c, g_m,...,g_1), which satisfies g_i = g_{k+1-i} and computes f. (eq_2, eq_3)
5. Instance n=3: f=(000 111) realized by the explicit 9-gate palindrome. (eq_6)

## Assumptions

- No experiment_scope was supplied; the smallest useful construction (odd-length palindrome as conjugate of one Toffoli gate) and the instance n=3, f=(000 111) were chosen by the reconstruction.
- Gate library restricted to NOT, CNOT and multiple-controlled Toffoli gates, all of which are involutions.
- The realizability criterion eq_5 is derived from group-theoretic reasoning, not read from the paper; the paper's precise theorem may be stated differently or use a different gate library.
- Integer encoding x = sum_i x_i 2^{i-1}; gate sequences are applied left to right.

## Missing information

- The paper's exact statement and proof of which self-inverse functions admit palindromic circuits.
- The construction with one extra circuit line for non-realizable involutions (how the function is embedded and which palindromic form is used).
- The construction using quantum gates (e.g., which non-permutation gates, such as controlled roots of NOT, are allowed and how palindromicity is defined for them).
- Whether negative controls, mixed-polarity gates, or other gate libraries are permitted in the paper's definition.
