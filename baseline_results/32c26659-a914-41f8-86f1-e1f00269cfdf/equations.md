# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Estimate a time-varying optical phase \phi(t), modelled as a stochastic phase-noise process with imprecisely known parameters, imprinted on a squeezed state of light and read out by continuous homodyne detection over a fixed interval [0,T]; the estimate is formed by a fixed-interval smoother (using all data on [0,T]) that is made robust to the parameter uncertainty, and its mean-square error is compared with that of the nominal (non-robust) smoother.

Scope: Smallest useful construction (chosen here as an assumption, since no experiment_scope was supplied): a single-mode, linearized (small-phase) continuous-variable model with an Ornstein-Uhlenbeck phase-noise process whose damping rate \lambda is uncertain within a known interval, a squeezed-state homodyne measurement model with reduced measurement-noise intensity, a nominal Kalman filter plus Rauch-Tung-Striebel fixed-interval smoother, and a worst-case (min-max) robust smoothing criterion over the uncertainty set. Tiny explicit instance: \lambda_0=1, \delta_\lambda=0.5, \kappa=1, |\alpha|=1, r=0.5, T=2, discretised with \Delta t=0.5 (N=4 samples). Outside scope: the paper's specific robust-smoother synthesis (e.g. guaranteed-cost/H_\infty Riccati equations), the exact phase-noise model and parameter values used in the paper, any adaptive (feedback) homodyne scheme, non-ideal squeezing/loss modelling, and the paper's numerical results. This is a continuous-variable metrology/estimation scheme, not a qubit gate-model algorithm; the quantum part is state preparation and homodyne readout, while filtering/smoothing is classical postprocessing.

## Symbols

- $\phi(t)$: true optical phase to be estimated (stochastic process); domain: \mathbb{R}, t\in[0,T]
- $\lambda$: damping (inverse correlation time) rate of the phase-noise process; uncertain; domain: \lambda>0
- $\lambda_0, \delta_\lambda$: nominal value of \lambda and bound on its uncertainty; domain: \lambda_0>0, 0\le\delta_\lambda<\lambda_0
- $\kappa$: diffusion strength of the phase noise; domain: \kappa>0
- $V(t), W(t)$: independent standard Wiener processes (process noise and measurement/shot noise); domain: \mathbb{R}
- $y(t)$: integrated homodyne photocurrent record; domain: \mathbb{R}
- $|\alpha|$: coherent amplitude of the probe beam; domain: |\alpha|>0
- $r$: squeezing parameter of the probe (phase quadrature squeezed); domain: r\ge 0
- $R_{\mathrm{sq}}$: measurement-noise intensity, reduced by squeezing; domain: R_{\mathrm{sq}}>0
- $\hat\phi_f(t), P_f(t)$: forward (Kalman filter) estimate and its error variance; domain: \mathbb{R}, P_f>0
- $\hat\phi_s(t)$: fixed-interval smoothed estimate conditioned on the whole record on [0,T]; domain: \mathbb{R}
- $\hat\phi_s^{\mathrm{rob}}(t)$: robust fixed-interval smoothed estimate; domain: \mathbb{R}
- $T$: length of the fixed estimation interval; domain: T>0
- $\Delta t, N$: discretisation step and number of samples in the tiny instance, T=N\Delta t; domain: \Delta t>0, N\in\mathbb{N}

## eq_1: Phase-noise model (Ornstein-Uhlenbeck)

$$
d\phi(t) = -\lambda\,\phi(t)\,dt + \sqrt{\kappa}\,dV(t)
$$

Linear Gaussian stochastic model for the optical phase; \lambda and \kappa are the 'parameters underlying the phase noise'.

Provenance: `standard_background`. A standard phase-noise model in continuous-time optical phase tracking; the abstract only says 'phase noise' with underlying parameters and does not specify the model.

Equation assumptions:

- Phase noise is a stationary OU process; the paper may use another model (e.g. Wiener process or higher-order noise).

## eq_2: Linearized homodyne measurement of a squeezed probe

$$
dy(t) = 2|\alpha|\,\phi(t)\,dt + \sqrt{R_{\mathrm{sq}}}\,dW(t), \qquad R_{\mathrm{sq}} \approx e^{-2r}
$$

Homodyne photocurrent in the small-phase (linearized) regime; squeezing of the measured quadrature reduces the shot-noise intensity from 1 (coherent state) to approximately e^{-2r}.

