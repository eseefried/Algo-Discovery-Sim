# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct a mathematical specification of Grover's search algorithm executed on a 4-spin nuclear-spin-chain (Ising) quantum computer with nearest- and second-nearest-neighbour couplings, driven by resonant radio-frequency (Rabi) pulses, including the fidelity figure of merit and the 2πk-method condition that the abstract reports as governing maxima of the final fidelity as a function of the Rabi frequency.

Scope: ONE smallest useful construction (chosen as an assumption since no experiment_scope was supplied): a 4-qubit (N=16) Grover search for a single marked basis state w (instance w=|1111>, the all-spins-flipped state), with (i) the ideal gate-level Grover iteration as the reference, (ii) a drift Ising Hamiltonian with nearest- and second-nearest-neighbour z-z couplings, (iii) selective rectangular RF pulses parameterised by a Rabi frequency Omega, (iv) the fidelity between the ideal and the pulse-driven state, and (v) the 2πk resonance condition for the Rabi frequency with respect to the second-neighbour coupling. Outside scope: the paper's specific pulse-sequence decomposition of oracle and diffusion operators into RF pulses and free evolutions, numerical coupling/Larmor values, the time-resolved fidelity curves and the numerically obtained positions of the fidelity maxima.

## Symbols

- $n$: number of nuclear spins (qubits) in the chain; domain: n = 4 (abstract)
- $N$: search-space size, N = 2^n; domain: N = 16
- $I_k^{\alpha}$: spin-1/2 operator of nucleus k along axis alpha (I^alpha = sigma^alpha / 2); domain: alpha in {x,y,z}, k = 1..4
- $\omega_k$: Larmor (precession) frequency of spin k in the static field (assumed distinct for addressability); domain: real, positive, rad/s
- $J$: Ising coupling constant between nearest neighbours; domain: real, rad/s
- $J'$: Ising coupling constant between second-nearest neighbours; domain: real, rad/s
- $\Omega$: Rabi frequency of the RF driving pulse; domain: real, positive, rad/s
- $\nu, \varphi$: carrier frequency and phase of an RF pulse; domain: real
- $\tau$: duration of a single RF pulse; domain: real, positive, s
- $\Delta$: detuning of a non-targeted spin from the pulse carrier (set by couplings to its neighbours); domain: real, rad/s
- $k$: positive integer labelling the 2πk-method condition (number of full off-resonant rotations); domain: k in {1,2,3,...}
- $|w\rangle$: marked (target) computational basis state; domain: one of the 16 basis states; instance w = 1111
- $|s\rangle$: uniform superposition over all 16 basis states; domain: unit vector in C^16
- $G$: one Grover iteration (oracle followed by diffusion); domain: 16x16 unitary
- $r$: number of Grover iterations applied; domain: non-negative integer; instance r = 3
- $|\psi_{\rm ideal}(t)\rangle, |\psi(t)\rangle$: ideal (gate-level) reference state and actual pulse-driven state at time t; domain: unit vectors in C^16
- $F(t)$: fidelity between ideal and actual state at time t; domain: [0,1]

## eq_1: Drift Ising Hamiltonian of the spin chain with nearest and second-nearest neighbour couplings

$$
H_0 = -\sum_{k=1}^{4} \omega_k I_k^{z} - 2J\sum_{k=1}^{3} I_k^{z} I_{k+1}^{z} - 2J'\sum_{k=1}^{2} I_k^{z} I_{k+2}^{z}
$$

