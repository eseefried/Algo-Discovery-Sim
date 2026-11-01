# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Synthesize the two-qutrit controlled-shift CX3 and the ternary SWAP from a qutrit Fourier gate F and a diagonal controlled-phase entangler CZ3. This is a Weyl-Heisenberg variant of the abstract's TCX/TCZ-based synthesis. The target is a 16-dimensional unitary, with each qutrit embedded in 2 qubits, to be checked on the 9-dimensional computational subspace.

Scope: One tiny instance: two qutrits a,b in {0,1,2}, each embedded in 2 qubits with level 3 left as identity. The circuit must build F, F^dagger and CZ3 explicitly, then obtain CX3 by Fourier conjugation of CZ3 and SWAP3 from three conjugated CZ3-based shifts plus a negation N=F^2. Outside this scope: the Cartan-derived one-qutrit gates, the physical implementation, Toffoli and Muthukrishnan-Stroud synthesis, the qudit generalization, and any universality proof. The native predictions (U=exp(-i sum theta_k G_k), H_k, etc.) are not used. Their generator forms are not confirmed by the abstract and they do not define a build.

## Symbols

- $\omega$: primitive cube root of unity e^{2\pi i/3}; domain: complex unit
- $X,Z$: qutrit shift and clock gates; domain: 3x3 unitaries
- $F$: qutrit Fourier gate; domain: 3x3 unitary
- $N$: negation permutation |j> -> |-j mod 3>, equal to F^2; domain: 3x3 permutation unitary
- $a,b$: computational levels of qutrit 1 and qutrit 2; domain: {0,1,2}
- $E$: embedding of qutrit levels into qubit basis states: 0->00, 1->01, 2->10, with level 3 (11) acted on trivially; domain: 4-dimensional space containing a 3-dimensional subspace

## eq_1: Weyl-Heisenberg definitions and Fourier conjugation

$$
X|j\rangle=|j+1\bmod 3\rangle,\; Z|j\rangle=\omega^{j}|j\rangle,\; F|j\rangle=3^{-1/2}\sum_{k=0}^{2}\omega^{jk}|k\rangle,\; ZF=FX \Rightarrow FXF^{\dagger}=Z,\; F^{2}=N
$$

Standard qutrit gates. The sign convention is exact: ZF|j>=F|j+1>, so F X F^dagger = Z (not Z^-1). Also F^2|j>=|-j>.

Provenance: `standard_background`. Direct calculation from the definition of F.

Equation assumptions:

- Basis order |0>,|1>,|2>

## eq_2: Diagonal entangler

$$
CZ_3|a,b\rangle=\omega^{ab}|a,b\rangle
$$

Two-qutrit controlled-phase gate acting as a TCZ-like entangler. Its phase is 1 whenever a=0 or b=0, so only (1,1),(1,2),(2,1),(2,2) get nontrivial phases.

Provenance: `assumption`. Chosen as the concrete TCZ-like gate. The abstract names TCZ but does not give its matrix.

Equation assumptions:

- The TCZ of the paper is taken to be this standard generalized controlled-Z

## eq_3: Controlled shift from CZ3 by Fourier conjugation

$$
CX_3|a,b\rangle=|a,\,b+a\bmod 3\rangle,\quad CX_3=(I\otimes F^{\dagger})\,CZ_3\,(I\otimes F),\quad CX_3^{-1}=(I\otimes F^{\dagger})\,CZ_3^{\dagger}\,(I\otimes F)
$$

Verified by direct calculation: F|b> -> sum_k omega^{(a+b)k}|k> = sqrt(3)F|a+b>, and F^dagger returns |a+b>. The inverse uses CZ3^dagger (phase omega^{-ab}). The reverse-direction gate CX3^{(b->a)} is the same expression with the roles of the qutrits exchanged, since CZ3 is symmetric.

Provenance: `abstract_inferred`. The abstract says TCX or TCZ is the elementary gate, which suggests the two are interchangeable by one-qutrit gates. The exact conjugation here is derived from background.

Abstract evidence: we propose the ternary controlled X (TCX) gate or the ternary controlled Z (TCZ) gate as the two-qutrit elementary gate

Equation assumptions:

- F is the one-qutrit gate used for the conjugation

## eq_4: Ternary SWAP from three controlled shifts plus negation

$$
(a,b)\xrightarrow{CX_3^{(a\to b)}}(a,a+b)\xrightarrow{(CX_3^{(b\to a)})^{-1}}(-b,a+b)\xrightarrow{CX_3^{(a\to b)}}(-b,a)\xrightarrow{N\otimes I}(b,a),\quad SWAP_3=(N\otimes I)\,CX_3^{(a\to b)}\,(CX_3^{(b\to a)})^{-1}\,CX_3^{(a\to b)}
$$

Correction to the sketch: the three shifts alone give (a,b)->(-b,a), not (b,a). A final negation N=F^2 on qutrit 1 gives the exact swap. N exchanges levels 1 and 2 and fixes 0 and 3, so it is a qubit SWAP of the two qubits of qutrit 1 under the embedding. In circuit order the first factor applied is the rightmost.

Provenance: `assumption`. Traced by hand: the third step adds control -b to target a+b, giving a. The sketch omitted the sign fix.

Equation assumptions:

- Operator product reads right to left in time order

## eq_5: Qubit embedding and register convention

$$
E(j)=j_0+2j_1\text{ for qubits }(j_0,j_1),\; j\in\{0,1,2\},\; \text{global index}=a+4b,\; G_{16}=G_{9}\oplus I_{\text{unused}}
$$

Each qutrit gate is a 4x4 unitary equal to the 3x3 gate on levels 0..2 and the identity on level 3. Two-qutrit gates are 16x16 unitaries equal to the 9x9 gate on |a,b>, a,b<=2, and the identity on every basis state with a=3 or b=3. Qubits 0,1 hold qutrit a (qubit 0 is the LSB) and qubits 2,3 hold qutrit b.

Provenance: `assumption`. Needed so the unitary is exactly defined on 4 qubits and unitary-safe on unused levels.

Equation assumptions:

- Level 3 is never populated by inputs, but must still be acted on by the identity to keep the circuit unitary

## Registers

- qa: 2 qubits qubits; qutrit a; level j encoded as binary j (qubit 0 is LSB); level 3 unused
- qb: 2 qubits qubits; qutrit b; same encoding

## Initial state

Any state in the 9-dimensional span of |a,b> with a,b in {0,1,2}. Verification uses each basis state |a,b>, i.e. global index a+4b.

## Classical postprocessing

No measurement. Compare the built unitary with the target permutation and phase matrices on the 9-dimensional subspace, and check the identity on the unused levels.

## Algorithm steps

1. Build the 4x4 embedded gates F, F^dagger and N=F^2 (the identity on level 3), and tensor them with identity on the other qutrit. (eq_1, eq_5)
2. Build CZ3 and CZ3^dagger as 16x16 diagonal gates with phases omega^{ab} and omega^{-ab} on a,b in {1,2}, and 1 elsewhere. (eq_2, eq_5)
3. Build CX3 and its inverse for both control/target orientations as (I x F^dagger) CZ3^(±1) (I x F) on the target qutrit. Do not use direct mcx permutations. If a compiled unitary-matrix gate is used, state that. (eq_3)
4. Compose SWAP3 from CX3(a->b), CX3(b->a)^-1, CX3(a->b), then N on qutrit a. (eq_4)
5. Check the simulated 16x16 unitaries against the target matrices. CX3 is the permutation |a,b>->|a,a+b>, SWAP3 is |a,b>->|b,a> on the 9-dimensional subspace, and both are the identity on every state with a=3 or b=3. Check F X F^dagger = Z. For the sketch's full 16-dimensional output, no additional claims are made. (eq_1, eq_3, eq_4)

## Assumptions

- The gate set is F plus diagonal CZ3, which is a Weyl-Heisenberg variant and not the abstract's TCX plus Cartan one-qutrit route
- Level 3 of each qutrit embedding is acted on by the identity
- The circuit is a functional simulation of explicit gates and says nothing about black-box queries or hidden parameters

## Missing information

- Cartan-derived one-qutrit elementary gates
- Toffoli and Muthukrishnan-Stroud constructions
- Physical implementation details
- Qudit generalization
- Universality proof
