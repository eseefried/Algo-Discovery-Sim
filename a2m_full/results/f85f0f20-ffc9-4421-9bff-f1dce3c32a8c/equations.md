# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement universal one- and two-qubit gates (e.g. single-qubit H/Rx on either electron, CNOT/CZ) on two exchange-coupled electron spins with constant exchange J and a small g-factor difference. Controls are a piecewise-constant static field amplitude within a few Gauss plus RF drive, found by optimal control. The simulator realizes this as a fixed 2-qubit Trotterized slice circuit with classically precomputed angles.

Scope: Smallest construction: 2 qubits, no ancillas. A model Hamiltonian with constant Heisenberg exchange and different Zeeman terms is split into N piecewise-constant slices. Each slice is Rz Zeeman, RXX/RYY/RZZ exchange, and Rx/Ry drive gates. Angles are optimized offline by GRAPE-like ascent for a target gate (CNOT or CZ) and hard-coded. Fidelity is judged on the unitary up to global phase, with an optional Bell-state check. Outside scope: the paper's actual parameter values, RWA derivation, the exact decoupling pulse sequence, and the numerical results.

## Symbols

- $g_1,g_2$: electron g-factors, with small difference \Delta g=g_1-g_2; domain: positive reals
- $\mu_B$: Bohr magneton; domain: positive real
- $B$: static magnetic field amplitude, varied by a few Gauss; domain: real
- $J$: constant exchange coupling; domain: real
- $\Omega_k,\phi_k$: RF drive amplitude and phase in slice k; domain: real
- $N$: number of time slices; domain: positive integer
- $\Delta t$: slice duration; domain: positive real
- $\theta$: vector of all control parameters (B_k,\Omega_k,\phi_k); domain: real vector
- $F$: gate fidelity vs target; domain: [0,1]
- $U_{target}$: target 4x4 gate, e.g. CNOT or CZ; domain: U(4)

## eq_1: Model Hamiltonian

$$
H(t)=\frac{g_1\mu_B B}{2}Z_1+\frac{g_2\mu_B B}{2}Z_2+\frac{J}{4}(X_1X_2+Y_1Y_2+Z_1Z_2)+\frac{\Omega(t)}{2}\big[\cos(\omega t+\phi)(X_1+X_2)+\sin(\omega t+\phi)(Y_1+Y_2)\big]
$$

Two spins with different Zeeman splittings, constant Heisenberg exchange and a transverse RF drive that acts on both spins but is resonant with only one at a time. The Hamiltonian is the form given in the sketch; the exact normalization of J and the drive are assumptions.

Provenance: `assumption`. The abstract names two coupled electrons, constant exchange, and a small g difference, but gives no explicit Hamiltonian.

Equation assumptions:

- Heisenberg-type exchange
- hbar=1
- coupling normalization chosen
- RF drive couples to both spins

## eq_2: Selective resonance

$$
\omega=g_k\mu_B B,\quad |g_1-g_2|\mu_B B\gg\Omega
$$

Changing B by a few Gauss brings one electron and then the other into resonance with the RF frequency, so the drive acts selectively.

Provenance: `abstract_inferred`. Addressing via a small g difference implies different resonance conditions for the two spins. The selectivity inequality is my assumption.

Abstract evidence: Small g-factor difference of electrons allows to address qubits and to avoid strong magnetic field pulses.

Equation assumptions:

- RWA
- the selectivity condition holds

## eq_3: Slice product unitary

$$
U(\theta)=\prod_{k=N}^{1}\exp\!\big[-iH_k\Delta t\big]\approx\prod_{k=N}^{1}\Big[R_x R_y\text{-drive}_k\;e^{-i\frac{J\Delta t}{4}(XX+YY+ZZ)}\;R_z^{(1)}(\varphi_{1,k})R_z^{(2)}(\varphi_{2,k})\Big]
$$

The evolution is a product of piecewise-constant slice propagators. The circuit approximates each slice by a Trotter splitting into Rz, RXX/RYY/RZZ and Rx/Ry gates. XX, YY and ZZ commute, so the exchange factor is exact.

Provenance: `assumption`. The abstract says optimal control finds the evolution; the slice parametrization follows the sketch.

Equation assumptions:

- Trotter splitting error neglected or absorbed in the optimization
- \varphi_{j,k}=g_j\mu_B B_k\Delta t
- little-endian: q0=electron 1

## eq_4: Fidelity objective

$$
F(\theta)=\frac{|\mathrm{Tr}(U_{target}^\dagger U(\theta))|}{4},\quad \theta^*=\arg\max_\theta F
$$

Phase-insensitive gate fidelity maximized by gradient ascent (GRAPE-style) to find the controls.

Provenance: `abstract_inferred`. Optimal control implies maximizing a fidelity objective. The specific form is the standard one.

Abstract evidence: To find the evolution of the two-qubit system, we use the algorithms of the optimal control theory.

Equation assumptions:

- global phase ignored
- unitary dynamics, no decoherence

## eq_5: Exchange suppression by refocusing

$$
\sigma_x^{(1)}\sigma_x^{(2)}\,e^{-i\frac{J t}{4}(\vec\sigma_1\cdot\vec\sigma_2)}\,\sigma_x^{(1)}\sigma_x^{(2)}=e^{-i\frac{Jt}{4}(\vec\sigma_1\cdot\vec\sigma_2)}
$$

The Heisenberg coupling is invariant under simultaneous rotations of both spins, so a common pi pulse does not refocus it. Suppression therefore needs spin-selective rotations, e.g. a pi pulse on one spin only, which flips the sign of the XX and YY parts. I flag this as a caveat on the sketch's dynamical decoupling claim, and the actual sequence is unspecified.

Provenance: `standard_background`. This is a fact about the Heisenberg interaction. It shows that the suppression sequence must be spin-selective and not a global pi pulse.

Equation assumptions:

- ideal instantaneous pulses

## Registers

- q: 2 qubits; q0 = electron 1 spin, q1 = electron 2 spin; no ancillas

## Initial state

|00> for the unitary check. For the Bell test, apply H on q0 and then CNOT(q0,q1).

## Measurement

Prefer the unitary or statevector with no measurements. For the optional Bell check, measure both qubits and expect correlated 00/11 outcomes.

## Classical postprocessing

Offline GRAPE optimization of the angles. Evaluate F(\theta) on the simulated unitary.

## Algorithm steps

1. Fix the target gate, N, \Delta t, and the J, g_1, g_2 values. Run GRAPE offline to obtain the slice angles and hard-code them. (eq_1, eq_4)
2. Build the single-qubit selective rotations, with one electron resonant at a time via the B shift. (eq_2)
3. For each slice, apply the Rz Zeeman phases, the RXX/RYY/RZZ(J\Delta t/2) exchange, and the Rx/Ry drive gates, then concatenate the N slices. (eq_3)
4. Compare the unitary to U_target up to global phase via F. Optionally measure the Bell-state counts. (eq_4)

## Assumptions

- Heisenberg exchange with J constant and always on
- RWA holds
- piecewise-constant controls with fixed N
- angles are precomputed offline
- global phase ignored
- no decoherence
- all numerical parameter values chosen by me

## Missing information

- Actual Hamiltonian normalization and parameter values (J, \Delta g, B)
- The decoupling pulse sequence
- Control pulse shapes and numerical results
- The optimized angles
