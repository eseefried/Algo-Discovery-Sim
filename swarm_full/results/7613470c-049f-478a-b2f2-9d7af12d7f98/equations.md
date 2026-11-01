# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Develop a circuit decomposition of the quantum Fourier transform (QFT) for hybrid qudits (e.g., a qutrit plus qubits) using generalized Hadamard and generalized controlled-phase gates, implementable via selective rotations in NMR, and demonstrate it on an NMR quantum emulator in which four qubits emulate a qutrit coupled to two qubits.

Scope: Abstract-level reconstruction of the hybrid-qudit QFT: the standard QFT definition, the generalized Hadamard and controlled-phase gate forms as background, and a finite qutrit+2 qubit instance. The exact decomposition, pulse sequences, and experimental results are not given in the abstract.

## Symbols

- $d$: Dimension of the qudit or hybrid system level; domain: integer >= 2
- $\omega_d$: d-th root of unity e^{2\pi i/d}; domain: complex unit circle
- $F_d$: d-dimensional QFT matrix; domain: d x d unitary
- $H_d$: Generalized Hadamard gate; domain: d x d unitary
- $CP_{d,d'}$: Generalized controlled-phase gate between levels of dimension d and d'; domain: diagonal unitary

## eq_1: QFT definition

$$
F_N|j\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{2\pi i jk/N}|k\rangle
$$

Standard QFT action on a basis state, with N the total dimension (e.g., 3*2*2=12 for the hybrid instance).

Provenance: `standard_background`. Textbook definition of the QFT; the abstract names the QFT but gives no formula.

Equation assumptions:

- N equals the product of the subsystem dimensions

## eq_2: Generalized Hadamard

$$
H_d=F_d,\quad (H_d)_{kj}=\frac{1}{\sqrt{d}}\omega_d^{jk}
$$

Assumed form of the generalized Hadamard as the d-dimensional DFT matrix.

Provenance: `assumption`. The abstract mentions generalized Hadamard gates without a definition; the DFT form is the common convention.

Equation assumptions:

- Paper's generalized Hadamard matches the DFT matrix

## eq_3: Generalized controlled-phase

$$
CP_{d,d'}|j,k\rangle=e^{2\pi i jk/(dd')}|j,k\rangle
$$

Assumed diagonal phase gate coupling levels of subsystems of dimension d and d'.

Provenance: `assumption`. The abstract mentions generalized controlled-phase gates; this is the standard mixed-radix form and may differ from the paper.

Equation assumptions:

- Phase convention follows mixed-radix QFT decomposition

## Registers

- q: 1 qutrit (d=3), emulated by 2 qubits qubits; Qutrit subsystem, most significant digit; the emulator encodes its 3 levels in a 4-level two-qubit space
- a: 1 qubit qubits; First qubit coupled to the qutrit
- b: 1 qubit qubits; Second qubit coupled to the qutrit

## Initial state

Assumed: a computational basis state |j_q, j_a, j_b> (or a thermal-equilibrium-derived pseudo-pure state in NMR); the abstract does not specify the input.

## Measurement

Assumed: read out the NMR spectra (ensemble signal) of the emulating qubits after the QFT circuit, possibly via state tomography, to compare with the ideal QFT output; the abstract does not specify the protocol.

## Classical postprocessing

Assumed: compare the experimental output (spectra or reconstructed density matrix) with the ideal F_12 output, e.g., via a fidelity measure; the abstract gives no details.

## Algorithm steps

1. Apply generalized Hadamard H_3 on the qutrit (implemented via selective rotations on the emulating qubits). (eq_2)
2. Apply generalized controlled-phase gates between the qutrit and each qubit, with mixed-radix phases. (eq_3)
3. Apply Hadamard H_2 on the first qubit, then controlled-phase between the two qubits. (eq_2, eq_3)
4. Apply Hadamard H_2 on the last qubit; reverse digit order (swap) if required by the mixed-radix convention. Overall action is the QFT on dimension 12. (eq_1, eq_2)

## Assumptions

- Gate definitions are standard conventions, not confirmed from the paper.
- Generalized Hadamard is the DFT matrix; generalized controlled-phase uses mixed-radix phases.
- Gate ordering and qutrit ordering in the circuit plan are assumed from the standard mixed-radix QFT, not from the paper.
- Qutrit ordered first, followed by the two qubits; the emulator maps the qutrit onto a 4-level two-qubit space.
- Measurement and postprocessing are assumed typical NMR readout (spectra/tomography) and fidelity comparison.
- Measurement and postprocessing are assumed typical NMR readout and fidelity comparison.

## Missing information

- Exact gate decomposition ordering
- NMR pulse sequences and selective rotations
- Input states and actual measurement or tomography protocol
- Fidelity metrics and results
- Qutrit-to-qubit embedding used by the emulator
