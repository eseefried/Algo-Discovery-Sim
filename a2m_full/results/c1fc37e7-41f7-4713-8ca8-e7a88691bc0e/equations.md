# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

QFT over Z_12 on a hybrid register of one qutrit (d1=3) and two qubits (d2=d3=2), built from generalized Hadamards (F_d) and generalized controlled-phase gates. The qutrit is encoded in 2 qubits, so 4 physical qubits are used. The circuit has no oracle and no measurement in the unitary/statevector check.

Scope: One instance: N=12=3*2*2 with the qutrit as the most significant input digit. The deliverable is the exact circuit unitary on the 12-dimensional valid subspace of the 16-dimensional space. The output is labelled in digit-reversed order (qutrit register holds the least significant output digit). Outside this scope: the paper's NMR selective-rotation pulse sequences, the experiment and its fidelities, general mixed dimensions, and a physical qutrit.

## Symbols

- $N=d_1d_2d_3$: Total dimension, 3*2*2=12; domain: integer 12
- $x=4x_1+2x_2+x_3$: Input integer; digits x_1 in Z_3 (qutrit), x_2,x_3 in Z_2; domain: 0..11
- $y=y_1+3y_2+6y_3$: Output integer; y_1 in Z_3 on the qutrit register, y_2,y_3 in Z_2 on the qubits; domain: 0..11
- $\omega_3$: Primitive cube root of unity exp(2 pi i/3); domain: complex
- $F_3$: Generalized Hadamard (3-point DFT), entries omega_3^{ab}/sqrt(3); domain: 3x3 unitary
- $l$: Qutrit level, encoded on qubits (q_0,q_1) as l=q_0+2q_1; level 3 (q_0=q_1=1) is unused; domain: 0..2 (3 unused)

## eq_1: Target transform

$$
U_{\mathrm{QFT}}|x\rangle=\frac{1}{\sqrt{12}}\sum_{y=0}^{11}e^{2\pi i xy/12}|y\rangle
$$

Z_12 QFT that the hybrid circuit must realize on the valid subspace, with y read as y_1+3y_2+6y_3 from the registers (qutrit, qubit 2, qubit 3).

Provenance: `standard_background`. The abstract names the QFT for hybrid qudits; the Z_N DFT is its standard definition.

Equation assumptions:

- N=12 with dimensions (3,2,2)

## eq_2: Mixed-radix phase factorization

$$
\frac{xy}{12}\equiv\frac{x_1y_1}{3}+\frac{x_2y_1}{6}+\frac{x_3y_1}{12}+\frac{x_2y_2}{2}+\frac{x_3y_2}{4}+\frac{x_3y_3}{2}\pmod 1
$$

With x=4x_1+2x_2+x_3 and y=y_1+3y_2+6y_3, the DFT phase splits into one Hadamard-type term per digit plus controlled-phase terms between a processed digit and later digits.

Provenance: `assumption`. Direct expansion of x*y/12, dropping integer parts. It gives the decomposition Hadamard then controlled phases, as in the qubit QFT. Qutrit-first ordering forces the output digit order (y_1,y_2,y_3).

Equation assumptions:

- Qutrit is the most significant input digit

## eq_3: Generalized Hadamard

$$
F_3=\frac1{\sqrt3}\begin{pmatrix}1&1&1\\1&\omega_3&\omega_3^2\\1&\omega_3^2&\omega_3\end{pmatrix}\oplus\,[1]_{|11\rangle},\quad H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
$$

Gate on the qutrit encoding qubits (levels 0,1,2 as 00,01,10 with identity on the unused level 3) and the qubit Hadamard. F_3 is compiled from two-level Givens rotations on levels 0-1 and 1-2 plus phases.

Provenance: `abstract_inferred`. The generalized Hadamard of dimension d is the d-point DFT matrix. The Givens-rotation compilation is a construction choice, not specified in the abstract.

Abstract evidence: based on generalized Hadamard and generalized controlled-phase gates, which can be implemented using selective rotations in NMR

Equation assumptions:

- Compilation into standard Qiskit rotations and multi-controlled gates is left to the circuit builder; any exact decomposition of F_3 is acceptable

## eq_4: Qutrit-to-qubit controlled phases

$$
C_{1k}=\sum_{l,b}e^{2\pi i\, l b/(3\cdot 2^{k-1}\cdot\,2)}|l\rangle\langle l|\otimes|b\rangle\langle b|,\ k=2,3\ (\text{angles }2\pi lb/6,\ 2\pi lb/12)
$$

Phase exp(2 pi i y_1 x_k/(3*2^{k-1})) with y_1 the qutrit level and x_k the qubit value. Since l=q_0+2q_1, this equals CP(2 pi/6 or 2 pi/12) from q_0 plus CP(2 times that angle) from q_1 onto the target qubit; the action on the unused level 3 is irrelevant.

Provenance: `assumption`. Follows from eq_2 and linearity in l. It is a proposed implementation of the generalized controlled-phase gate and is simpler than the multi-controlled-phase form in the sketch.

Equation assumptions:

- Only the valid subspace is checked

## eq_5: Qubit-qubit controlled phase

$$
CP(\pi/2)=\mathrm{diag}(1,1,1,i)\ \text{between qubit 2 and qubit 3}
$$

Implements the phase exp(2 pi i y_2 x_3/4).

Provenance: `standard_background`. Standard qubit-QFT controlled phase, with the angle from eq_2.

## Registers

- qutrit: 2 qubits (q0,q1), level l=q0+2*q1, levels 0..2 used qubits; Holds x_1 at input and y_1 at output
- qubit2: 1 qubit (q2) qubits; Holds x_2 at input and y_2 at output
- qubit3: 1 qubit (q3) qubits; Holds x_3 at input and y_3 at output

## Initial state

Computational basis state with qutrit level x_1, qubit2 = x_2, qubit3 = x_3. The Qiskit statevector index is x_1+4*x_2+8*x_3. This index differs from x=4x_1+2x_2+x_3, so convert digits explicitly.

## Measurement

None for the unitary/statevector check. For a counts variant, measure all 4 qubits and decode y_1=q0+2*q1, y_2=q2, y_3=q3 (Qiskit bit 0 is rightmost in the key), then y=y_1+3y_2+6y_3.

## Classical postprocessing

Compare the statevector amplitude at output digits (y_1,y_2,y_3) with exp(2 pi i x y/12)/sqrt(12) for y=y_1+3y_2+6y_3, and check zero weight on the unused level 11 of the qutrit. For a periodic input, peaks appear at multiples of 12/period.

## Algorithm steps

1. Apply F_3 on the qutrit register (q0,q1), identity on level 3. (eq_3)
2. Apply the controlled phases from the qutrit to qubit2 (angle 2pi/6 per level) and to qubit3 (angle 2pi/12 per level), each as CP gates from q0 and q1 (q1 with twice the angle). (eq_4)
3. Apply H on qubit2, then CP(pi/2) between qubit2 and qubit3. (eq_3, eq_5)
4. Apply H on qubit3. No final swap is applied, because the output is already in (y_1,y_2,y_3) order. (eq_3)

## Assumptions

- Qutrit encoded as 00,01,10 with 11 unused
- Qutrit is the most significant input digit
- The runner checks the valid 12-dimensional subspace
- Output digit order is reversed relative to input significance
- Selective rotations are compiled into standard Qiskit gates

## Missing information

- The paper's exact selective-rotation decomposition of F_3 and the controlled-phase gates
- The runner's expected output-ordering convention
- Whether a final permutation to standard output order y=4a+2b+c is required
