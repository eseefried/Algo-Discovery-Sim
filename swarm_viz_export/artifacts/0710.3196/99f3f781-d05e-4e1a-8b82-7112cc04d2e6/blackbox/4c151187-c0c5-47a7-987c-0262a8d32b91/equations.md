# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Grover search on 4 qubits (N=16) with one marked basis state w, as an ideal gate-level unitary that includes the initial Hadamard layer, with an optional second-neighbour ZZ phase layer standing in for the nuclear-spin-chain Ising couplings.

Scope: Ideal Grover algorithm on 4 qubits with k=3 iterations. The unitary built from |0000> includes H^{\otimes 4} as its first layer. An optional ZZ_{j,j+2} phase layer follows each Grover iteration. The pulse-level Hamiltonian, the Rabi-frequency scan and the 2πk-condition maxima are outside this scope. No query complexity is claimed and the oracle is compiled from the explicit w.

## Symbols

- $N$: search space size, 2^n; domain: N=16
- $n$: number of qubits (spins); domain: n=4
- $w$: marked basis state; domain: integer in 0..15, assumed w=5 unless specified
- $x_j$: bit j of x, on qubit q_j; domain: {0,1}
- $|s\rangle$: uniform superposition; domain: state in (C^2)^{\otimes 4}
- $k$: number of Grover iterations; domain: integer, 3
- $\theta$: Grover angle, sin θ = 1/sqrt(N); domain: (0, π/2)
- $\phi$: optional second-neighbour ZZ error phase; domain: real, default 0
- $F_t$: fidelity with |w> after iteration t; domain: [0,1]

## eq_1: Uniform initial state

$$
|s\rangle=H^{\otimes 4}|0000\rangle=\frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle,\quad x=\sum_{j=0}^{3}x_j2^j
$$

State preparation. The built unitary must start with H on all four qubits. q0 is the least significant bit.

Provenance: `standard_background`. Standard Grover initialisation. The reviewer found the Hadamard layer missing in a previous build, so it is now mandatory in the circuit.

Equation assumptions:

- Little-endian encoding
- Circuit applied to |0000>

## eq_2: Oracle and diffusion

$$
O_w=I-2|w\rangle\langle w|,\quad D=2|s\rangle\langle s|-I,\quad G=D\,O_w
$$

Phase oracle and inversion about the mean; one Grover iteration.

Provenance: `standard_background`. Standard Grover search. The abstract names the algorithm but gives no equations.

Equation assumptions:

- Single marked state
- Oracle compiled from the explicit w

## eq_3: Gate decomposition

$$
O_w=X^{\bar w}\,CCCZ\,X^{\bar w},\quad D\simeq H^{\otimes4}X^{\otimes4}\,CCCZ\,X^{\otimes4}H^{\otimes4}
$$

X^{\bar w} applies X to the qubits where w has a 0 bit. The diffusion circuit equals D up to a global phase of -1.

Provenance: `standard_background`. Standard multi-controlled-Z construction.

Equation assumptions:

- Global phase is irrelevant

## eq_4: Iteration count and success probability

$$
k=\mathrm{round}\left(\frac{\pi}{4}\sqrt{N}-\frac12\right)=3,\quad P_{succ}=\sin^2((2k+1)\theta)\approx0.961
$$

Exact for ideal gates, evaluated at N=16, k=3. k is fixed at 3 for this instance; do not use floor(x) as a general substitute.

Provenance: `standard_background`. Standard Grover analysis.

Equation assumptions:

- Ideal gates, phi=0

## eq_5: Fidelity and optional ZZ error layer

$$
F_t=|\langle w|\psi_t\rangle|^2,\quad E_{\phi}=\prod_{j=0}^{1}\exp\left(-i\phi Z_jZ_{j+2}/4\right)
$$

Fidelity after each Grover iteration. E_phi is an optional second-neighbour ZZ layer applied after each G; as RZZ(angle)=exp(-i angle ZZ/2), the angle is phi/2.

Provenance: `assumption`. The abstract mentions fidelity and second-nearest-neighbour Ising interactions. The error layer is a proposed simplification, not the paper's model.

Equation assumptions:

- The error is a pure ZZ phase layer
- Nearest-neighbour terms are omitted
- phi is a free parameter

## Registers

- q: 4 qubits; spin-chain qubits q0..q3; q0 is the least significant bit; all are data qubits, no ancillas

## Initial state

|0000>

## Measurement

Measure all qubits in the computational basis and read x=sum x_j 2^j. The circuit is measurement-free, so measurement is applied outside it.

## Classical postprocessing

Output x as the candidate marked element w. Success probability is about 0.961 for phi=0.

## Algorithm steps

1. Apply H to all 4 qubits to prepare |s>. This layer is part of the built unitary. (eq_1)
2. Repeat k=3 times: apply O_w, then D, then optionally E_phi (phi=0 by default). (eq_2, eq_3, eq_4, eq_5)
3. Optionally record F_t after each iteration from the simulated state. (eq_5)

## Assumptions

- Marked state w is an explicit instance parameter, assumed w=5 (binary 0101) unless specified
- The Hamiltonian-level pulse model is not reproduced
- n=4 matches the abstract's four-spin simulation

## Missing information

- Actual spin-chain Hamiltonian parameters and coupling values
- Pulse sequences for each gate
- Rabi-frequency scan and 2πk-condition details
- The marked state used in the paper
