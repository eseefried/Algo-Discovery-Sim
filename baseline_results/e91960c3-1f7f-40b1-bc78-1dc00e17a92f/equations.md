# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct the quantum Fourier transform (QFT) on a hybrid (mixed-dimension) qudit register as a circuit built from generalized Hadamard gates and generalized controlled-phase gates, as described in the abstract, for a tiny explicit instance suitable for later circuit generation.

Scope: Scoped instance (chosen because no experiment_scope was supplied): the QFT on a single hybrid system consisting of one qutrit (d_1 = 3) and one qubit (d_2 = 2), i.e. an N = 6 dimensional space, decomposed into one generalized Hadamard H_3, one generalized controlled-phase gate with angle 2\pi/6, and one Hadamard H_2, with digit-reversed output ordering. Outside scope: the paper's larger experimental instance (qutrit coupled to two qubits, N = 12), the NMR emulation of a qutrit using qubits (four qubits emulating qutrit + two qubits), the translation of gates into NMR selective rotations / pulse sequences, and any experimental fidelities or tomography results.

## Symbols

- $d_1$: Dimension of the first qudit (qutrit in the scoped instance); domain: integer, d_1 = 3 in the instance
- $d_2$: Dimension of the second qudit (qubit in the scoped instance); domain: integer, d_2 = 2 in the instance
- $N$: Total Hilbert-space dimension of the hybrid register, N = d_1 d_2; domain: integer, N = 6 in the instance
- $\omega_m$: Primitive m-th root of unity, \omega_m = e^{2\pi i/m}; domain: complex number on the unit circle, m \in \{d_1, d_2, N\}
- $x_1, y_1$: Computational-basis label of the first qudit (input digit x_1, output digit y_1); domain: \mathbb{Z}_{d_1} = \{0,1,2\}
- $x_2, y_2$: Computational-basis label of the second qudit (input digit x_2, output digit y_2); domain: \mathbb{Z}_{d_2} = \{0,1\}
- $x, y$: Integer labels of the full N-dimensional basis states (input x, output y), via mixed-radix encoding; domain: \mathbb{Z}_N = \{0,\dots,5\}
- $F_N$: Quantum Fourier transform unitary on the N-dimensional hybrid register; domain: N \times N unitary matrix
- $H_d$: Generalized Hadamard (discrete Fourier transform) gate on a single qudit of dimension d; domain: d \times d unitary matrix
- $CP(\theta)$: Generalized controlled-phase gate between two qudits, applying phase e^{i\theta j k} to |j\rangle|k\rangle; domain: d_1 d_2 \times d_1 d_2 diagonal unitary, \theta \in [0, 2\pi)

## eq_1: QFT on an N-dimensional register

$$
F_N |x\rangle = \frac{1}{\sqrt{N}} \sum_{y=0}^{N-1} \omega_N^{x y} |y\rangle, \qquad \omega_N = e^{2\pi i / N}
$$

Definition of the quantum Fourier transform acting on computational basis state |x> of the full hybrid register of dimension N; exact equality.

Provenance: `standard_background`. Standard definition of the QFT on a d-dimensional (here N-dimensional) Hilbert space; the abstract names the QFT but does not write this relation.

Equation assumptions:

- The hybrid-qudit QFT is the standard DFT unitary on the N = d_1 d_2 dimensional joint space.

## eq_2: Mixed-radix encoding of input and output labels

$$
x = x_1 d_2 + x_2, \quad y = y_1 + d_1 y_2, \qquad x_1, y_1 \in \mathbb{Z}_{d_1},\; x_2, y_2 \in \mathbb{Z}_{d_2}
$$

Integer encoding: the input integer x has most-significant digit x_1 (qudit 1) and least-significant digit x_2 (qudit 2); the output integer y is read with digit roles reversed (qudit 1 holds the least-significant digit y_1). This digit reversal is the mixed-radix analogue of the bit reversal of the qubit QFT.

Provenance: `assumption`. A specific register ordering and encoding must be fixed for the product decomposition in eq_5 to hold; this choice makes the circuit need no explicit swap, at the price of reversed output digit order.

Equation assumptions:

- Register order: first tensor factor is the qutrit (d_1 = 3), second is the qubit (d_2 = 2).
- Output digits are read in reversed order (no final swap included).

