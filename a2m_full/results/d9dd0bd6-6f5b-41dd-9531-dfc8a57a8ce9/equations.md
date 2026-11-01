# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate a hidden random-walk phase trajectory phi_1..phi_N imprinted on a truncated-Fock squeezed-light register, from discretized homodyne-like outcomes, using a fixed-interval RTS smoother whose process-noise variance is chosen robustly (minimax MSE) over an uncertain q in [q_min,q_max].

Scope: One tiny instance: a 3-qubit truncated Fock register (dimension 8, even-photon squeezed vacuum amplitudes), N~4-6 time steps, one circuit per step with a hidden phi_k, many shots per step to get a measured outcome distribution, then classical scalar Kalman filter plus RTS smoother with a robust (inflated) q. Outside scope: continuous-mode treatment, true homodyne statistics, the paper's exact robust smoother derivation and parameter uncertainty model, experimental details.

## Symbols

- $\phi_k$: hidden phase at step k; domain: real, radians
- $q$: random-walk noise variance (uncertain); domain: q in [q_min,q_max], q>0
- $r$: effective readout noise variance of the phase measurement (assumed known or calibrated); domain: r>0
- $\xi$: squeezing parameter of the truncated state; domain: real, small, e.g. 0.5
- $c_n$: Fock amplitudes of squeezed vacuum, truncated and renormalized; domain: complex, n=0..7
- $y_k$: phase estimate/measurement derived from shot statistics at step k; domain: real
- $\hat x_{k|k},P_{k|k}$: filtered mean and variance; domain: real, P>=0
- $\hat x_{k|N},P_{k|N}$: smoothed mean and variance; domain: real, P>=0
- $q_r$: robust design noise variance used in the smoother; domain: [q_min,q_max]

## eq_1: Phase random walk

$$
\phi_{k+1}=\phi_k+w_k,\quad w_k\sim\mathcal N(0,q),\ q\in[q_{\min},q_{\max}]
$$

State model with uncertain diffusion variance.

Provenance: `abstract_inferred`. The abstract mentions phase noise with uncertain parameters; the random walk form is the assumed model.

Abstract evidence: uncertainties explicitly introduced in parameters underlying the phase noise

Equation assumptions:

- Gaussian random walk

## eq_2: Phase encoding on Fock register

$$
|\psi_k\rangle=e^{-i\phi_k \hat n}\sum_{n=0}^{7}c_n|n\rangle,\quad e^{-i\phi \hat n}=\bigotimes_{j=0}^{2}P(-2^{j}\phi)_j
$$

Diagonal phase gate with Fock number n=sum_j 2^j b_j (qubit j is bit j, little-endian), made of P gates.

Provenance: `assumption`. Proposed discretization of the phase shift; P gates on bits give exactly this diagonal.

Equation assumptions:

- Truncation to 8 levels
- c_n approx squeezed vacuum: c_{2m} proportional to (-tanh xi)^m sqrt((2m)!)/(2^m m!)

## eq_3: Quadrature-like readout

$$
p(y\mid\phi_k)=\left|\langle y|H^{\otimes3}|\psi_k\rangle\right|^2
$$

Hadamard-basis rotation then computational-basis measurement gives discretized outcome y in 0..7 (bit order little-endian: last counts character is qubit 0). Per-step phase measurement y_k is derived classically, e.g. by maximum likelihood over a phi grid, with effective variance r.

Provenance: `assumption`. Emulation of homodyne by basis rotation as in the sketch.

Equation assumptions:

- Phase-to-outcome map is not claimed to be linear; ML grid estimate with r calibrated by simulation

## eq_4: Kalman filter forward pass

$$
P_{k|k-1}=P_{k-1|k-1}+q_r,\ K_k=\frac{P_{k|k-1}}{P_{k|k-1}+r},\ \hat x_{k|k}=\hat x_{k|k-1}+K_k(y_k-\hat x_{k|k-1}),\ P_{k|k}=(1-K_k)P_{k|k-1}
$$

Scalar forward filter with design noise q_r.

Provenance: `standard_background`. Standard scalar Kalman filter for a random walk observed with noise.

Equation assumptions:

- Direct observation y_k=phi_k+v_k, v_k~N(0,r)

## eq_5: RTS fixed-interval smoother

$$
G_k=\frac{P_{k|k}}{P_{k|k}+q_r},\ \hat x_{k|N}=\hat x_{k|k}+G_k(\hat x_{k+1|N}-\hat x_{k|k}),\ P_{k|N}=P_{k|k}+G_k^2(P_{k+1|N}-P_{k+1|k})
$$

Backward pass from k=N-1 to 1, initialized by the filter at N.

Provenance: `standard_background`. Standard RTS recursion for a random walk.

Equation assumptions:

- Offline use of whole record

## eq_6: Minimax robust design

$$
q_r=\arg\min_{q_d\in[q_{\min},q_{\max}]}\ \max_{q\in[q_{\min},q_{\max}]}\ \mathrm{MSE}(q_d,q),\quad \mathrm{MSE}=\frac1N\sum_k\mathbb E(\hat x_{k|N}-\phi_k)^2
$$

Pick design q_r by grid search over q_d and q using simulated trajectories; the result is typically an inflated q.

Provenance: `abstract_inferred`. Minimax criterion is the assumed meaning of robust; the paper's exact design may differ (e.g. H-infinity).

Abstract evidence: robust fixed-interval smoother designed with uncertainties explicitly introduced in parameters underlying the phase noise

Equation assumptions:

- Minimax over interval is the robustness definition

## Registers

- fock: 3 qubits; truncated Fock register for the squeezed mode, little-endian n
- c: 3 qubits; classical bits for measured outcome y (bit i from qubit i)

## Initial state

|000> on fock; prepare normalized sum_n c_n|n> using a RY ladder plus controlled RYs (standard gates, no initialize)

## Measurement

Measure all 3 Fock qubits in the computational basis after H on each; many shots per time step.

## Classical postprocessing

ML phase estimate per step, Kalman filter, RTS smoother, minimax selection of q_r, MSE comparison versus true phi.

## Algorithm steps

1. Simulate or choose the hidden phase trajectory phi_k from the random walk with true q in the interval. (eq_1)
2. For each k build the circuit: state prep, P-gate phase shift with phi_k, H on all Fock qubits, measure all 3 qubits; collect counts. (eq_2, eq_3)
3. Convert counts to y_k by ML over a phi grid and calibrate r. (eq_3)
4. Run forward filter then RTS smoother with q_r. (eq_4, eq_5)
5. Choose q_r by minimax MSE, compare robust smoother, nominal smoother and filter under mismatched q. (eq_6)

## Assumptions

- Chosen smallest construction: 3-qubit Fock register, N about 5 steps
- Phase is directly observed with Gaussian noise of variance r
- Phase must lie in an unambiguous range, with possible 2π-periodic ambiguity ignored
- No black-box placeholder used; phase is applied by explicit P gates

## Missing information

- Paper's actual robust smoother equations and uncertainty model
- Continuous-time dynamics and real homodyne model
- Squeezing and noise parameters
- Query budget and which gate is the hidden box
