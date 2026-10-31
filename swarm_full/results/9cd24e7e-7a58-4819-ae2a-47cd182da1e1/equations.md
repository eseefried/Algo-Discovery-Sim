# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Estimate a fluctuating optical phase imprinted on a squeezed state of light using a robust fixed-interval smoother that explicitly accounts for uncertainty in the parameters governing the phase noise, and show improved estimation over a non-robust smoother.

Scope: Abstract-level estimation-theory reconstruction; not a gate-based circuit. Only a generic phase-noise model, smoother, and robust cost are given as labeled background or assumptions. The specific noise model, uncertainty set, and measurement scheme are not in the abstract.

## Symbols

- $\phi(t)$: time-varying optical phase to be estimated; domain: real-valued stochastic process on [0,T]
- $\theta$: uncertain parameter of the phase noise model; domain: \theta\in\Theta, uncertainty set
- $y(t)$: measurement record; domain: real-valued process
- $\hat\phi_s(t)$: fixed-interval smoothed phase estimate using all data over [0,T]; domain: real

## eq_1: Phase diffusion model

$$
d\phi=\sqrt{\theta}\,dW
$$

Assumed Wiener phase-noise model with uncertain diffusion parameter theta.

Provenance: `assumption`. The abstract mentions phase noise parameters but not the model, so a simple Wiener process is assumed.

Equation assumptions:

- Wiener phase diffusion
- scalar theta

## eq_2: Smoothed estimate

$$
\hat\phi_s(t)=\mathbb{E}[\phi(t)\mid y(\tau),\,0\le\tau\le T]
$$

Fixed-interval smoother conditions on the whole record over [0,T].

Provenance: `standard_background`. Standard definition of fixed-interval smoothing.

## eq_3: Robust criterion

$$
\min_{\hat\phi}\max_{\theta\in\Theta}\mathbb{E}\left[(\phi-\hat\phi)^2\right]
$$

Minimax mean-square error over the parameter uncertainty set, as one possible robust design.

Provenance: `assumption`. The abstract says the smoother is robust to uncertainty in parameters but does not specify the criterion.

Equation assumptions:

- MSE cost
- minimax formulation

## Registers

- optical_mode: 1 squeezed optical mode (assumed) qubits; Squeezed light carrying the fluctuating phase phi(t)

## Initial state

Single-mode squeezed vacuum (assumed), squeezing level unspecified in abstract

## Measurement

Continuous homodyne-type detection of the phase-modulated squeezed light over [0,T], yielding y(t) (assumed; scheme not stated in abstract).

## Classical postprocessing

Apply the robust fixed-interval smoother (assumed minimax MSE) to the full record y(t), then compare against a non-robust smoother, e.g. by MSE.

## Algorithm steps

1. Prepare squeezed light and imprint the fluctuating phase phi(t), modeled as diffusion with uncertain parameter theta. (eq_1)
2. Record the measurement signal y(t) over the fixed interval [0,T]. (no equation reference)
3. Compute the fixed-interval smoothed estimate with the robust design over the uncertainty set Theta. (eq_2, eq_3)

## Assumptions

- The phase noise is a Wiener process with uncertain diffusion rate.
- Robustness is formulated as a minimax mean-square error.
- Homodyne-type detection of a single squeezed mode is assumed.

## Missing information

- Actual phase noise model and uncertain parameters
- Uncertainty set and robust smoother algorithm
- Measurement scheme such as homodyne detection and squeezing level
- Quantitative improvement metric
- Interval length T and detector efficiency are unspecified.
