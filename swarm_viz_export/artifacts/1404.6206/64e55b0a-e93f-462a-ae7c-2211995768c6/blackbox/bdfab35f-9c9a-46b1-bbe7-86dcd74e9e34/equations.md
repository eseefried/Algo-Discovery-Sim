# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Generate an orthonormal basis of n=3 qubit Bell-like states, each a 2^m-term superposition with amplitudes ±2^{-m/2}, by applying Hadamards on m qubits followed by a multi-qubit controlled-X (CNOT fan-out) layer, with an optional multi-controlled-X (Toffoli-type) variant. Input basis index x selects the basis state.

Scope: Single instance n=3, m=2 (m=1 also valid). Variant A: H on 2 controls then CNOT fan-out onto 1 target with f(c)=c1 xor c2. Variant B: H on 2 controls then a doubly-controlled X (CCX) on the target, a nonlinear f(c)=c1 AND c2. Both are generic family members, not the paper's exact two controlled-unitary gates. Qudit extension and entanglement/monogamy analysis are out of scope. Input loading by X gates is an optional parameter x in the build, and the unitary alone has columns |B_x>.

## Symbols

- $n$: total number of qubits; domain: integer, n=3
- $m$: number of Hadamard control qubits; states have 2^m terms; domain: integer, 1<=m<n
- $x=(a,y)$: input basis label; a in {0,1}^m sets signs, y in {0,1}^{n-m} sets target offset; domain: bit strings
- $f$: map {0,1}^m -> {0,1}^{n-m}; linear XOR (variant A) or AND (variant B); domain: Boolean function
- $|B_x\rangle$: output Bell-like basis state; domain: n-qubit pure state
- $W$: circuit unitary, controlled-X layer times H on controls; domain: unitary on 2^n dimensions

## eq_1: Bell-like state

$$
|B_{a,y}\rangle=2^{-m/2}\sum_{c\in\{0,1\}^m}(-1)^{a\cdot c}\,|c\rangle\,|f(c)\oplus y\rangle
$$

Output on input |a>|y>; a 2^m-term superposition with amplitudes ±2^{-m/2}.

Provenance: `abstract_inferred`. Equal-magnitude amplitudes are stated in the abstract; the H plus controlled-X realization is an assumed construction.

Abstract evidence: The Bell-like states in any basis is superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$).

Equation assumptions:

- controls are the first m qubits
- f is a Boolean function applied as X^{f(c)} on targets

## eq_2: Circuit unitary

$$
W=\Big(\sum_{c}|c\rangle\langle c|\otimes X^{f(c)}\Big)\,(H^{\otimes m}\otimes I^{\otimes(n-m)})
$$

H on controls then controlled-X on targets. Variant A: CNOT c1->t, CNOT c2->t. Variant B: CCX(c1,c2->t).

Provenance: `assumption`. Proposed concrete controlled-unitaries; the paper's two gates are not given in the abstract.

Equation assumptions:

- X-type controlled operation only

## eq_3: Orthonormality

$$
\langle B_{x}|B_{x'}\rangle=\langle x|W^\dagger W|x'\rangle=\delta_{x,x'}
$$

Outputs form an orthonormal basis because W is unitary.

Provenance: `standard_background`. A unitary maps an orthonormal basis to an orthonormal basis.

## eq_4: Instance maps

$$
f_A(c_1,c_2)=c_1\oplus c_2,\quad f_B(c_1,c_2)=c_1c_2
$$

Variant A gives a linear map (CNOT fan-out); variant B gives a nonlinear map (CCX). The two bases differ, so they can have different entanglement content offline.

Provenance: `assumption`. Smallest concrete choices; B illustrates a multi-controlled gate.

Equation assumptions:

- qubit order (c1,c2,t)

## eq_5: Multi-controlled-X

$$
C^{m}X=I-P_1\cdots P_m\otimes I+P_1\cdots P_m\otimes X,\quad P_k=|1\rangle\langle1|_k
$$

Standard multi-controlled-X: X on the target only if all controls are |1>. Used in variant B with m=2.

Provenance: `standard_background`. Standard definition. The specialist's predicted eq. (1) and (2) were rejected as not usable here (the first is malformed, the second concerns an unknown gate).

## Registers

- c: m=2 qubits; control qubits receiving H, the first qubits in the label
- t: n-m=1 qubits; target qubit receiving controlled-X

## Initial state

Computational basis state |a>|y> loaded by X gates for index x=(a,y). The label is written c1 c2 t with c1 leftmost; in Qiskit little-endian this means qubit 0=c1, qubit 1=c2, qubit 2=t, and the integer index is x=a1+2a2+4y. With no x given, the unitary W is built and column x is |B_x>.

## Classical postprocessing

Decoding: apply W^dagger and read the computational basis to recover x. Entanglement comparisons (concurrence, negativity, monogamy score) are offline and not implemented.

## Algorithm steps

1. Optionally load basis input |a>|y> with X gates. (eq_2)
2. Apply H to the m control qubits. (eq_2)
3. Apply the controlled-X layer: CNOT fan-out (variant A) or CCX (variant B), per f. (eq_2, eq_4, eq_5)
4. The output is |B_x>; orthonormality over all x can be checked with the Gram matrix of the columns of W. (eq_1, eq_3)

## Assumptions

- n=3, m=2 smallest instance
- only X-type controlled gates; phase-type gates not implemented
- qubit 0 is the least significant bit of the integer index

## Missing information

- The paper's two specific multiple-qubit controlled-unitary gates
- Proof that earlier algorithms are special cases
- Qudit generalization
- Entanglement and monogamy score results
