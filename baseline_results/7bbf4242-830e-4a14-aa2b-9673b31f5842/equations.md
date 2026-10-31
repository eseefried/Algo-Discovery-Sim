# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Estimate an unknown phase \phi of a single-qubit phase gate U_\phi using a total budget of N gate applications distributed over M qubits prepared in a product state (generalized Kitaev phase estimation), and quantify the Bayesian mean square error of the resulting estimator.

Scope: One finite construction: M qubits each prepared in |+>, qubit j receives n_j applications of U_\phi with \sum_j n_j = N, each qubit is measured independently after a local phase shift \theta_j and a Hadamard, and \phi is estimated by Bayesian postprocessing with a flat prior. Tiny explicit instance (assumption): M=2, N=3, (n_1,n_2)=(1,2), (\theta_1,\theta_2)=(0,\pi/2). Outside scope: derivation of the optimal distribution {n_j}, the proof of near-optimality against the Bayesian bound, the loss analysis, comparison with entangled strategies, and the alternative resource quantification for Shor's algorithm.

## Symbols

- $\phi$: Unknown phase to be estimated; domain: [0, 2\pi)
- $U_\phi$: Single-qubit phase gate; domain: 2x2 unitary, U_\phi = \mathrm{diag}(1, e^{i\phi})
- $N$: Total number of phase gate applications (resource); domain: positive integer
- $M$: Number of qubits in the product state; domain: positive integer
- $n_j$: Number of phase gate applications on qubit j; domain: non-negative integers, j=1..M, \sum_j n_j = N
- $\theta_j$: Local measurement phase shift on qubit j (0 for X-basis, \pi/2 for Y-basis); domain: [0,2\pi)
- $x_j$: Measurement outcome on qubit j; domain: {0,1}
- $\tilde\phi(x)$: Estimator of \phi from the outcome string x=(x_1,...,x_M); domain: [0,2\pi)
- $\Delta^2$: Bayesian average cost (mean square error or its periodic variant) of the estimator; domain: non-negative real

## eq_1: Product probe state after distributed phase gates

$$
|\Psi_\phi\rangle = \bigotimes_{j=1}^{M} U_\phi^{n_j}|+\rangle = \bigotimes_{j=1}^{M} \frac{1}{\sqrt{2}}\left(|0\rangle + e^{i n_j \phi}|1\rangle\right), \qquad \sum_{j=1}^{M} n_j = N
$$

Each of the M qubits starts in |+> and accumulates phase n_j\phi after n_j applications of the phase gate; the distribution {n_j} is arbitrary subject to the total budget N. Standard Kitaev corresponds to n_j = 2^{j-1}.

Provenance: `abstract_inferred`. Direct formalization of 'N phase gates distributed arbitrarily over M qubits in a product state'; the |+> initial state and diag(1,e^{i\phi}) gate are the standard Kitaev choice, not stated in the abstract.

Abstract evidence: $N$ phase gates, acting on $M$ qubits prepared in a product state, may be distributed in an arbitrary way

Equation assumptions:

- Initial product state is |+>^{\otimes M}
- Phase gate acts as diag(1, e^{i\phi}) on each qubit

## eq_2: Local measurement statistics

$$
p(x_j \mid \phi; n_j, \theta_j) = \frac{1}{2}\left[1 + (-1)^{x_j}\cos(n_j\phi + \theta_j)\right], \qquad p(x\mid\phi) = \prod_{j=1}^{M} p(x_j\mid\phi; n_j,\theta_j)
$$

Probability of outcome x_j when qubit j is measured after applying the phase shift diag(1,e^{i\theta_j}) followed by a Hadamard; outcomes on different qubits are independent because the state is a product.

Provenance: `standard_background`. Born rule applied to eq_1 with the standard Kitaev X/Y-type measurement; exact equality.

Equation assumptions:

- Measurements are local, non-adaptive, fixed phases \theta_j
- No losses or noise

## eq_3: Bayesian estimation and cost

$$
p(\phi\mid x) = \frac{p(x\mid\phi)}{\int_0^{2\pi} p(x\mid\phi')\,\frac{d\phi'}{2\pi}}, \qquad \Delta^2 = \int_0^{2\pi}\frac{d\phi}{2\pi}\sum_{x\in\{0,1\}^M} p(x\mid\phi)\, C\big(\tilde\phi(x),\phi\big)
$$

Flat-prior Bayesian posterior and average cost of the estimator over outcomes and prior. The cost C is the squared error (\tilde\phi-\phi)^2 or its periodic variant 4\sin^2((\tilde\phi-\phi)/2); which one the paper uses is not stated in the abstract.

Provenance: `standard_background`. Standard Bayesian phase-estimation framework consistent with the abstract's reference to 'mean square error' and 'the fundamental Bayesian estimation bound'.