## eq_3: Generalized Hadamard gate on a d-level qudit

$$
H_d |j\rangle = \frac{1}{\sqrt{d}} \sum_{k=0}^{d-1} \omega_d^{j k} |k\rangle, \qquad \omega_d = e^{2\pi i/d}
$$

Single-qudit discrete Fourier transform (Chrestenson/generalized Hadamard) gate; for d = 2 it is the usual Hadamard, for d = 3 it is the 3x3 matrix with entries \omega_3^{jk}/\sqrt{3}.

Provenance: `abstract_inferred`. The abstract states the decomposition uses generalized Hadamard gates; the standard meaning of this term for qudits is the single-qudit DFT matrix. Phase/convention details of the paper are not available.

Abstract evidence: generalized Hadamard

Equation assumptions:

- The paper's generalized Hadamard coincides with the single-qudit DFT matrix up to possible global phase or sign convention of the exponent.

## eq_4: Generalized controlled-phase gate

$$
CP(\theta)\, |j\rangle_1 |k\rangle_2 = e^{i \theta\, j k}\, |j\rangle_1 |k\rangle_2, \qquad j \in \mathbb{Z}_{d_1},\; k \in \mathbb{Z}_{d_2}
$$

Two-qudit diagonal gate applying a phase proportional to the product of the two basis labels; symmetric in control and target. In the scoped instance \theta = 2\pi/N = 2\pi/6.

Provenance: `abstract_inferred`. The abstract states the decomposition uses generalized controlled-phase gates; the natural qudit generalization of the controlled-phase is the diagonal gate with phase exponent proportional to the product of the labels, which is exactly what the mixed-radix factorization (eq_5) requires.

Abstract evidence: generalized controlled-phase gates

Equation assumptions:

- The paper's generalized controlled-phase gate is diagonal with phase e^{i\theta j k}; alternative conventions (e.g. phases only on specific control levels) would change the decomposition.

## eq_5: Mixed-radix product decomposition of the hybrid QFT

$$
F_N |x_1\rangle_1 |x_2\rangle_2 = \Big( \frac{1}{\sqrt{d_1}} \sum_{y_1=0}^{d_1-1} \omega_{d_1}^{x_1 y_1}\, \omega_N^{x_2 y_1} |y_1\rangle_1 \Big) \otimes \Big( \frac{1}{\sqrt{d_2}} \sum_{y_2=0}^{d_2-1} \omega_{d_2}^{x_2 y_2} |y_2\rangle_2 \Big)
$$

Exact factorization of eq_1 using eq_2: since x y / N = x_1 y_1 / d_1 + x_1 y_2 + x_2 y_1 / N + x_2 y_2 / d_2 and the integer term x_1 y_2 contributes no phase, the QFT output is a product state over the two qudits with output digits in reversed order.

Provenance: `standard_background`. Direct algebraic consequence of eq_1 and eq_2 (mixed-radix Cooley–Tukey factorization of the DFT); this is the mathematical content that the abstract's circuit decomposition realizes.

Equation assumptions:

- Encoding and register ordering of eq_2.

## eq_6: Gate-level circuit for the scoped instance (qutrit ⊗ qubit, N = 6)

$$
F_6 \;=\; \big( I_3 \otimes H_2 \big)\; CP\!\left(\tfrac{2\pi}{6}\right)\; \big( H_3 \otimes I_2 \big) \quad \text{(up to the output digit reversal of eq_2)}
$$

Circuit implementing eq_5 for d_1 = 3, d_2 = 2: H_3 on the qutrit creates the \omega_3^{x_1 y_1} amplitudes, the controlled-phase with angle 2\pi/6 (qubit label x_2 times qutrit label y_1) supplies the cross phase \omega_6^{x_2 y_1}, and H_2 on the qubit supplies \omega_2^{x_2 y_2}. Operators act right-to-left. Equality to F_6 holds exactly after relabelling the output as y = y_1 + 3 y_2.

Provenance: `assumption`. Proposed smallest hybrid instance of the abstract's generalized-Hadamard plus generalized-controlled-phase decomposition; obtained by matching eq_3 and eq_4 to the factors in eq_5. The paper's actual instance (qutrit + two qubits) and its exact gate ordering are not available.

