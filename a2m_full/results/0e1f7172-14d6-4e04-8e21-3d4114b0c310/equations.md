# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Numerically search for a piecewise-constant single-qubit pulse sequence (effective singlet-triplet qubit, fixed gradient h0 about X plus controllable exchange J(t) about Z) that implements a target gate exactly while cancelling to first order the sensitivity to quasi-static gradient error delta_h and multiplicative exchange (voltage) noise eps; verify on a one-qubit statevector simulator.

Scope: One system qubit, no ancillas, N-segment piecewise-constant sequence, target = pi/2 rotation about one axis (e.g. X) as the smallest instance. Quasi-static noise only; first-order Magnus cancellation; the optimizer is run classically offline and the found parameters are fed into a fixed rx/rz circuit. Outside scope: non-quasi-static (colored) bath dynamics, filter-function treatment of time-dependent noise, realistic pulse-shape/bandwidth constraints, higher-order cancellation, the paper's specific sequences and fidelities.

## Symbols

- $N$: number of piecewise-constant segments; domain: positive integer, e.g. 4-8
- $J_k, \tau_k$: exchange amplitude and duration of segment k; domain: |J_k|<=J_max, tau_k>=tau_min, real
- $h_0$: fixed nominal gradient (X-axis) coefficient; domain: real, fixed
- $\delta_h$: quasi-static nuclear-bath gradient error; domain: real, small
- $\epsilon$: relative multiplicative error on J; domain: real, small
- $U_0(t)$: ideal (noise-free) propagator; domain: SU(2)
- $\Omega_1^{(\delta)},\Omega_1^{(\epsilon)}$: first-order Magnus error vectors for bath and voltage noise; domain: su(2) vectors in R^3
- $U_{tar}$: target gate; domain: SU(2)
- $C$: cost function to minimize; domain: nonnegative real
- $F$: gate fidelity; domain: [0,1]

## eq_1: Segment propagator

$$
U(\delta_h,\epsilon)=\prod_{k=N}^{1}\exp\!\Big[-i\tau_k\Big(\tfrac{J_k(1+\epsilon)}{2}Z+\tfrac{h_0+\delta_h}{2}X\Big)\Big]
$$

Total propagator of the piecewise-constant sequence with static errors. Factor 1/2 convention on X is an assumption.

Provenance: `assumption`. Concrete single-qubit model from the sketch for a singlet-triplet qubit; the abstract names only the noise types.

Equation assumptions:

- Effective single-qubit reduction
- Gradient error enters as an X term, exchange noise is multiplicative on J
- Normalization of coefficients is a choice

## eq_2: Toggling-frame error expansion

$$
U(\delta_h,\epsilon)=U_0(T)\exp\!\big[-i(\delta_h\,\Omega_1^{(\delta)}+\epsilon\,\Omega_1^{(\epsilon)})+O(2)\big],\quad \Omega_1^{(\delta)}=\tfrac12\int_0^T U_0^\dagger X U_0\,dt,\ \ \Omega_1^{(\epsilon)}=\tfrac12\int_0^T J_0(t)\,U_0^\dagger Z U_0\,dt
$$

First-order Magnus error terms in the toggling frame for the quasi-static noise.

Provenance: `abstract_inferred`. Perturbative minimization implies first-order error terms; explicit integrals are standard Magnus background applied to the assumed model.

Abstract evidence: allows sensitivity against non-Markovian decoherence and control errors to be perturbatively minimized via numerical search

Equation assumptions:

- Quasi-static noise
- Sketch writes bath operator as Z; here the bath operator is the X gradient term given eq_1 — choose consistently when implementing

## eq_3: Cost function

$$
C(\{J_k,\tau_k\})=1-\tfrac14\big|\mathrm{Tr}(U_{tar}^\dagger U_0(T))\big|^2\cdot 1+\|\Omega_1^{(\delta)}\|^2+\|\Omega_1^{(\epsilon)}\|^2
$$

Target-gate infidelity (for d=2, |Tr|^2/4 is the process fidelity) plus squared norms of first-order error vectors; C=0 means exact gate with first-order cancellation of both noises.

Provenance: `assumption`. Proposed formulation of the numerical search objective; weighting is unspecified in the abstract.

Equation assumptions:

- Equal weights
- Bounds on J_k and tau_k enforced by the optimizer

## eq_4: Robust-gate condition

$$
U_0(T)=U_{tar},\quad \Omega_1^{(\delta)}=0,\quad \Omega_1^{(\epsilon)}=0
$$

Conditions satisfied at a cost minimum of zero.

Provenance: `abstract_inferred`. Simultaneous leading-order cancellation plus a high-fidelity gate implies these conditions.

Abstract evidence: which simultaneously cancel to the leading order the dephasing due to non-Markovian nuclear-bath dynamics and voltage noise affecting the control fields

Equation assumptions:

- Exact solution exists for the chosen N and bounds

## eq_5: Fidelity readout

$$
F(\delta_h,\epsilon)=\tfrac14\big|\mathrm{Tr}\big(U_{tar}^\dagger U(\delta_h,\epsilon)\big)\big|^2,\qquad F_{state}=|\langle\psi_{tar}|U(\delta_h,\epsilon)|0\rangle|^2
$$

Fidelity swept over static errors; a plateau near zero error (1-F = O(error^4) for first-order cancellation in amplitude) confirms cancellation.

Provenance: `standard_background`. Standard fidelity definitions.

Equation assumptions:

- Static errors on a grid

## Registers

- q: 1 qubits; single effective singlet-triplet qubit, little-endian index 0, no ancilla

## Initial state

|0>

## Measurement

Statevector comparison preferred (no measurements); alternatively measure qubit 0 in the Z basis after the sequence and estimate population, which only tests state fidelity for one input.

## Classical postprocessing

Offline optimization of pulse parameters; compute F over the (delta_h, eps) grid; check the plateau width relative to an uncorrected baseline sequence.

## Algorithm steps

1. Fix h0, bounds on J and tau, N and target (pi/2 X rotation); define the model of eq_1. (eq_1)
2. Classically compute the error vectors and cost; run random-restart BFGS or gradient descent until C is near 0. (eq_2, eq_3, eq_4)
3. Build the circuit: for each segment apply rz(J_k tau_k) for exchange and rx(h0 tau_k) for gradient (angles = 2*coefficient*tau, noting segments with both terms non-commuting are approximated by sequential rotation unless split via small Trotter steps; exact segments need a single axis-tilted rotation, realizable with u or rotation about tilted axis via basis changes). (eq_1)
4. For each static (delta_h, eps) in a grid, rebuild the circuit with perturbed angles and compare statevector with the target; compute fidelity map. (eq_5)

## Assumptions

- Smallest instance chosen: one qubit, N around 4-8 segments, pi/2 X rotation target
- Quasi-static noise, first-order cancellation, and the optimizer finds exact solutions
- Segment with simultaneous J and h0 is a single rotation about axis (h0, 0, J) with angle tau*sqrt(h0^2+J^2)

## Missing information

- Paper's actual Hamiltonian normalization and control bounds
- Actual pulse sequences and parameter values
- Treatment of colored/non-Markovian bath beyond quasi-static
- Specific control-noise model (voltage-to-J relation, e.g. exponential)
- Universal gate set choice and optimizer details