Provenance: `standard_background`. Standard linearized continuous homodyne model for phase estimation with squeezed light; the exact noise expression in the paper (including losses, anti-squeezing leakage, or adaptive local-oscillator feedback) is unknown.

Equation assumptions:

- Small-phase linearization sin(\phi)\approx\phi is valid.
- Ideal pure squeezing with no loss; no adaptive feedback of the local-oscillator phase.

## eq_3: Parametric uncertainty in the phase-noise model

$$
\lambda = \lambda_0 + \Delta_\lambda, \qquad |\Delta_\lambda| \le \delta_\lambda
$$

The true damping rate lies in a known interval around the nominal value; the robust smoother is designed over this set rather than for \lambda_0 alone.

Provenance: `abstract_inferred`. The abstract states that uncertainties are introduced into phase-noise parameters; a norm-bounded interval on \lambda is the simplest concrete realization. Which parameters are uncertain, and the uncertainty structure, are not stated.

Abstract evidence: uncertainties explicitly introduced in parameters underlying the phase noise

Equation assumptions:

- Only \lambda is uncertain and the uncertainty is a deterministic norm-bounded perturbation; \kappa could also be uncertain in the paper.

## eq_4: Nominal forward Kalman filter

$$
d\hat\phi_f = -\lambda_0\hat\phi_f\,dt + \frac{2|\alpha|P_f}{R_{\mathrm{sq}}}\big(dy - 2|\alpha|\hat\phi_f\,dt\big), \qquad \dot P_f = -2\lambda_0 P_f + \kappa - \frac{4|\alpha|^2 P_f^2}{R_{\mathrm{sq}}}
$$

Kalman-Bucy filter for eq_1-eq_2 with the nominal parameter \lambda_0; it is the forward pass of the fixed-interval smoother.

Provenance: `standard_background`. Standard Kalman-Bucy equations for a scalar linear Gaussian system; optimal only when the model is exact, which motivates the robust design in the abstract.

Equation assumptions:

- Initial conditions \hat\phi_f(0)=0, P_f(0)=\kappa/(2\lambda_0) (stationary prior).

## eq_5: Nominal fixed-interval (RTS) smoother, backward pass

$$
\frac{d\hat\phi_s}{dt} = -\lambda_0\hat\phi_s + \kappa\,P_f(t)^{-1}\big(\hat\phi_s - \hat\phi_f\big), \qquad \hat\phi_s(T)=\hat\phi_f(T)
$$

Rauch-Tung-Striebel backward recursion giving the estimate conditioned on the entire record y(s), 0\le s\le T.

Provenance: `standard_background`. Standard continuous-time RTS fixed-interval smoother; the abstract names a 'fixed-interval smoother' but does not specify which smoother form (RTS, two-filter/Mayne-Fraser) the paper uses.

Equation assumptions:

- RTS form chosen; the paper may use a two-filter form.

## eq_6: Robust smoothing criterion over the uncertainty set

$$
\hat\phi_s^{\mathrm{rob}} = \arg\min_{\hat\phi}\ \sup_{|\Delta_\lambda|\le\delta_\lambda}\ \mathbb{E}\big[(\phi(t)-\hat\phi(t))^2\big]
$$

Worst-case (guaranteed-cost/min-max) formulation: the robust smoother minimizes an upper bound on the error variance that holds for all admissible parameter perturbations.

Provenance: `abstract_inferred`. 'Robust ... designed with uncertainties explicitly introduced' implies a design criterion over the uncertainty set; a worst-case criterion is the generic meaning. The paper's actual synthesis (e.g. modified Riccati equations with uncertainty-dependent terms) is not available from the abstract and is NOT reconstructed here.

Abstract evidence: a robust fixed-interval smoother designed with uncertainties explicitly introduced in parameters underlying the phase noise

Equation assumptions:

- Min-max mean-square criterion; the specific robust-smoother equations are a missing paper contribution.

## eq_7: Performance metric for comparison

$$
\mathrm{MSE}[\hat\phi] = \frac{1}{T}\int_0^T \mathbb{E}\big[(\phi(t)-\hat\phi(t))^2\big]\,dt, \qquad \mathrm{MSE}[\hat\phi_s^{\mathrm{rob}}] < \mathrm{MSE}[\hat\phi_s] \ \text{(claimed, for } \Delta_\lambda\neq 0)
$$

