# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Decompose an n-qubit diagonal Hermitian gate D = diag((-1)^{f(x)}) into a product of multi-controlled Z gates by writing the GF(2) binary representation of f in the monomial (ANF) basis, then build the circuit with MCZ gates and compare with D by statevector or unitary simulation.

Scope: One tiny instance: n=3 with f given as a length-8 truth table of bits. Compute the ANF coefficients c_S by the binary Moebius transform, apply one MCZ per S with c_S=1 on n data qubits with no ancillas and no measurement, and verify against diag((-1)^f) up to global phase. Gray-code ordering, gate sharing, and the paper's cost comparison against multiplexed-Rz are outside this scope.

## Symbols

- $n$: number of qubits; domain: positive integer, small (e.g. 3)
- $x$: computational basis index with bits x_{n-1}...x_0, where qubit i holds x_i (little-endian); domain: {0,1}^n, integer 0..2^n-1
- $f$: sign function of the gate, with D|x> = (-1)^{f(x)}|x>; domain: f:{0,1}^n -> {0,1}
- $b$: binary representation of D, b[x]=f(x); domain: GF(2)^{2^n}
- $S$: nonempty subset of qubit indices; domain: subsets of {0,...,n-1}
- $c_S$: ANF coefficient, equal to 1 if MCZ_S is applied; domain: GF(2)
- $v_S$: binary representation of MCZ_S, v_S[x]=prod_{i in S} x_i; domain: GF(2)^{2^n}

## eq_1: Diagonal Hermitian entries are signs

$$
D=D^\dagger,\ D^\dagger D=I,\ D\ \text{diagonal}\ \Rightarrow\ D_{xx}\in\{+1,-1\},\ D_{xx}=(-1)^{f(x)}
$$

A Hermitian unitary diagonal gate has real unit-modulus entries, so each is +1 or -1.

Provenance: `abstract_inferred`. Hermitian implies real diagonal entries and unitarity implies modulus 1, so the entries are +/-1. This is the standard inference, not a quoted formula.

Abstract evidence: diagonal Hermitian quantum gates

Equation assumptions:

- Diagonal gate is exactly unitary

## eq_2: MCZ binary representation

$$
v_S[x]=\prod_{i\in S}x_i,\quad \mathrm{MCZ}_S|x\rangle=(-1)^{v_S[x]}|x\rangle
$$

The binary vector of the multi-controlled Z on S is the indicator that all x_i with i in S equal 1.

Provenance: `abstract_inferred`. The abstract says MCZ binary representations form a basis. The explicit vector form is inferred from the definition of MCZ and the sketch.

Abstract evidence: the binary representations of multiple-controlled $Z$ gates form a basis

Equation assumptions:

- Binary representation is the sign-exponent truth table

## eq_3: ANF decomposition over GF(2)

$$
f(x)=\bigoplus_{S\neq\emptyset}c_S\prod_{i\in S}x_i\ \oplus c_\emptyset,\quad b=\bigoplus_S c_S v_S
$$

Writing the binary representation in the MCZ basis is the algebraic normal form of f. The constant term c_empty only gives a global phase.

Provenance: `abstract_inferred`. The abstract states the mapping to basis expansion. The identification with ANF/Reed-Muller is background recalled from the sketch.

Abstract evidence: the problem of decomposing a given diagonal Hermitian gate is mapped to the problem of writing its binary representation in the specific basis mentioned above

Equation assumptions:

- Basis is the monomial ANF indicators
- Constant term is dropped as a global phase

## eq_4: Binary Moebius transform

$$
c_S=\bigoplus_{x\subseteq S}f(x),\ \text{with } x \text{ identified with its support set}
$$

Closed-form solution of the triangular system, computed in O(n 2^n) by the fast Moebius butterfly: for each bit i and each x with x_i=1, set b[x] <- b[x] xor b[x with bit i cleared].

Provenance: `standard_background`. Standard Moebius inversion for ANF over GF(2). It is not stated in the abstract.

Equation assumptions:

- Index x is bitmask of support

## eq_5: Circuit as product of commuting MCZ

$$
D\simeq\prod_{S\neq\emptyset:\,c_S=1}\mathrm{MCZ}_S\ \text{(up to global phase }(-1)^{c_\emptyset})
$$

D equals the product of MCZ gates over the support of c, in any order since all are diagonal. The gate count equals the Hamming weight of c over nonempty S.

Provenance: `abstract_explicit`. Directly stated; the product formula follows from eq_3 and the fact that diagonal gates commute.

Abstract evidence: these gates can be decomposed to a set that solely consists of multiple-controlled $Z$ gates

Equation assumptions:

- Global phase ignored

## Registers

- q: n (3 for the tiny instance) qubits; data qubits, qubit i holds x_i; no ancillas

## Initial state

The runner reads the unitary or statevector; for a state check use a uniform superposition (H on all qubits) so every sign is observable as a relative phase. No measurement.

## Classical postprocessing

Classical computation of ANF coefficients by the Moebius transform, then a list of subsets S with c_S=1. Optionally order the MCZ gates (e.g. Gray code) to lower CZ count and depth.

## Algorithm steps

1. Take the truth table f (length 2^n) and form b[x]=f(x) with x as little-endian integer, qubit i = bit i. (eq_1)
2. Run the fast binary Moebius transform to obtain c_S for all S, and drop c_empty as global phase. (eq_3, eq_4)
3. For each nonempty S with c_S=1 apply Z (|S|=1), CZ (|S|=2), CCZ (|S|=3), or a general MCZ via standard gates, on qubits in S. Order is free. (eq_2, eq_5)
4. Compare the resulting unitary with diag((-1)^f) up to global phase. (eq_5)

## Assumptions

- Scope is one tiny instance, n=3, with f given as a truth table
- Entries are only +1 or -1
- Global phase is ignored
- Cost is judged after transpiling to u and cx

## Missing information

- The paper's exact binary representation convention
- The paper's ordering and sharing optimization
- How |S|>=3 MCZ gates are decomposed with CZ in the paper
- The numerical cost comparison with the multiplexed-Rz method
