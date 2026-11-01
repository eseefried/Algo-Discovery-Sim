# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Characterize which self-inverse reversible functions (involutions in S_{2^n}) can be realized as palindromic reversible circuits (circuits equal to their reverse), and construct alternatives with an extra line or quantum gates when not possible. The abstract gives no precise characterization criterion.

Scope: Background definitions only, plus a tiny assumed instance: n=2 bits, circuits over a gate library of self-inverse gates (e.g. NOT/CNOT/Toffoli). Covers the relation between palindromic circuits and involutions. The actual characterization theorem, the extra-line construction, and the quantum-gate construction are outside scope.

## Symbols

- $n$: number of circuit lines/variables; domain: positive integer
- $f$: reversible function on n bits, as a permutation of {0,...,2^n-1}; domain: S_{2^n}
- $C=g_1g_2\cdots g_k$: reversible circuit as a cascade of gates; domain: gate sequence
- $C^{R}$: reverse circuit g_k\cdots g_1; domain: gate sequence
- $g_i$: gate, assumed self-inverse (e.g. Toffoli); domain: permutation of {0,1}^n

## eq_1: Self-inverse function

$$
f\circ f=\mathrm{id},\quad f\in S_{2^n}
$$

Self-inverse reversible functions are involutions in the symmetric group on 2^n points (identity included).

Provenance: `abstract_inferred`. The abstract states the isomorphism between involutions and self-inverse functions; the defining relation f^2=id is the standard meaning of involution.

Abstract evidence: involutions in the symmetric group $S_{2^{n}}$ which are isomorphic to self-inverse reversible function on $n$ variables

Equation assumptions:

- Identity is counted as an involution

## eq_2: Palindromic circuit

$$
C=C^{R},\quad g_i=g_{k+1-i}\ \text{for } i=1,\dots,k
$$

A circuit is palindromic if it equals its reverse, i.e. the gate sequence reads the same in both directions.

Provenance: `abstract_inferred`. Direct reading of the definition as gate-sequence equality.

Abstract evidence: reversible circuits that are equal to their reverse circuit, which are called palindromic circuits

Equation assumptions:

- Equality is of gate sequences, not just of realized functions

## eq_3: Reverse circuit realizes inverse

$$
f_{C^{R}}=f_C^{-1}\ \text{when each } g_i^{-1}=g_i
$$

With self-inverse gates, the reverse circuit computes the inverse function.

Provenance: `standard_background`. Standard: (g_k\cdots g_1) is the inverse of g_1\cdots g_k when each gate is an involution.

Equation assumptions:

- All gates are self-inverse

## eq_4: Palindromic implies self-inverse

$$
C=C^{R}\Rightarrow f_C=f_C^{-1}\Rightarrow f_C\circ f_C=\mathrm{id}
$$

Any palindromic circuit over self-inverse gates realizes an involution; the converse (which involutions have a palindromic realization) is the paper's question and is not reconstructed.

Provenance: `abstract_inferred`. Follows from eq_2 and eq_3; the converse criterion is not given in the abstract.

Abstract evidence: We precisely determine which self-inverse functions can be realized as a palindromic circuit.

Equation assumptions:

- Self-inverse gate library

## Registers

- x: n (tiny instance: 2) qubits; data lines carrying the bit string, integer encoding x=\sum x_i 2^i (assumed)
- anc: 1 (optional) qubits; extra line used in the alternative palindromic representation (construction not specified)

## Algorithm steps

1. Represent a self-inverse reversible function on n bits as an involution in S_{2^n}. (eq_1)
2. Synthesize a circuit over self-inverse gates and test whether its gate sequence is palindromic. (eq_2, eq_3)
3. Note that palindromic realizations necessarily give involutions; the exact criterion for which involutions admit them is needed but not given. (eq_4)

## Assumptions

- Tiny instance n=2 chosen as the smallest useful illustration
- Gate library consists of self-inverse gates
- Classical reversible setting only

## Missing information

- Exact criterion for which involutions admit palindromic circuits
- Extra-line construction
- Quantum-gate construction
- Gate library used in the paper
- Cost or complexity results
