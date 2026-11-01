# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Reconstruct the logical gate algebra of the bosonic-walker universal-computation scheme: dual-rail position encoding, Rx via tunnelling, Rz via detuning, and CZ via on-site Bose-Hubbard interaction, on a tiny 2-qubit instance.

Scope: Single-particle 4-mode dual-rail model of 2 qubits (qubit 0 on modes 0,1; qubit 1 on modes 2,3), reduced to the 4-dimensional logical space. One Rx(theta) on qubit 0, one Rz(phi) on qubit 1, then one CZ. Out of scope: piecewise-constant graph geometry, 2D lattice layout, full bosonic many-body dynamics, swap routing, Steane code, 3D extension, ultracold-atom implementation, error correction, and the full proof of universality.

## Symbols

- $a_i^\dagger,a_i$: bosonic creation/annihilation operators on site i; domain: operators
- $J$: hopping amplitude; domain: real >0
- $U$: on-site interaction strength; domain: real
- $\theta$: X-rotation angle; domain: real
- $\phi$: Z-rotation angle; domain: real
- $t$: evolution time; domain: real >=0

## eq_1: Bose-Hubbard Hamiltonian

$$
H=-J\sum_{\langle i,j\rangle}\left(a_i^\dagger a_j+a_j^\dagger a_i\right)+\frac{U}{2}\sum_i n_i(n_i-1)
$$

Standard Bose-Hubbard model as the underlying dynamics. The interaction normalization n(n-1)/2 is taken from the method sketch.

Provenance: `standard_background`. The abstract names the Bose-Hubbard model but gives no explicit form. This is the textbook form. The predicted U n(n-1) factor and the predicted coupling formulas J=4πa^3/m, U=2πa^3/λ are not adopted.

Equation assumptions:

- Spinless bosons
- The exact graph and lattice geometry are not specified

## eq_2: Dual-rail encoding

$$
|0\rangle_k=a_{2k}^\dagger|\mathrm{vac}\rangle,\quad |1\rangle_k=a_{2k+1}^\dagger|\mathrm{vac}\rangle
$$

Each qubit is one walker on a two-site pair, so the number of sites is 2n, linear in the number of qubits.

Provenance: `assumption`. The abstract says information is encoded in walker positions and that the vertex count is linear in the qubit number. The specific two-site encoding is a proposed instance.

Equation assumptions:

- Site ordering is qubit-major
- Basis index is 2*q0+q1 with qubit 0 most significant

## eq_3: X rotation via hopping

$$
R_x(\theta)=e^{-i\theta X/2}=\exp\!\left[i Jt\,(a_{0}^\dagger a_{1}+a_{1}^\dagger a_{0})\right],\quad Jt=\theta/2
$$

In the single-particle sector, hopping between the two rails of a qubit acts as the Pauli X generator, which gives an Rx rotation.

Provenance: `abstract_inferred`. The abstract claims arbitrary X rotations. Hopping with sign -J gives exp(+iJtX), so Jt=θ/2 gives exp(-iθX/2) only if the sign is absorbed into the convention (apply Jt=-θ/2 for the literal -J Hamiltonian). The mechanism is the sketch's, not the paper's.

Abstract evidence: Arbitrary X and Z rotations are constructed

Equation assumptions:

- Single-particle subspace
- Sign convention absorbed into the definition of t or J

## eq_4: Z rotation via detuning

$$
R_z(\phi)=e^{-i\phi Z/2}=\mathrm{diag}(e^{-i\phi/2},e^{i\phi/2})
$$

A relative on-site energy offset between the two rails of a qubit, applied for time t, produces a Z rotation.

Provenance: `abstract_inferred`. The abstract claims Z rotations. A detuning of magnitude Δ with Δt=φ gives this unitary up to a global phase. The mechanism is the sketch's.

Abstract evidence: Arbitrary X and Z rotations are constructed

Equation assumptions:

- Detuning is applied locally to one site pair

## eq_5: CZ via interaction phase

$$
\mathrm{CZ}=\mathrm{diag}(1,1,1,-1)=e^{-iUt\,|11\rangle\langle 11|},\quad Ut=\pi
$$

The interaction phase acts only when both walkers are in the |1> rail, giving a controlled-phase gate at Ut=π.

Provenance: `abstract_inferred`. The abstract states a cphase gate exists. The mechanism of bringing the walkers together is a sketch assumption. In the 4-dimensional logical space it is compiled directly as a diagonal gate.

Abstract evidence: an entangling two-qubit cphase gate

Equation assumptions:

- Interaction is active only for |11>
- Walker routing is idealized away

## eq_6: Target logical unitary

$$
U_{\rm tot}=\mathrm{CZ}\,\left(I\otimes R_z(\phi)\right)\left(R_x(\theta)\otimes I\right)
$$

Composite logical unitary for the 2-qubit instance, acting on the 4-dimensional logical register.

Provenance: `assumption`. A tiny instance chosen to test the gate algebra.

Equation assumptions:

- Qubit 0 is the left tensor factor

## Registers

- q0: 2 modes (sites 0,1) qubits; dual-rail logical qubit 0
- q1: 2 modes (sites 2,3) qubits; dual-rail logical qubit 1

## Initial state

Logical |00>, i.e. one walker on site 0 and one on site 2. Other inputs are a user-chosen superposition of the four logical basis states, prepared externally.

## Measurement

Position measurement of each walker in the computational basis: a rail index of 0 or 1 gives the logical bit. A single-qubit measurement is a local measurement on one site pair. The circuit itself is measurement-free.

## Classical postprocessing

Decode the logical probabilities over |q0 q1> from walker positions. Basis index is 2*q0+q1.

## Algorithm steps

1. Apply Rx(theta) on qubit 0 as a 2x2 block on its logical subspace (hopping for Jt=theta/2). (eq_3)
2. Apply Rz(phi) on qubit 1 as a diagonal detuning phase. (eq_4)
3. Apply the CZ phase (-1 on logical |11>) from the on-site interaction at Ut=pi. (eq_5, eq_6)

## Assumptions

- Reduced to the 4-dimensional logical subspace, not simulating the full bosonic Fock space
- Explicit classical parameters theta and phi are compiled into gates
- Swap is not included; it could be built from three CNOTs, each a CZ plus Hadamards from Rx and Rz
- This verifies logical gate algebra only, not black-box query complexity

## Missing information

- Piecewise-constant graph geometry and the actual construction on it
- Paper's actual gate schedules and how the walkers are routed
- Swap gate construction on the graph
- Steane code encoding and the 3D extension
- Physical parameters for the optical-lattice implementation