Equation assumptions:

- Instance choice d_1 = 3, d_2 = 2 (N = 6) rather than the paper's qutrit + two qubits (N = 12).
- Gate conventions of eq_3 and eq_4.
- No final swap/digit-reordering gate included.

## Registers

- q1 (qutrit): 1 qutrit (d_1 = 3) qubits; Holds the most-significant input digit x_1 and, after the circuit, the least-significant output digit y_1
- q2 (qubit): 1 qubit (d_2 = 2) qubits; Holds the least-significant input digit x_2 and, after the circuit, the most-significant output digit y_2; acts as control (label x_2) of the controlled-phase gate

## Initial state

Computational basis state |x_1\rangle_1 |x_2\rangle_2 with x = 3 x_1 + x_2 \in \{0,\dots,5\} (eq_2); e.g. the explicit test input |1\rangle_1 |1\rangle_2 corresponding to x = 4. Preparation of this state from the NMR thermal/pseudo-pure state is outside scope.

## Measurement

Not specified by the abstract. For verification of the scoped instance, an assumed option is to measure both qudits in the computational basis (or perform state tomography on the N = 6 space) for a set of input basis states and compare with the ideal F_6 action of eq_1; the NMR readout actually used by the paper is unknown.

## Classical postprocessing

Only the digit-reversal relabelling y = y_1 + 3 y_2 (eq_2) and, for verification, comparison of measured output distributions / reconstructed states with the ideal F_6 amplitudes; no paper-specific postprocessing is known from the abstract.

## Algorithm steps

1. Prepare the hybrid register in the mixed-radix encoded basis state |x_1>|x_2> (or an arbitrary input superposition) with the ordering of eq_2. (eq_2)
2. Apply the generalized Hadamard H_3 to the qutrit, producing (1/\sqrt{3}) \sum_{y_1} \omega_3^{x_1 y_1} |y_1>|x_2>. (eq_3, eq_6)
3. Apply the generalized controlled-phase CP(2\pi/6) between qubit (label x_2) and qutrit (label y_1), multiplying each branch by \omega_6^{x_2 y_1}. (eq_4, eq_6)
4. Apply the Hadamard H_2 to the qubit, producing (1/\sqrt{2}) \sum_{y_2} \omega_2^{x_2 y_2} |y_2>; the joint state now equals F_6|x> with output digits reversed (eq_5). (eq_3, eq_5, eq_6)
5. Interpret the output: read qutrit label as y_1 and qubit label as y_2 and form y = y_1 + 3 y_2 (classical relabelling; alternatively insert a hybrid swap, not included here). (eq_2, eq_5)

## Assumptions

- No experiment_scope was supplied, so the smallest hybrid instance (one qutrit + one qubit, N = 6) was chosen instead of the paper's qutrit + two qubits (N = 12) system.
- Hybrid QFT is taken to be the standard DFT unitary on the joint N-dimensional space (eq_1).
- Register ordering (qutrit first, qubit second), mixed-radix input encoding x = 3 x_1 + x_2, and digit-reversed output y = y_1 + 3 y_2 (eq_2).
- Generalized Hadamard = single-qudit DFT matrix; generalized controlled-phase = diagonal gate with phase e^{i\theta j k} (eq_3, eq_4); the paper's exact conventions may differ by phases or exponent signs.
- No final swap gate is included; the output digit reversal is handled classically.
- Measurement description is a verification choice, not taken from the abstract.

## Missing information

- The paper's explicit circuit for the qutrit + two qubits (N = 12) QFT, including gate ordering, controlled-phase angles (expected 2\pi/6 and 2\pi/12 type angles) and any swap/reordering gates.
- The exact definitions and conventions of the paper's generalized Hadamard and generalized controlled-phase gates.
- How these gates are decomposed into NMR selective rotations (pulse sequences, J-coupling evolution, phases, durations).
- The encoding used by the four-qubit NMR emulator to represent a single qutrit within two qubits (which qubit subspace levels represent the qutrit states and how the unused level is handled).
- Initial-state preparation (pseudo-pure state) and readout/tomography protocol on the NMR system.
- Any experimental fidelities or numerical results.
