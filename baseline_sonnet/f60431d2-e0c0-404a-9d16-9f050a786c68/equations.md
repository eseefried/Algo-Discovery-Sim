# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Specify the two-qutrit ternary controlled-X (TCX) and controlled-Z (TCZ) gates as elementary entangling gates, and relate them to one another, as a minimal basis for ternary quantum circuit synthesis.

Scope: Only the standard definitions of the qutrit X and Z gates, a controlled-X gate (TCX) and a controlled-Z gate (TCZ) with a tiny two-qutrit instance, and the Fourier-conjugation relation between TCX and TCZ. Outside scope: the Cartan decomposition of one-qutrit gates, the universality proof, physical implementations, SWAP/Toffoli/Muthukrishnan-Stroud synthesis, and the general qudit extension.

## Symbols

- $|j\rangle$: qutrit computational basis state; domain: j in {0,1,2}
- $X$: ternary shift gate; domain: 3x3 unitary
- $Z$: ternary clock (phase) gate; domain: 3x3 unitary
- $\omega$: primitive cube root of unity; domain: e^{2\pi i/3}
- $F$: qutrit Fourier (generalized Hadamard) gate; domain: 3x3 unitary
- $\mathrm{TCX}$: ternary controlled-X gate; control first, target second (assumed convention); domain: 9x9 unitary
- $\mathrm{TCZ}$: ternary controlled-Z gate; domain: 9x9 unitary

## eq_1: Qutrit X and Z

$$
X|j\rangle=|j+1 \bmod 3\rangle,\quad Z|j\rangle=\omega^{j}|j\rangle
$$

Generalized Pauli shift and clock gates for qutrits.

Provenance: `standard_background`. Standard qutrit Weyl-Heisenberg operators; the abstract does not give explicit definitions.

Equation assumptions:

- The paper's X and Z may differ in convention.

## eq_2: TCX definition

$$
\mathrm{TCX}|c\rangle|t\rangle=|c\rangle|t+c \bmod 3\rangle
$$

Controlled shift: target is shifted by the control value, i.e. X^c is applied to the target.

Provenance: `assumption`. A common qutrit generalization of CNOT; the paper's exact TCX definition (e.g. control on a single level) is not stated in the abstract.

Equation assumptions:

- Control value c applies X^c to the target
- Control is the first register

## eq_3: TCZ definition

$$
\mathrm{TCZ}|c\rangle|t\rangle=\omega^{ct}|c\rangle|t\rangle
$$

Controlled phase gate applying Z^c on the target.

Provenance: `assumption`. Natural counterpart of TCX; the paper's exact definition is not given in the abstract.

Equation assumptions:

- Z^c is applied to the target

## eq_4: TCX-TCZ relation

$$
\mathrm{TCX}=(I\otimes F)\,\mathrm{TCZ}'\,(I\otimes F^{\dagger}),\quad F|j\rangle=\tfrac{1}{\sqrt3}\sum_{k=0}^{2}\omega^{jk}|k\rangle
$$

TCX is equal to TCZ conjugated by Fourier gates on the target, up to the sign or ordering convention of F, which fixes whether TCZ' is TCZ or its inverse.

Provenance: `standard_background`. Standard fact that F maps X to Z (or Z^-1) by conjugation. The abstract only says TCX or TCZ can serve as the elementary gate, which suggests this equivalence but does not state it.

Equation assumptions:

- F convention chosen so F X F^dagger is Z or Z^-1
- TCZ' denotes TCZ or its inverse depending on convention

## Registers

- control: 1 qutrit (dimension 3) qubits; control; basis |0>,|1>,|2>
- target: 1 qutrit (dimension 3) qubits; target; basis |0>,|1>,|2>

## Initial state

Illustrative instance (assumed): |c,t> = |1>|2>, giving TCX -> |1>|0> and TCZ -> omega^2 |1>|2>.

## Algorithm steps

1. Prepare the two-qutrit basis state |c>|t>, with the control register ordered first. (eq_1)
2. Apply TCX as the assumed controlled shift. (eq_2)
3. Alternatively apply TCZ, or realize TCX from TCZ via Fourier conjugation on the target. (eq_3, eq_4)

## Assumptions

- Gate definitions follow common qutrit conventions, not necessarily the paper's.
- No Cartan decomposition or universality equations are reconstructed.

## Missing information

- Paper's exact definitions of TCX and TCZ
- Cartan decomposition of the one-qutrit elementary gates
- Universality proof and synthesis constructions for SWAP, Toffoli and Muthukrishnan-Stroud gates
- Physical implementation details
- General qudit extension
