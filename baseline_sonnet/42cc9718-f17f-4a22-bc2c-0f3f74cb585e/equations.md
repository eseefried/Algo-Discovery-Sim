# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Estimate a time-varying optical phase of a squeezed light state from noisy homodyne-type measurements, comparing a standard fixed-interval smoother with a robust smoother that accounts for uncertainty in parameters of the phase noise model. The abstract gives no explicit equations.

Scope: Smallest useful construction: a scalar linear-Gaussian phase-tracking model (random-walk phase, linear measurement) with a standard fixed-interval Rauch-Tung-Striebel smoother as the nominal baseline. The paper-specific robust smoother design, uncertainty set, squeezed-state measurement model and performance results are outside scope. This is a classical estimation baseline, not a quantum circuit.

## Symbols

- $\phi_k$: Optical phase at time step k; domain: real, radians
- $q$: Phase-noise (diffusion) variance per step; the uncertain parameter in the robust setting; domain: q>0
- $w_k$: Process noise driving the phase; domain: real Gaussian, variance q
- $y_k$: Measurement record at step k; domain: real
- $v_k$: Measurement noise; domain: real Gaussian, variance r
- $r$: Measurement noise variance; domain: r>0
- $\hat\phi_{k|N},P_{k|N}$: Smoothed phase estimate and its variance given data y_1..y_N; domain: real; nonnegative real
- $N$: Fixed-interval length; domain: positive integer

## eq_1: Phase random-walk model

$$
\phi_{k+1}=\phi_k+w_k,\quad w_k\sim\mathcal N(0,q)
$$

Assumed scalar phase noise model with diffusion parameter q

Provenance: `assumption`. The abstract mentions phase noise parameters but not their form; a random walk is a simple proposed instance.

Equation assumptions:

- Wiener-type phase diffusion
- Gaussian increments

## eq_2: Linearized measurement model

$$
y_k=\phi_k+v_k,\quad v_k\sim\mathcal N(0,r)
$$

Assumed effective linear measurement of the phase

Provenance: `assumption`. Actual squeezed-light measurement model is not given; this is a placeholder linear-Gaussian approximation.

Equation assumptions:

- Small-phase linearization
- Gaussian measurement noise

## eq_3: Kalman filter recursion

$$
P_{k|k-1}=P_{k-1|k-1}+q,\; K_k=\frac{P_{k|k-1}}{P_{k|k-1}+r},\; \hat\phi_{k|k}=\hat\phi_{k|k-1}+K_k(y_k-\hat\phi_{k|k-1}),\; P_{k|k}=(1-K_k)P_{k|k-1}
$$

Forward filtering pass with nominal q, with \hat\phi_{k|k-1}=\hat\phi_{k-1|k-1}

Provenance: `standard_background`. Standard Kalman filter for the scalar model above.

Equation assumptions:

- Nominal known q and r

## eq_4: Fixed-interval RTS smoother

$$
J_k=\frac{P_{k|k}}{P_{k+1|k}},\;\hat\phi_{k|N}=\hat\phi_{k|k}+J_k(\hat\phi_{k+1|N}-\hat\phi_{k+1|k}),\;P_{k|N}=P_{k|k}+J_k^2(P_{k+1|N}-P_{k+1|k})
$$

Backward pass for k=N-1,...,1 giving the nominal smoothed estimate

Provenance: `standard_background`. Standard RTS fixed-interval smoother; the paper's robust variant is not specified in the abstract.

Equation assumptions:

- Exact arithmetic; nominal parameters

## eq_5: Robustness target (qualitative)

$$
q\in[q_{\min},q_{\max}]
$$

Assumed interval uncertainty in the phase-noise parameter, which the robust smoother would be designed to tolerate

Provenance: `assumption`. The abstract says uncertainties are explicitly introduced in phase noise parameters, but not the uncertainty model.

Equation assumptions:

- Interval uncertainty is a placeholder; the paper's model may differ

## Classical postprocessing

Compare the mean-square error of the smoothed estimates against the true phase trajectory for nominal and mismatched q.

## Algorithm steps

1. Fix a tiny instance, e.g. N=5, nominal q and r, with prior phase mean and variance. (eq_1, eq_2)
2. Run the forward Kalman filter with nominal parameters. (eq_3)
3. Run the backward RTS pass to obtain nominal fixed-interval smoothed estimates. (eq_4)
4. Evaluate the smoother when the true q lies in an uncertainty interval. The robust design itself is not reconstructed. (eq_5)

## Assumptions

- No scope was provided, so a scalar linear-Gaussian toy instance was chosen.
- The problem is classical state estimation; no quantum circuit is implied.
- Squeezing level, measurement type and robust criterion are unspecified.

## Missing information

- Actual phase-noise model and which parameters are uncertain
- Squeezed-state measurement model (e.g. homodyne) and noise levels
- Robust smoother formulation (minimax, H-infinity, or other) and uncertainty set
- Performance metric and the reported quantitative improvement