Equation assumptions:

- Flat prior on [0,2\pi)
- Cost function form (MSE vs. periodic 4\sin^2) is a choice

## eq_4: Error scaling claims

$$
\Delta^2_{\mathrm{Kitaev}} \sim \frac{c_1}{N}, \qquad \min_{\{n_j\},\{\theta_j\},\tilde\phi} \Delta^2 \sim \frac{c_2}{N^{2}}
$$

Asymptotic (not exact) scaling: the standard Kitaev distribution yields mean square error scaling as 1/N, while the optimal distribution over the product state achieves Heisenberg 1/N^2 scaling. Constants c_1, c_2 are not given in the abstract.

Provenance: `abstract_explicit`. Stated directly in the abstract as asymptotic scaling statements.

Abstract evidence: Unlike the standard algorithm, where the mean square error scales as $1/N$, the optimal generalizations offer the Heisenberg $1/N^{2}$ error scaling

Equation assumptions:

- Scaling is asymptotic in N; prefactors unknown

## eq_5: Fundamental Bayesian bound for N gate uses (reference)

$$
\Delta^2 \;\gtrsim\; \frac{\pi^{2}}{N^{2}} \quad (N\to\infty)
$$

Known asymptotic optimal Bayesian cost (periodic cost, flat prior) achievable with an optimal entangled N-gate probe; the abstract claims the optimal product-state generalization comes very close to this bound.

Provenance: `standard_background`. Recalled background result for optimal Bayesian single-phase estimation with N uses; exact constant depends on the cost function and is asymptotic, not an abstract-sourced value.

Equation assumptions:

- Periodic cost 4\sin^2((\tilde\phi-\phi)/2) and flat prior
- Asymptotic regime

## eq_6: Tiny explicit instance

$$
M=2,\; N=3,\; (n_1,n_2)=(1,2),\; (\theta_1,\theta_2)=(0,\tfrac{\pi}{2}): \quad p(x_1,x_2\mid\phi)=\tfrac{1}{4}\left[1+(-1)^{x_1}\cos\phi\right]\left[1-(-1)^{x_2}\sin 2\phi\right]
$$

Smallest nontrivial distribution of N=3 gates over M=2 qubits with one X-basis and one Y-basis measurement; the likelihood follows from eq_2.

Provenance: `assumption`. Chosen as a minimal concrete instance for circuit generation; not specified by the abstract.

Equation assumptions:

- Specific choice of N, M, {n_j}, {\theta_j}

## Registers

- q: M (instance: 2) qubits; Probe qubits, qubit j receives n_j phase-gate applications and is measured locally

## Initial state

|+\rangle^{\otimes M} = H^{\otimes M}|0\rangle^{\otimes M}

## Measurement

Computational-basis measurement of every qubit after the local phase shift \theta_j and Hadamard; outcome string x \in \{0,1\}^M with likelihood given by eq_2.

## Classical postprocessing

Compute the flat-prior posterior p(\phi|x) from eq_3, output the Bayes estimator \tilde\phi(x) (e.g. the circular mean of the posterior for the periodic cost), and evaluate the average cost \Delta^2; compare scaling in N against eq_4 and eq_5.

## Algorithm steps

1. Prepare each of the M qubits in |+> via Hadamard on |0>. (eq_1)
2. Apply the phase gate U_\phi n_j times to qubit j, with \sum_j n_j = N (instance: 1 application on qubit 1, 2 on qubit 2). (eq_1, eq_6)
3. Apply the local phase shift diag(1,e^{i\theta_j}) and a Hadamard to each qubit, then measure in the computational basis. (eq_2, eq_6)
4. Repeat the experiment or use the single-shot outcome string in a Bayesian update with flat prior and compute the estimator minimizing the average cost. (eq_3, eq_4, eq_5)

## Assumptions

- Initial product state |+>^{\otimes M} and phase gate diag(1,e^{i\phi}) as in standard Kitaev phase estimation
- Measurements are local, non-adaptive, with fixed phases \theta_j in {0, \pi/2}
- Flat prior and a squared-error or periodic squared-error cost function
- Lossless, noiseless setting
- Tiny instance M=2, N=3, (n_1,n_2)=(1,2), (\theta_1,\theta_2)=(0,\pi/2) chosen by the reconstruction, not the paper

## Missing information

- The optimal distribution {n_j} (and M) achieving 1/N^2 scaling and the prefactor c_2
- Whether the paper's measurements are adaptive and which cost function (MSE vs. periodic) defines 'mean square error'
- The loss model and the resulting performance comparison with entanglement-based strategies
- The alternative resource quantification relevant to Shor's algorithm under which standard Kitaev is optimal
- Numerical values quantifying 'very close to the fundamental Bayesian estimation bound'
