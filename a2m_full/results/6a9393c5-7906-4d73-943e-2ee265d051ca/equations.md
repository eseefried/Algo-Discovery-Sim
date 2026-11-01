# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Emulate the universal gate set of the Bose-Hubbard quantum-walk scheme (dual-rail walker position qubits; Rx, Rz, CP, SWAP, local Z-basis measurement) as an ordinary n-qubit circuit, with a Steane-code encoding example. Lattice dynamics are not simulated.

Scope: Gate-level emulation on n logical qubits, one qubit each, no ancillas for the universal gate set. Smallest instance: 2 qubits with Rx and Rz on each and one CP(phi), then Z-basis measurement. The Steane [[7,1,3]] encoder is a secondary extension (7 qubits, no syndrome ancillas). Outside scope: the actual Bose-Hubbard Hamiltonian on a piecewise-constant graph, the 3D lattice extension, the optical-lattice implementation, the linear vertex-count proof, and error-correction beyond encoding.

## Symbols

- $\theta$: rotation angle for Rx or Rz; domain: real
- $\phi$: controlled-phase angle, equal to Ut/\hbar; domain: real, mod 2\pi
- $U$: Hubbard on-site interaction strength; domain: real
- $t$: interaction time; domain: real, nonnegative
- $n$: number of encoded logical qubits; domain: positive integer
- $|0\rangle,|1\rangle$: walker on left or right site of a two-vertex pair; domain: computational basis of one qubit

## eq_1: Rz from on-site offset

$$
R_z(\theta)=e^{-i\theta Z/2}=\mathrm{diag}(e^{-i\theta/2},e^{i\theta/2})
$$

Energy offset between the two sites of a pair gives a Z rotation.

Provenance: `abstract_inferred`. The abstract claims arbitrary Z rotations; the explicit form is the standard rotation with an idealized Hamiltonian.

Abstract evidence: Arbitrary X and Z rotations are constructed

Equation assumptions:

- Exact evolution under H=(\theta/2t)Z
- Dual-rail encoding

## eq_2: Rx from tunneling

$$
R_x(\theta)=e^{-i\theta X/2}=\begin{pmatrix}\cos\frac{\theta}{2}&-i\sin\frac{\theta}{2}\\-i\sin\frac{\theta}{2}&\cos\frac{\theta}{2}\end{pmatrix}
$$

Tunneling between the two sites for a time t gives an X rotation.

Provenance: `abstract_inferred`. Tunneling Hamiltonian -J X on the pair gives \theta=2Jt; the abstract claims arbitrary X rotations.

Abstract evidence: Arbitrary X and Z rotations are constructed

Equation assumptions:

- Single walker, no loss
- Idealized exact tunneling

## eq_3: Controlled phase from Hubbard interaction

$$
CP(\phi)=\mathrm{diag}(1,1,1,e^{i\phi}),\quad \phi=-Ut/\hbar
$$

The on-site interaction phase appears only when both walkers occupy interacting sites, i.e. on |11>. The sign is convention, and phi is tunable.

Provenance: `abstract_inferred`. A cphase gate is claimed; the mapping to U t follows from the sketch's assumption that the interaction acts only on |11>.

Abstract evidence: an entangling two-qubit cphase gate

Equation assumptions:

- Interaction acts only on |11>
- phi freely tunable
- Single-qubit phases are compensated by Rz

## eq_4: SWAP

$$
\mathrm{SWAP}|a,b\rangle=|b,a\rangle
$$

Exchanging the encoded positions of two walkers. It can be built from three CX gates.

Provenance: `abstract_inferred`. The abstract names a swap gate; its action is standard.

Abstract evidence: a swap gate

Equation assumptions:

- Non-interacting path crossing

## eq_5: Z-basis readout probability

$$
P(x)=|\langle x|\psi\rangle|^2,\quad x\in\{0,1\}^n
$$

Measuring qubit i in the computational basis corresponds to locating walker i. For X-basis measurement, apply H before measuring.

Provenance: `abstract_inferred`. Local position detection corresponds to a computational-basis measurement.

Abstract evidence: single-qubit measurements to be performed in a straightforward manner with localized operators

Equation assumptions:

- Ideal projective measurement

## Registers

- q: n (smallest instance n=2) qubits; one qubit per logical qubit, encoding the walker position on a two-site pair; qubit i is the i-th logical qubit
- c: n qubits; classical bits, measure(i,i); in Qiskit counts keys bits[::-1][i] is qubit i

## Initial state

|0...0> (all walkers on left sites)

## Measurement

Computational basis on each needed qubit i via measure(i,i). Unitary or statevector tasks take no measurements.

## Classical postprocessing

Reverse each counts key (bits[::-1]) so index i is qubit i. For the Steane extension, decode by a syndrome lookup table.

## Algorithm steps

1. Apply single-qubit Rx(theta) and Rz(theta) rotations on chosen qubits. (eq_1, eq_2)
2. Apply CP(phi) between the chosen pair of qubits (qiskit cp), and SWAP where connectivity requires it. (eq_3, eq_4)
3. Optionally apply H before measuring a qubit in the X basis, then measure the needed qubits, or read the statevector if the task asks for it. (eq_5)

## Assumptions

- Smallest instance is 2 qubits, since the task gives no scope
- Dual-rail encoding, with 2 vertices per qubit
- Idealized exact Hamiltonian evolution with freely tunable angles
- One walker per qubit, no loss; the circuit is a plain qubit circuit
- Gate-level circuit rather than a lattice simulation
- Steane encoding uses the standard CNOT circuit; syndrome ancillas would need to fit under the qubit cap

## Missing information

- The explicit Bose-Hubbard graph layout and Hamiltonian parameters
- The paper's gate-construction details and the exact logical encoding of the Steane code
- The task's qubit cap, angle values, and expected output format
