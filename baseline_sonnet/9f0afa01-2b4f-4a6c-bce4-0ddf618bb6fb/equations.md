# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Training of (restricted) Boltzmann machines by maximizing the log-likelihood, where quantum methods are claimed to reduce training time and improve optimization. The abstract gives no explicit equations, so only the standard classical objective and gradient are reconstructed as background.

Scope: Smallest useful construction: a tiny RBM (e.g. 2 visible, 2 hidden units) with the standard energy function, Gibbs distribution, log-likelihood and gradient, plus a quantum-state encoding of the Gibbs distribution as a labelled assumption. The paper's actual quantum training algorithm, its state preparation, gradient estimation and the full Boltzmann machine and multi-layer extensions are outside this scope.

## Symbols

- $v$: visible unit configuration; domain: {0,1}^{n_v}
- $h$: hidden unit configuration; domain: {0,1}^{n_h}
- $W$: visible-hidden weight matrix; domain: R^{n_v x n_h}
- $b,d$: visible and hidden biases; domain: R^{n_v}, R^{n_h}
- $Z$: partition function; domain: positive real
- $E(v,h)$: energy function; domain: real
- $O_{ML}$: average log-likelihood objective over training data; domain: real
- $\rho_{\mathrm{Gibbs}}$: Gibbs distribution encoded as a quantum state; domain: normalized state

## eq_1: RBM energy

$$
E(v,h) = -\sum_i b_i v_i - \sum_j d_j h_j - \sum_{i,j} v_i W_{ij} h_j
$$

Energy function of a restricted Boltzmann machine.

Provenance: `standard_background`. The abstract names the RBM but gives no equation; this is the standard form.

Equation assumptions:

- Binary units
- Bipartite connectivity

## eq_2: Gibbs distribution

$$
P(v,h)=\frac{e^{-E(v,h)}}{Z},\quad Z=\sum_{v,h}e^{-E(v,h)}
$$

Joint probability of the model; the marginal is P(v)=sum_h P(v,h).

Provenance: `standard_background`. Standard definition.

Equation assumptions:

- Temperature set to 1

## eq_3: Log-likelihood objective

$$
O_{ML}=\frac{1}{N}\sum_{x\in\text{data}}\log\sum_h P(x,h)
$$

Objective function to be maximized in training.

Provenance: `standard_background`. The abstract mentions optimizing the underlying objective function without specifying it; maximum likelihood is the standard choice.

Equation assumptions:

- Maximum likelihood is the objective

## eq_4: Weight gradient

$$
\frac{\partial O_{ML}}{\partial W_{ij}}=\langle v_i h_j\rangle_{\text{data}}-\langle v_i h_j\rangle_{\text{model}}
$$

Gradient as the difference between data and model correlations; the model term is the costly part that quantum sampling would target.

Provenance: `standard_background`. Standard Boltzmann machine gradient.

Equation assumptions:

- Data expectation is taken with clamped visible units

## eq_5: Gibbs state encoding

$$
|\psi\rangle=\sum_{v,h}\sqrt{P(v,h)}\,|v\rangle|h\rangle
$$

A coherent encoding of the model distribution; measuring in the computational basis samples from P.

Provenance: `assumption`. Proposed construction for sampling the model term. The abstract does not state how the paper prepares states.

Equation assumptions:

- Preparation of this state is available; its method is not specified

## Registers

- visible: n_v (assume 2) qubits; visible units v
- hidden: n_h (assume 2) qubits; hidden units h

## Measurement

Assumed: computational-basis measurement of both registers to sample (v,h) from P, estimating the model expectation.

## Classical postprocessing

Assumed: average samples to estimate the correlations, form the gradient and update W, b, d by gradient ascent.

## Algorithm steps

1. Define the tiny RBM energy and Gibbs distribution. (eq_1, eq_2)
2. Define the log-likelihood objective and its gradient. (eq_3, eq_4)
3. Assumed: prepare the Gibbs-state encoding and sample it to estimate the model correlations in the gradient. (eq_5)

## Assumptions

- Binary RBM with 2 visible and 2 hidden units as the tiny instance
- Maximum-likelihood objective
- The quantum algorithm itself is not specified in the abstract; eq_5 is a placeholder construction

## Missing information

- Actual quantum state preparation or sampling method
- Complexity or speedup claims in formal form
- Gradient estimation procedure
- Full Boltzmann machine and multi-layer model constructions
- Objective function details beyond the generic one