Time-independent Hamiltonian of the four-spin chain in the static magnetic field: individual Zeeman terms plus Ising (z-z) couplings between nearest neighbours (J) and second-nearest neighbours (J').

Provenance: `abstract_inferred`. The abstract specifies an Ising-type nuclear spin chain with nearest and second-nearest neighbour interactions; the explicit form, sign conventions and the factor 2 follow the standard Ising-spin-chain quantum-computer model and are not stated in the abstract.

Abstract evidence: taking into Ising type interactions between nearest and second nearest neighbours into account

Equation assumptions:

- Open chain of 4 spins with distinct Larmor frequencies omega_k so that spins are individually addressable
- Sign/normalisation convention (-2J I^z I^z) is a choice; the paper may use a different convention
- Only z-z (Ising) couplings, no flip-flop terms

## eq_2: RF pulse Hamiltonian (rotating-wave approximation)

$$
H_{\rm rf}(t) = -\Omega \sum_{k=1}^{4} \left[ I_k^{x}\cos(\nu t + \varphi) - I_k^{y}\sin(\nu t + \varphi) \right], \qquad H(t) = H_0 + H_{\rm rf}(t)
$$

Circularly polarised transverse RF field of Rabi frequency Omega, carrier frequency nu and phase varphi acting on all spins; a pulse tuned to nu = omega_k (shifted by the coupling-dependent offset of the desired neighbour configuration) rotates spin k selectively. Pulse duration tau with Omega tau = pi/2 or pi gives pi/2 or pi rotations on the resonant spin.

Provenance: `standard_background`. The abstract only names the Rabi frequency as the scanned parameter; the explicit form of the RF driving term is standard for RF-driven nuclear-spin quantum computers.

Equation assumptions:

- Rectangular pulses of constant amplitude
- Rotating-wave approximation valid (Omega, J, J' much smaller than omega_k)
- Pulses are applied sequentially; free evolution under H_0 between pulses

## eq_3: Ideal Grover iteration on 4 qubits

$$
|s\rangle = \frac{1}{4}\sum_{x=0}^{15}|x\rangle,\quad O_w = \mathbb{1} - 2|w\rangle\langle w|,\quad D = 2|s\rangle\langle s| - \mathbb{1},\quad G = D\,O_w
$$

Gate-level reference algorithm: uniform superposition, phase oracle marking w, inversion about the mean, and the Grover iterate G. Basis state |x> = |x_1 x_2 x_3 x_4> with spin k encoding bit x_k (spin up = 0, spin down = 1), x = sum_k x_k 2^{4-k}.

Provenance: `standard_background`. Grover's algorithm is named in the abstract; its standard operator definitions are recalled as background, not extracted from the paper.

Equation assumptions:

- Single marked item
- Register ordering: spin 1 is the most significant bit

## eq_4: Success amplitude and iteration count for N=16

$$
\sin\theta = \frac{1}{\sqrt{N}} = \frac{1}{4},\qquad |\langle w| G^{r}|s\rangle|^{2} = \sin^{2}\big((2r+1)\theta\big),\qquad r_{\rm opt} = \left\lfloor \frac{\pi}{4}\sqrt{N} \right\rfloor = 3
$$

Exact success probability after r ideal Grover iterations for a single marked item in N=16; three iterations give sin^2(7 theta) ≈ 0.961.

Provenance: `standard_background`. Standard Grover analysis specialised to the abstract's four-spin case; the abstract does not state how many iterations were simulated.

Equation assumptions:

- Single marked item
- The paper may have simulated a different number of iterations (e.g. a single iteration)

## eq_5: 2πk-method condition for the Rabi frequency with respect to the second-neighbour coupling

$$
\sqrt{\Omega^{2} + \Delta^{2}}\;\tau = 2\pi k,\quad \tau = \frac{\pi}{\Omega}\;\Rightarrow\; \Omega = \frac{|\Delta|}{\sqrt{4k^{2}-1}},\qquad |\Delta| = 2J'
$$

A spin detuned by Delta from the carrier of a pi pulse (Omega tau = pi) performs a full 2πk rotation about its tilted effective field and returns to its initial state (up to phase) when the generalised Rabi angle is a multiple of 2π, suppressing the unwanted non-resonant transition. Taking the detuning produced by the second-nearest-neighbour coupling, |Delta| = 2J' (in the convention of eq_1), gives discrete Rabi frequencies Omega_k at which the fidelity is maximal; for a pi/2 pulse (tau = pi/(2 Omega)) the condition reads Omega = |Delta|/sqrt(16k^2-1).

Provenance: `abstract_inferred`. The abstract states that fidelity maxima occur at Rabi frequencies satisfying the 2πk condition with respect to J'. The generic 2πk formula is standard background for spin-chain quantum computers; identifying the relevant detuning with the second-neighbour splitting 2J' is an inference from the quote, and the exact numerical prefactor depends on the paper's Hamiltonian convention.

Abstract evidence: we obtained pronounced maxima at frequencies which fulfil the condition of the 2πk-method with respect to the second nearest neighbour interactions

Equation assumptions:

- Detuning magnitude |Delta| = 2J' follows the convention of eq_1; a different convention (e.g. J' I^z I^z without factor 2, or frequency units) changes the prefactor
- Condition quoted for pi pulses; the paper may apply it to pi/2 pulses or both

## eq_6: Fidelity of the realisation

$$
F(t) = \left|\langle \psi_{\rm ideal}(t)|\psi(t)\rangle\right|^{2},\qquad |\psi(t)\rangle = \mathcal{T}\exp\!\left(-i\int_0^{t} H(t')\,dt'\right)|\psi(0)\rangle,\qquad F_{\rm final}(\Omega) = F(T_{\rm total})
$$

State fidelity between the pulse-driven state obtained by numerically integrating the Schrödinger equation under H(t) and the ideal gate-level state after the corresponding step of the algorithm; the final fidelity is evaluated at the end of the pulse sequence as a function of Omega.

Provenance: `abstract_inferred`. The abstract defines the figure of merit qualitatively (time-dependent and final fidelity vs Rabi frequency); the squared-overlap definition and the piecewise ideal reference are standard choices not confirmed by the abstract.

Abstract evidence: We determine the temporal behaviour of the fidelity during the algorithm, and we compute the final fidelity as a function of the Rabi frequency

Equation assumptions:

- Fidelity defined as squared overlap of pure states (the paper might use the overlap without squaring)
- Ideal reference state is piecewise constant, equal to the ideal state after the most recently completed logical gate
- hbar = 1

## Registers

- spin chain: 4 qubits; Four nuclear spins I_1..I_4 forming the search register; spin k encodes bit x_k (spin up = 0, down = 1), spin 1 is the most significant bit

## Initial state

|\psi(0)\rangle = |0000\rangle (all spins aligned with the static field, idealised pure ground state); the uniform superposition |s> is then created by a selective pi/2 pulse on each spin.

## Measurement

Projective measurement of all four spins in the z basis (computational basis); outcome x = 1111 is the search result with probability |<w|psi(T_total)>|^2 (ideal: sin^2(7 theta) for r = 3). In the numerical simulation no measurement is needed: the fidelity F is evaluated directly from the state vector.

## Classical postprocessing

Read the 4-bit outcome and verify it is the marked item; for the simulation, locate maxima of F_final(Omega) and compare with Omega_k = 2J'/sqrt(4k^2-1), k = 1,2,...

## Algorithm steps

1. Initialise the chain in |0000> and apply a pi/2 RF pulse (Omega tau = pi/2) to each of the four spins in turn to prepare the uniform superposition |s> (Hadamard-like step). (eq_1, eq_2, eq_3)
2. Implement the oracle O_w for w = 1111 as a conditional phase flip using selective pulses on one spin conditioned (through the J, J' shifts) on the states of the other spins, interleaved with free evolution under H_0. (eq_1, eq_2, eq_3)
3. Implement the diffusion operator D = 2|s><s| - 1 as pi/2 pulses on all spins, a conditional phase flip on |0000> (same technique as the oracle), and pi/2 pulses again. (eq_2, eq_3)
4. Repeat the oracle + diffusion block r times (instance r = 3 for N = 16). (eq_3, eq_4)
5. Throughout, integrate the Schrödinger equation under H(t) and record F(t); at the end of the sequence record F_final(Omega), scanning Omega and comparing maxima with the 2πk values Omega_k. (eq_5, eq_6)

## Assumptions

- No experiment_scope supplied: scope restricted to a single 4-qubit Grover search with one marked state w = 1111 and r = 3 iterations (choice of w and r is arbitrary)
- Hamiltonian convention of eq_1 (factor 2J, 2J', hbar = 1) is assumed; the paper's convention is unknown
- Only Ising (z-z) couplings, rotating-wave approximation, rectangular sequential pulses, no decoherence
- The specific pulse-sequence decomposition of oracle and diffusion operators is a generic proposal, not the paper's sequence
- Spin 1 is the most significant bit; spin up encodes 0

## Missing information

- Numerical values of Larmor frequencies omega_k, couplings J and J', pulse durations and total sequence time
- The paper's exact pulse sequence realising the oracle and the diffusion operator, and the number of Grover iterations simulated
- Which marked state(s) were used
- Precise definition of the fidelity (squared overlap or not) and of the ideal reference state during pulses
- Whether the 2πk condition was applied to pi pulses, pi/2 pulses, or both, and the exact detuning used (prefactor relating Delta to J')
- Numerical results: fidelity time traces and positions/heights of the fidelity maxima versus Rabi frequency
