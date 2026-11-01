# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given an involution f in S_{2^n} (f(f(x))=x) as a permutation table on n lines, build a palindromic reversible circuit G=g1...gk...g1 (gate list equal to its reverse) over NOT/CNOT/Toffoli that computes f on the data lines, or, when not possible, an alternative palindromic representation using one extra ancilla line or controlled-V/V-dagger gates.

Scope: Tiny instances n=2,3 (up to 4 qubits including one ancilla). Covers: involution cycle decomposition, palindrome-as-involution property, parity obstruction check, conjugation form h c h^{-1}, and the verification readout. Outside scope: the paper's exact characterization theorem of which involutions are palindromic, the general ancilla construction proof, and the V/V-dagger construction details and their optimality.

## Symbols

- $n$: number of data lines; domain: integer, 2<=n<=4
- $f$: self-inverse reversible function (involution); domain: permutation of {0,1}^n with f∘f=id
- $g_i$: self-inverse gate (NOT, CNOT, Toffoli); domain: gate library NCT on the lines
- $G$: palindromic circuit g_1...g_k...g_1, or g_1...g_k c g_k...g_1 with a central self-inverse gate c; domain: permutation of {0,1}^n (or n+1 lines)
- $h, c$: conjugator circuit and self-inverse middle block; domain: reversible circuits
- $\mathrm{sgn}(f)$: parity of the permutation f: (-1)^{number of transpositions}; domain: {+1,-1}
- $t(f)$: number of 2-cycles of f; domain: nonnegative integer
- $V$: square root of NOT, V^2=X; domain: 2x2 unitary

## eq_1: Involution

$$
f(f(x))=x\ \ \forall x\in\{0,1\}^n,\quad f=\prod_{j=1}^{t(f)}(a_j\ b_j)
$$

Involution is a product of disjoint transpositions with remaining points fixed.

Provenance: `abstract_inferred`. Self-inverse functions correspond to involutions in the symmetric group, which have cycle type of 2-cycles and fixed points (standard group theory).

Abstract evidence: involutions in the symmetric group $S_{2^{n}}$ which are isomorphic to self-inverse reversible function on $n$ variables

Equation assumptions:

- f given as an explicit table

## eq_2: Palindrome equals reverse

$$
G=g_1 g_2\cdots g_k\cdots g_2 g_1,\quad G^{-1}=g_1\cdots g_k\cdots g_1=G
$$

A palindrome of self-inverse gates equals its reverse circuit and is hence an involution.

Provenance: `abstract_inferred`. Reverse circuit of self-inverse gates is the mirrored gate list; palindrome means mirror equals itself.

Abstract evidence: reversible circuits that are equal to their reverse circuit, which are called palindromic circuits

Equation assumptions:

- each gate is self-inverse (NOT, CNOT, Toffoli)
- central gate, if present, is self-inverse

## eq_3: Conjugation form

$$
G=h\,c\,h^{-1},\quad c^2=\mathrm{id}
$$

Candidate palindrome via conjugating a self-inverse middle block c by h; if h is written as gates and h^{-1} is its mirror, G is palindromic when c is palindromic.

Provenance: `assumption`. Sketch's proposed structure; the exact sufficiency/necessity conditions are not given in the abstract.

Equation assumptions:

- c is itself a palindromic circuit or single self-inverse gate

## eq_4: Parity obstruction

$$
n\ge 4,\ G\in\langle \mathrm{NCT}\rangle_n\Rightarrow \mathrm{sgn}(G)=+1;\ \text{obstructed if } t(f)\text{ odd}
$$

On n>=4 lines NCT gates generate only even permutations, so an involution with an odd number of 2-cycles cannot be built without an extra line.

Provenance: `standard_background`. Known result on parity of reversible gates (Toffoli's even-permutation theorem); for n<=3 other obstructions may occur and are not specified here.

Equation assumptions:

- no ancilla
- NCT only

## eq_5: Ancilla variant

$$
A\,|x\rangle|0\rangle=|f(x)\rangle|0\rangle,\quad A=A^{-1}\text{ palindromic on }n+1\text{ lines}
$$

Circuit on n+1 lines acting as f on data and restoring ancilla to 0.

Provenance: `assumption`. Sketch requirement; concrete construction not given.

Equation assumptions:

- a single extra line suffices

## Registers

- data: n qubits; holds x in {0,1}^n, bit i = qubit i (little-endian, x=sum x_i 2^i)
- anc: 0 or 1 qubits; optional ancilla, qubit index n, initialized |0> and returned to |0>

## Initial state

|x>_data|0>_anc for each basis input x in {0,...,2^n-1}

## Measurement

Statevector simulation without measurement (or measure data bits only if counts requested); read output basis state; mind little-endian bit order.

## Classical postprocessing

Compare output index to f(x); check ancilla bit is 0; check gate list palindrome; check G·G=id.

## Algorithm steps

1. Decompose f into transpositions and fixed points; compute t(f) and parity. (eq_1, eq_4)
2. Search small NCT palindromes (gate sequences up to some length, optional central gate) for one whose permutation equals f, e.g. via conjugation of a simple middle gate. (eq_2, eq_3)
3. If none exists, search palindromes on n+1 lines with ancilla returning to 0; otherwise a controlled-V/V-dagger palindrome. (eq_5)
4. Verify for all basis inputs: output equals f(x), ancilla 0, gate list equals reverse, and G applied twice is identity. (eq_1, eq_2)

## Assumptions

- Chosen target: n=2 or 3 instances given as explicit permutation tables
- Gate library NCT plus controlled-V/V-dagger for the quantum variant
- Palindromic means identical gate sequence when reversed (V and V-dagger mirror placement needs care since V reversed is V-dagger)
- Only one extra line allowed

## Missing information

- Exact necessary-and-sufficient characterization of palindromic-realizable involutions
- Explicit ancilla construction
- Exact V/V-dagger palindrome construction (reverse of V is V†, so symmetric placement must be defined)
- Cost metrics and gate set specifics
