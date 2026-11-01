# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Synthesize two-qutrit ternary gates (controlled-shift CX3, SWAP3) from a Fourier gate F and the diagonal entangler CZ3 on two qutrits, as a variant of the abstract's TCX/TCZ-based synthesis; verify on the 9-dimensional subspace of a 4-level-per-qutrit qubit embedding.

Scope: Single tiny instance: two qutrits (a,b in {0,1,2}), each embedded in 2 qubits (level 3 untouched). Covers F, CZ3, CX3 = (I x F^dagger) CZ3 (I x F), and SWAP3 as three controlled-shift gates. Out of scope: Cartan decomposition of one-qutrit gates, physical implementation, Muthukrishnan-Stroud gates, Toffoli synthesis, general qudit extension, universality proof.

## Symbols

- $\omega$: primitive cube root of unity e^{2\pi i/3}; domain: complex unit
- $X$: qutrit shift gate; domain: 3x3 unitary
- $Z$: qutrit clock gate; domain: 3x3 unitary
- $F$: qutrit Fourier gate; domain: 3x3 unitary
- $a,b$: computational basis labels of qutrit 1 and 2; domain: {0,1,2}

## eq_1: Fourier gate

$$
F|j\rangle=3^{-1/2}\sum_{k=0}^{2}\omega^{jk}|k\rangle,\quad X|j\rangle=|j+1\bmod 3\rangle,\quad Z|j\rangle=\omega^{j}|j\rangle
$$

Definitions of F, X, Z

Provenance: `standard_background`. Standard Weyl-Heisenberg qutrit definitions; not stated in abstract.

Equation assumptions:

- Basis ordering |0>,|1>,|2>

## eq_2: Fourier conjugation

$$
F X F^{\dagger}=Z
$$

Fourier gate maps shift to clock; sign convention should be checked in simulation (F X F^dagger = Z^{\pm1} depending on convention)

Provenance: `standard_background`. Direct calculation with the F defined above gives F X F^dagger = Z^{-1}... to be verified numerically; the sketch's sign may need correction.

Equation assumptions:

- Implementation must verify sign and swap F with F^dagger if needed

## eq_3: Diagonal entangler

$$
CZ_3|a,b\rangle=\omega^{ab}|a,b\rangle
$$

Controlled-phase two-qutrit gate

Provenance: `assumption`. Proposed native gate related to the abstract's TCZ gate.

Equation assumptions:

- Chosen as the TCZ-like gate

## eq_4: Controlled shift from CZ3

$$
CX_3|a,b\rangle=|a,b+a\bmod 3\rangle,\quad CX_3=(I\otimes F^{\dagger})\,CZ_3\,(I\otimes F)
$$

TCX-like gate by Fourier conjugation on target

Provenance: `abstract_inferred`. Inferred that TCX and TCZ are interconvertible by one-qutrit gates. Exact F vs F^dagger ordering depends on convention and is to be checked.

Abstract evidence: we propose the ternary controlled X (TCX) gate or the ternary controlled Z (TCZ) gate as the two-qutrit elementary gate

Equation assumptions:

- Sign convention fixed by numerical check

## eq_5: Ternary SWAP

$$
SWAP_3=CX_3^{(a\to b)}\,\big(CX_3^{(b\to a)}\big)^{-1}\,CX_3^{(a\to b)},\quad |a,b\rangle\mapsto|b,a\rangle
$$

Three controlled shifts: b->b+a, a->a-b, b->b+a gives (a,b)->(a,a+b)->(-b,a+b)->(-b,a); the net result is a swap up to a sign (-b), so a final one-qutrit negation (|j>->|-j>) is needed to give an exact swap

Provenance: `assumption`. Correction to the sketch: tracing the sequence yields (-b,a), not (b,a); an extra parity/negation permutation fixes it. Alternatively use the a->a-b, b->b+a, a->a-b ordering.

Equation assumptions:

- Compose with negation gates or verify numerically

## Registers

- q1: 2 qubits qubits; qutrit 1, level j encoded as binary integer j, level 3 unused
- q2: 2 qubits qubits; qutrit 2, same encoding

## Initial state

Any state in the 9-dimensional subspace; unitary is verified on basis states |a,b>.

## Classical postprocessing

Compare the simulated unitary on the 9-dimensional subspace to target permutation or phase matrices.

## Algorithm steps

1. Embed each qutrit in 2 qubits and build F, F^dagger, X, Z as 4x4 unitaries acting as identity on level 3. (eq_1, eq_2)
2. Build CZ3 as diagonal phases omega^{ab} on the 9 states, identity elsewhere. (eq_3)
3. Compose CX3 by conjugating the target with F. (eq_4)
4. Compose three controlled shifts (with sign correction) to form SWAP3. (eq_5)

## Assumptions

- Gate set is Fourier plus diagonal entangler, differing from the abstract's TCX/Cartan route
- Level 3 of each embedding is untouched, so unitarity requires identity extension

## Missing information

- Cartan-derived one-qutrit gates
- Toffoli and Muthukrishnan-Stroud constructions
- Physical implementation details
- Qudit generalization
