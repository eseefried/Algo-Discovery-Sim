# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Construct the quantum Fourier transform on a hybrid qudit register (mixed dimensions) via a decomposition into generalized Hadamard and generalized controlled-phase gates. The abstract mentions an NMR emulation of one qutrit plus two qubits but gives no explicit equations.

Scope: Smallest useful instance: hybrid register of one qutrit (d=3) and two qubits (d=2), total dimension 12, with standard QFT definition and a standard mixed-radix Hadamard/controlled-phase decomposition. Out of scope: the paper's specific gate decomposition, the NMR selective-rotation pulse sequences, the four-qubit qutrit emulation encoding, and experimental results and fidelities.

## Symbols

- $d_j$: local dimension of qudit j; domain: integer >= 2; instance d_0=3, d_1=d_2=2
- $N$: total Hilbert space dimension, product of d_j; domain: integer; N=12 in the instance
- $\omega_N$: primitive N-th root of unity exp(2 pi i/N); domain: complex unit circle
- $x,y$: computational basis integers; domain: 0..N-1
- $H_d$: generalized Hadamard (d-dimensional DFT) gate; domain: unitary on C^d
- $CP$: generalized controlled-phase gate between qudits with dimensions d_a and d_b; domain: diagonal unitary on C^{d_a} tensor C^{d_b}

## eq_1: QFT definition

$$
F_N|x\rangle=\frac{1}{\sqrt N}\sum_{y=0}^{N-1}\omega_N^{xy}|y\rangle
$$

QFT on the full hybrid register of dimension N, where the register basis is identified with integers 0..N-1.

Provenance: `standard_background`. Standard QFT definition; the abstract names the QFT but states no equation.

Equation assumptions:

- N=3*2*2=12 for the instance

## eq_2: Generalized Hadamard

$$
H_d|k\rangle=\frac{1}{\sqrt d}\sum_{l=0}^{d-1}e^{2\pi i kl/d}|l\rangle
$$

Single-qudit DFT used as the generalized Hadamard; d=3 for the qutrit, d=2 gives the ordinary Hadamard.

Provenance: `standard_background`. Common definition of generalized Hadamard; the paper's exact convention is not given in the abstract.

Equation assumptions:

- Sign and normalization convention may differ from the paper

## eq_3: Mixed-radix encoding

$$
x=x_0\,d_1 d_2+x_1\,d_2+x_2,\quad x_j\in\{0,\dots,d_j-1\}
$$

Register ordering: qutrit most significant, then the two qubits.

Provenance: `assumption`. Needed to make the QFT well defined on the hybrid register; ordering is a proposed choice.

Equation assumptions:

- Qutrit is first (most significant) register
- d_0=3,d_1=d_2=2

## eq_4: Generalized controlled-phase

$$
CP_{ab}^{(m)}|k_a,k_b\rangle=\exp\!\left(\frac{2\pi i\,k_a k_b}{m}\right)|k_a,k_b\rangle
$$

Diagonal two-qudit phase gate, with m the product of the relevant dimensions for the mixed-radix phase 2 pi k_a k_b / m (e.g. m dividing the cumulative radix).

Provenance: `assumption`. Generic form of generalized controlled-phase; the actual phase schedule of the paper is not specified in the abstract.

Equation assumptions:

- Phase denominators m must be derived from the mixed-radix factorization of eq_1; not derived here

## eq_5: Decomposition form

$$
F_N=\mathrm{SWAP/reorder}\cdot\prod_{j}\Big(H_{d_j}^{(j)}\prod_{k>j}CP_{jk}\Big)
$$

Schematic structure of a QFT decomposed into Hadamards and controlled-phases, followed by a digit-reordering permutation.

Provenance: `abstract_inferred`. The abstract states the decomposition uses these gate types; the detailed ordering and phases are the usual qubit-QFT analogue and are not given.

Abstract evidence: a circuit decomposition of the QFT for hybrid qudits based on generalized Hadamard and generalized controlled-phase gates

Equation assumptions:

- Exact gate ordering and phases not verified; digit-reversal permutation may be needed

## Registers

- q0: 1 qutrit (dimension 3) qubits; most significant digit
- q1: 1 qubit qubits; middle digit
- q2: 1 qubit qubits; least significant digit

## Initial state

Arbitrary computational basis state |x_0,x_1,x_2> (e.g. |0,0,0> or a chosen test state); not specified in the abstract.

## Algorithm steps

1. Encode input integer x in mixed-radix digits across the qutrit and two qubits. (eq_3)
2. Apply generalized Hadamard on the qutrit, then controlled-phase gates between qutrit and each qubit. (eq_2, eq_4)
3. Apply Hadamard on the first qubit and a controlled-phase with the second qubit, then Hadamard on the last qubit. (eq_2, eq_4)
4. Apply the digit reordering to match the QFT output convention; compare with the target transform. (eq_1, eq_5)

## Assumptions

- Chose the qutrit plus two qubits instance to match the abstract's emulated system.
- Standard QFT and DFT conventions used as background.
- Mixed-radix phase factors are not derived or verified here.

## Missing information

- Exact gate decomposition, phase angles, and gate ordering of the paper
- Handling of the mixed-dimension reordering
- NMR selective-rotation implementations
- Mapping of the qutrit onto two-qubit emulation levels
- Measurement, tomography and fidelity results
