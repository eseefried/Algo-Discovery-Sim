# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Learn the parameters theta=(J_j,h_j) of a 1D transverse-field Ising chain by Bayesian (sequential Monte Carlo) inference, where each experiment's likelihood is computed on a Lieb-Robinson light-cone patch of at most 8 qubits simulated exactly. Scoped to one tiny instance: an 8-qubit chain standing in for the device, with a patch of at most 8 qubits, one Bayesian update per experiment.

Scope: Single-round likelihood circuit on a patch of at most 8 qubits (product state |+>^m, exact or Trotterized evolution, measure one qubit in Z or X), plus the classical particle-filter update, resampling or Liu-West step, and an expected-information-gain experiment choice. Out of scope: the 50-qubit device, the actual epistemic velocity formula, interactive quantum learning details, pulse-level control optimization, the Fisher information bounds, and the 750 kb data figure.

## Symbols

- $\theta=(J_j,h_j)$: unknown Hamiltonian couplings and fields; domain: real vectors
- $n$: number of qubits in the chain (patch size m<=8); domain: positive integers
- $t$: evolution time of an experiment; domain: positive reals
- $q$: measured qubit index; domain: {1,...,n}
- $v(\sigma)$: Lieb-Robinson velocity, depending on posterior uncertainty sigma; domain: positive reals
- $r$: light-cone radius; domain: nonnegative integers
- $w_k$: weight of particle k; domain: [0,1], sum w_k = 1
- $d$: measurement outcome; domain: {0,1}
- $B$: measurement basis (Z or X); domain: {Z,X}

## eq_1: Ising Hamiltonian

$$
H(\theta)=\sum_j J_j Z_j Z_{j+1}+\sum_j h_j X_j
$$

1D Ising model with unknown couplings and fields

Provenance: `assumption`. Abstract names an Ising model simulator; the exact form is taken from the task sketch.

Equation assumptions:

- nearest-neighbour 1D chain
- open boundaries

## eq_2: Light-cone restriction

$$
r=\lceil v(\sigma)\,t\rceil+\text{margin},\quad \text{patch}=\{j:|j-q|\le r\}
$$

Qubits within radius r of the measured qubit are simulated; v depends on the posterior spread, so it is epistemic

Provenance: `abstract_inferred`. The abstract says the velocity depends on the uncertainty. The functional form v(sigma) and the margin are not given.

Abstract evidence: the Lieb–Robinson velocity is epistemic for our protocol, meaning that information propagates at a rate that depends on the uncertainty in the system Hamiltonian

Equation assumptions:

- v(sigma) is a monotone function of posterior spread, unspecified
- patch size capped at 8

## eq_3: Likelihood

$$
P(d\mid\theta,t,q,B)=\langle\psi_0|e^{iH_{patch}(\theta)t}\,\Pi^{B}_{d,q}\,e^{-iH_{patch}(\theta)t}|\psi_0\rangle,\ |\psi_0\rangle=|+\rangle^{\otimes m}
$$

Born-rule outcome probability on the patch, computed per particle by statevector simulation

Provenance: `standard_background`. Standard quantum measurement; the patch approximates the full chain within the Lieb-Robinson tolerance.

Equation assumptions:

- negligible noise
- ideal projective measurement
- truncation error is controlled by the margin

## eq_4: Bayes update

$$
w_k'\propto w_k\,P(d\mid\theta_k,t,q,B),\quad \sum_k w_k'=1
$$

Sequential Monte Carlo reweighting after each experiment

Provenance: `abstract_inferred`. Bayesian inference is stated; the particle-filter form is an assumed implementation.

Abstract evidence: using Bayesian inference in concert with Lieb-Robinson bounds

Equation assumptions:

- particle representation of the posterior

## eq_5: Liu-West resampling

$$
\theta_k'=a\,\theta_{i(k)}+(1-a)\bar\theta+h\,\xi,\ \xi\sim\mathcal N(0,\Sigma),\ h^2=1-a^2
$$

Resample particles and apply a kernel shift to preserve the posterior mean and covariance

Provenance: `standard_background`. Common SMC practice, used when the effective sample size is low.

Equation assumptions:

- a close to 1, such as 0.98
- triggered when the effective sample size falls below a threshold

## eq_6: Expected information gain

$$
(t,q,B)^*=\arg\max\ \left[H\!\left(\sum_k w_kP(d|\theta_k)\right)-\sum_k w_kH\big(P(d|\theta_k)\big)\right]
$$

Adaptive experiment design by maximizing mutual information between the outcome and theta

Provenance: `assumption`. The sketch proposes maximizing information gain; the abstract only mentions interactive learning, so this is an assumed criterion.

Equation assumptions:

- candidate set of finitely many (t,q,B) with t not small

## Registers

- patch: m<=8 qubits; qubits of the light-cone patch simulated, initialized to |+>

## Initial state

|+>^{\otimes m} on the patch, prepared by H gates on |0>^m

## Measurement

Single-qubit projective measurement of qubit q in the Z basis, or in the X basis via H before measurement; Qiskit little-endian ordering, so measure(i,i) maps bit i to the last-character position.

## Classical postprocessing

Particle-filter Bayesian inference: reweighting, effective-sample-size check, Liu-West resampling, posterior mean and variance, stopping test. Control design on the learned theta is out of scope.

## Algorithm steps

1. Initialize particles theta_k from a prior with weights 1/N. (eq_1)
2. Choose an experiment (t,q,B), e.g. by expected information gain. (eq_6)
3. Compute the light-cone radius from the current posterior spread and extract the patch. (eq_2)
4. For each particle, build the circuit: H on all patch qubits, then exact or Trotter evolution (RZZ with angle 2J_j dt, RX with angle 2h_j dt), then basis rotation and measurement or exact probability, giving the likelihood. (eq_1, eq_3)
5. Take the device outcome d and update the weights, resampling with Liu-West when the effective sample size is low. (eq_4, eq_5)
6. Repeat until the posterior variance is below a threshold. (eq_4, eq_6)

## Assumptions

- Experiment scope chosen by me: 1D open chain, n<=8, product initial state |+>^n
- Trotter angles: RZZ(2 J dt) and RX(2 h dt), with Qiskit sign conventions to be checked
- Noise negligible, simulator trusted
- The form of v(sigma) is unspecified
- Hidden parameters of the target device are simulated by the runner, not by an opaque gate

## Missing information

- Form of the epistemic Lieb-Robinson velocity and margin
- Prior distribution and particle count
- Experiment design heuristic actually used
- Details of the interactive quantum learning step
- Control optimization procedure
- Time-step choices
