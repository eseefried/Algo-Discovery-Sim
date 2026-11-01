# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate the ground-state energy E_0(R) of the 2-qubit reduced STO-3G HeH+ Hamiltonian at a chosen bond distance R by iterative (Kitaev-style) phase estimation using one reused ancilla and two system qubits, then compare to exact diagonalization of the 4x4 matrix.

Scope: One bond distance with explicit symbolic coefficients g0..g5 (to be supplied classically per R), 3 qubits total, m-bit iterative PEA with exact compilation of controlled-U^(2^k). Outside scope: computing the molecular integrals, the NV-center hardware, pulse-level control, error analysis behind the 1e-14 Hartree figure, and the full dissociation scan beyond looping over R.

## Symbols

- $R$: HeH+ bond distance; domain: positive real
- $g_0,\dots,g_5$: Real coefficients of the reduced Hamiltonian at distance R, from classical integrals plus qubit mapping; domain: real
- $H$: 2-qubit reduced Hamiltonian; domain: 4x4 Hermitian
- $t$: Evolution time, chosen so that t*(E-E_ref) lies in a window of width less than 2\pi; domain: positive real
- $E_{ref}$: Energy offset (shift) used to avoid phase wrapping; domain: real
- $\varphi$: Phase fraction 0.b_1...b_m; domain: [0,1)
- $m$: Number of phase bits; domain: positive integer
- $b_k$: Measured ancilla bit for power 2^{k-1} (b_1 is most significant); domain: {0,1}
- $\theta_k$: Feedback rotation angle in round k; domain: real

## eq_1: Reduced Hamiltonian

$$
H = g_0 I + g_1 Z_0 + g_2 Z_1 + g_3 Z_0 Z_1 + g_4 X_0 X_1 + g_5 Y_0 Y_1
$$

Two-qubit form of the minimal-basis HeH+ electronic Hamiltonian after symmetry reduction

Provenance: `standard_background`. Known structure for minimal-basis 2-qubit molecular Hamiltonians; the abstract names only the minimal basis HeH+. The coefficients depend on R and the mapping and are not given.

Equation assumptions:

- STO-3G, 2 spatial orbitals, reduced to 2 qubits by symmetry
- g_i supplied classically for each R

## eq_2: Block structure and exact evolution

$$
H|00\rangle=(g_0+g_1+g_2+g_3)|00\rangle,\; H|11\rangle=(g_0-g_1-g_2+g_3)|11\rangle,\; H|_{\{01,10\}}=(g_0-g_3)I+(g_1-g_2)Z+(g_4+g_5)X
$$

The XX and YY terms act in the odd-parity subspace {|01>,|10>}; XX+YY couples these with amplitude g4+g5 and annihilates |00>,|11>. U=e^{-iHt} is diagonal phases on |00>,|11> and a 2x2 rotation with phase e^{-i(g0-g3)t} on the odd block.

Provenance: `standard_background`. Direct algebra: XX+YY = 2(|01><10|+|10><01|) up to sign, so on the odd block it acts as 2X; hence the coupling coefficient is 2(g4+g5) if XX+YY is interpreted as X0X1+Y0Y1 with g4=g5, and the exact value should be recomputed from the matrix before implementation. The qubit-label convention for Z0 and Z1 must be fixed.

Equation assumptions:

- Little-endian: qubit 0 is the least significant bit of the state label
- Recompute the odd-block matrix numerically rather than trusting the closed form

## eq_3: Phase encoding

$$
U|\psi_j\rangle=e^{-i(E_j-E_{ref})t}|\psi_j\rangle,\quad 2\pi\varphi=-(E-E_{ref})t \bmod 2\pi
$$

Eigenphase of U relates to energy; t and E_ref are chosen so the mapping is unambiguous over the spectrum

Provenance: `standard_background`. Standard PEA relation. Global phase of U becomes relative phase only via the controlled version, so the offset E_ref can be included as a phase gate on the ancilla control.

Equation assumptions:

- Spectrum fits in a window of width less than 2\pi/t
- Controlled-U implemented with the E_ref phase included as a phase gate on the control

## eq_4: Iterative feedback and bit extraction

$$
\theta_k=-2\pi\,0.0b_{k+1}\dots b_m,\quad P(b_k=0)=\cos^2\!\big(\pi(2^{k-1}\varphi'+\theta_k/2\pi)\big)\text{ up to sign convention}
$$

Round k applies H on ancilla, controlled-U^{2^{k-1}}, phase feedback from previously measured less significant bits, H, then measure. Rounds run from k=m down to 1, so the least significant bit is measured first.

Provenance: `standard_background`. Kitaev/Dorner iterative PEA. The exact sign convention must be validated by simulation; if \varphi is exactly m-bit representable the outcome is deterministic.

Equation assumptions:

- Eigenstate prepared exactly, or sufficient overlap with repetition
- Ancilla reset between rounds

## eq_5: Energy readout

$$
E = E_{ref} - \frac{2\pi\varphi}{t},\quad \varphi=\sum_{k=1}^m b_k 2^{-k},\quad \delta E\approx \frac{2\pi}{t\,2^m}
$$

Energy from the measured bits with resolution set by m

Provenance: `abstract_inferred`. The small uncertainty is attributed to digital phase resolution in this inferred iterative-PEA reading; the abstract does not state the algorithm. 1e-14 Hartree would need roughly 2^-m*2π/t below 1e-14, i.e. m around 45 bits, which is far beyond a small simulation.

Abstract evidence: we report an energy uncertainty (given our model basis) of the order of $10^{-14}$ Hartree

Equation assumptions:

- The method is iterative PEA (inferred, unconfirmed)

## Registers

- anc: 1 qubits; Reused ancilla (NV electron spin), measured and reset each round
- sys: 2 qubits; System qubits (nuclear spins) holding the reduced molecular state
- c: m classical bits qubits; Measured phase bits b_k; the first measured is the least significant

## Initial state

|0>_anc ⊗ HF state on sys, X applied to the appropriate qubit to make |01> (or |10>), in the little-endian convention, with the Hartree-Fock determinant parity assumed to lie in the odd-parity block

## Measurement

Measure the ancilla only, once per round, into classical bit for b_k; system qubits are not measured. With Qiskit little-endian counts the last character is classical bit 0, so assign each b_k a defined clbit index and reverse carefully.

## Classical postprocessing

Compute phi=sum b_k 2^-k, E=E_ref-2*pi*phi/t, repeat shots to reduce overlap error and pick the lowest consistent outcome, compare to the smallest eigenvalue of the 4x4 H.

## Algorithm steps

1. Classically compute g_0..g_5 for chosen R, choose t and E_ref so the spectrum fits in one phase window; precompute the exact 4x4 matrix and eigenvalues for comparison. (eq_1, eq_3)
2. Prepare the Hartree-Fock state on the system qubits with X gates. (eq_2)
3. For k=m down to 1: reset ancilla, H on ancilla, controlled-U^{2^{k-1}} (exact compile, or one query to the black box per round if so supplied), phase feedback Rz/P with angle theta_k computed from earlier bits, H, measure ancilla into bit b_k. (eq_2, eq_4)
4. Classically assemble phi from the bits and compute E; compare with exact diagonalization; repeat for each R. (eq_5)

## Assumptions

- Minimal-basis 2-qubit reduction with a specific mapping
- Hartree-Fock overlap with ground state is nonzero
- t and E_ref chosen to avoid aliasing
- Controlled-U^{2^k} compiled exactly (not Trotter)
- Mid-circuit measurement and reset with classical feedback is available
- The iterative PEA identification is inferred from the abstract, not stated

## Missing information

- Actual g_i(R) values and the qubit mapping used in the paper
- Exact control-gate decomposition and NV pulse sequence
- Number of phase bits m and the time t used
- Whether the paper used iterative PEA at all
- How the 1e-14 Hartree uncertainty was defined