Time-averaged mean-square estimation error; the claimed improvement is that the robust smoother has lower error than the nominal smoother when the true parameters deviate from nominal.

Provenance: `abstract_inferred`. The abstract claims improvement; mean-square error is the standard figure of merit for phase estimation. The magnitude and conditions of improvement are not given.

Abstract evidence: exhibits improvement when using a robust fixed-interval smoother

Equation assumptions:

- Improvement measured in mean-square error; the inequality is the paper's claim, not verified here.

## Registers

- optical probe mode: 1 bosonic mode (continuous-variable, not qubits) qubits; Carries the squeezed state whose phase quadrature is shifted by \phi(t) and read out by homodyne detection
- classical measurement record: N = T/\Delta t real samples (N=4 in the tiny instance) qubits; Stores homodyne increments \Delta y_k used by the forward filter and backward smoother

## Initial state

Probe mode in a phase-squeezed coherent state |\alpha, r\rangle = D(\alpha)S(r)|0\rangle with \alpha real and squeezing of the phase quadrature; estimator initialised at \hat\phi_f(0)=0 with stationary prior variance P_f(0)=\kappa/(2\lambda_0).

## Measurement

Continuous (time-resolved) homodyne detection of the phase quadrature of the squeezed probe, yielding the photocurrent increments dy(t) of eq_2; in the discretised tiny instance, N=4 Gaussian samples \Delta y_k with mean 2|\alpha|\phi_k\Delta t and variance R_{sq}\Delta t.

## Classical postprocessing

Forward Kalman filtering (eq_4) followed by backward fixed-interval smoothing (eq_5) for the nominal estimator; a robust fixed-interval smoother (eq_6) designed over the parameter uncertainty set for the robust estimator; evaluation and comparison of the time-averaged mean-square error (eq_7), e.g. by Monte Carlo over sample paths of \phi(t).

## Algorithm steps

1. Specify the nominal phase-noise model and the uncertainty set for its parameters (tiny instance: \lambda_0=1, \delta_\lambda=0.5, \kappa=1). (eq_1, eq_3)
2. Prepare the squeezed probe state and let the true phase process \phi(t) (with some \lambda in the uncertainty set) act on it. (eq_1)
3. Perform continuous homodyne detection of the phase quadrature over [0,T], recording y(t) (tiny instance: |\alpha|=1, r=0.5, R_{sq}=e^{-1}, T=2, \Delta t=0.5). (eq_2)
4. Run the nominal forward Kalman filter on the record to obtain \hat\phi_f(t), P_f(t). (eq_4)
5. Run the backward fixed-interval smoother to obtain the nominal smoothed estimate \hat\phi_s(t). (eq_5)
6. Design and run the robust fixed-interval smoother over the uncertainty set to obtain \hat\phi_s^{rob}(t) (specific synthesis equations missing from the abstract). (eq_6, eq_3)
7. Compare mean-square errors of nominal and robust smoothers for true \lambda\neq\lambda_0. (eq_7)

## Assumptions

- No experiment_scope was supplied; the single-mode OU-noise, linearized-homodyne construction and the tiny instance (\lambda_0=1, \delta_\lambda=0.5, \kappa=1, |\alpha|=1, r=0.5, T=2, \Delta t=0.5, N=4) are the reconstructor's choices, not paper content.
- The phase-noise model is Ornstein-Uhlenbeck and only its damping rate is uncertain.
- Small-phase linearization of the homodyne signal holds and squeezing is ideal and lossless.
- The robust smoother is characterised only by a generic worst-case criterion; the paper's actual robust-smoother equations are not reconstructed.
- The scheme is continuous-variable metrology with classical estimation; it is not a qubit gate-model algorithm, so any circuit-generation stage would need a bosonic-mode or Gaussian-state simulator rather than a qubit circuit.

## Missing information

- Exact phase-noise model and which of its parameters are treated as uncertain, and the uncertainty structure (interval, norm-bounded, stochastic).
- The specific robust fixed-interval smoother synthesis (e.g. guaranteed-cost or H_\infty Riccati equations, two-filter vs RTS form).
- Measurement model details: adaptive vs non-adaptive homodyne, squeezing level, optical loss and detection efficiency.
- Numerical parameter values, interval length T, and the quantitative size of the reported improvement.
