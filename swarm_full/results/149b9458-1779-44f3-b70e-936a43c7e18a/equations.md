# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Bootstrap characterization and control-model learning of a larger quantum simulator (e.g. a 50-qubit Ising simulator) using a small trusted quantum simulator (8 qubits), combining Bayesian inference, Lieb-Robinson bounds for compressed simulation, and interactive quantum learning, with Fisher information bounds motivating long evolution times.

Scope: Abstract-level reconstruction of the Hamiltonian-learning problem: Bayesian posterior over Hamiltonian parameters, Lieb-Robinson light-cone compression, and a Fisher information bound. Circuit, measurement and numerical details are not given in the abstract and are assumed generically.

## Symbols

- $H(\vec{x})$: Ising Hamiltonian of the device, parameterized by unknown parameters; domain: Hermitian operator on n qubits
- $\vec{x}$: unknown Hamiltonian parameters (couplings, fields); domain: R^d
- $t$: evolution time of an experiment; domain: t>0
- $D$: experimental data record; domain: measurement outcomes
- $v_{LR}$: Lieb-Robinson velocity, which depends on the uncertainty in the Hamiltonian (epistemic); domain: positive real
- $I(\vec{x})$: Fisher information about the parameters; domain: positive semidefinite matrix
- $N$: number of experiments; domain: positive integer

## eq_1: Bayes update

$$
P(\vec{x}\mid D)=\frac{P(D\mid \vec{x})P(\vec{x})}{\int P(D\mid \vec{x}')P(\vec{x}')\,d\vec{x}'}
$$

Posterior over Hamiltonian parameters given experimental data

Provenance: `abstract_inferred`. Bayesian inference is stated; the explicit Bayes rule is standard.

Abstract evidence: using Bayesian inference

## eq_2: Lieb-Robinson bound

$$
\|[A(t),B]\|\le c\,\|A\|\|B\|\,e^{-(d(A,B)-v_{LR}t)/\xi}
$$

Information propagation is confined to a light cone, allowing simulation of only a small sub-region

Provenance: `abstract_inferred`. Abstract names the bounds; the form shown is the generic standard version, not the paper's specific one.

Abstract evidence: Lieb-Robinson bounds

Equation assumptions:

- Generic form with constants c, xi; the paper's exact form is unknown

## eq_3: Cramer-Rao bound

$$
\mathrm{Cov}(\hat{x})\succeq \left(N\, I(\vec{x})\right)^{-1}
$$

Experiment count N is limited by the Fisher information; the abstract's claim is that I is small for short t, so N diverges

Provenance: `abstract_inferred`. Links Fisher information to the number of experiments needed; the Cramer-Rao bound is standard background and the paper's specific bounds are not given.

Abstract evidence: upper bounds for the Fisher information

Equation assumptions:

- Unbiased estimator

## Registers

- sim: 8 (trusted simulator, assumed) qubits; Small simulator that emulates the light-cone-restricted sub-region of the large device
- dev: 50 (device under characterization) qubits; Larger Ising simulator whose Hamiltonian parameters are learned

## Initial state

Assumed product state |0>^{\otimes n} (or a simple product state) on both the device and the simulator, per experiment.

## Measurement

Assumed: after evolution for time t, measure the qubits in the light cone of the chosen observable in a fixed local basis (e.g. computational), repeating for a number of shots to estimate outcome frequencies. The abstract does not specify the basis or shot count; only the ~750 kilobit total data budget is stated.

## Classical postprocessing

Use the outcome record as the likelihood input to the Bayesian update (eq_1), with the likelihood computed on the 8-qubit simulator restricted to the light cone (eq_2). Select the next experiment adaptively from the posterior and stop when the posterior covariance is small. The final estimate is the posterior mean, whose precision is bounded by eq_3.

## Algorithm steps

1. Draw a prior over Hamiltonian parameters x and choose an experiment (evolution time t, initial state, observable) adaptively from the current posterior. (eq_1)
2. Restrict the simulation to the light-cone region of the observable, using the Lieb-Robinson bound so that the 8-qubit simulator suffices to compute the likelihood. (eq_2)
3. Evolve the device under H(x) for time t and evolve the simulator under the candidate model for the same t. (no equation reference)
4. Update the posterior with the measured data, and repeat until the posterior is sufficiently narrow. Long t is preferred because the Fisher information shrinks at short t. (eq_1, eq_3)

## Assumptions

- Equation forms are generic background, not taken from the paper.
- Registers, initial state and steps are an assumed generic reconstruction.
- Product-state initialization and adaptive choice of t.
- Computational-basis measurement and posterior-mean estimator are assumed.
- The 8-qubit simulator is treated as trusted.

## Missing information

- Explicit Hamiltonian form (couplings, fields, geometry)
- Exact experiment design and circuits
- Exact rule for choosing experiments and light-cone size
- Exact measurement scheme, basis and shots per experiment
- Bayesian update algorithm details (e.g. sequential Monte Carlo)
- Paper's specific Fisher information bounds and how epistemic v_LR is computed
