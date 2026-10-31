# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantum-assisted training of (deep) restricted and full Boltzmann machines: use quantum computing to reduce training time and improve optimization of the underlying objective function, including models lacking efficient classical training.

Scope: Abstract-level reconstruction of the training objective and a standard background gradient; no quantum circuit details are given in the abstract, so only a small finite Boltzmann machine example is scoped.

## Symbols

- $v,h$: visible and hidden binary units; domain: {0,1}^n x {0,1}^m
- $W,b,d$: weights, visible biases, hidden biases; domain: real parameters
- $E(v,h)$: Boltzmann machine energy function; domain: real
- $Z$: partition function; domain: positive real
- $O_{ML}$: average log-likelihood objective; domain: real

## eq_1: RBM energy

$$
E(v,h)=-\sum_i b_i v_i-\sum_j d_j h_j-\sum_{i,j} W_{ij} v_i h_j
$$

Energy of a restricted Boltzmann machine configuration.

Provenance: `standard_background`. Standard RBM definition; the abstract names restricted Boltzmann machines but gives no formulas.

Equation assumptions:

- Binary units

## eq_2: Gibbs distribution

$$
P(v,h)=e^{-E(v,h)}/Z,\quad Z=\sum_{v,h}e^{-E(v,h)}
$$

Model distribution defined by the energy.

Provenance: `standard_background`. Standard definition needed to state the training objective.

## eq_3: Likelihood gradient

$$
\partial O_{ML}/\partial W_{ij}=\langle v_i h_j\rangle_{data}-\langle v_i h_j\rangle_{model}
$$

Gradient of average log-likelihood; the model expectation is the hard term quantum sampling would target.

Provenance: `standard_background`. Standard background for the optimization of the underlying objective function.

Equation assumptions:

- Maximum-likelihood training

## Registers

- vis: n qubits; visible units of the small example RBM
- hid: m qubits; hidden units of the small example RBM
- anc: unknown qubits; assumed ancilla for Gibbs-state preparation or amplitude/rotation encoding

## Initial state

Assumed: all registers in |0>; generic initial state, not given in the abstract.

## Measurement

Assumed: measure vis and hid in the computational basis after successful ancilla post-selection (ancilla=1), giving samples (v,h) from P(v,h). Repeat to estimate <v_i h_j>_model.

## Classical postprocessing

Assumed: average v_i h_j over samples for the model term, compute the data term classically from training data with sampled/conditional hidden units, form the gradient difference per eq_3, and update W (and b,d) by gradient ascent.

## Algorithm steps

1. Assumed: apply Hadamards to vis and hid to create a uniform superposition over configurations (v,h). (no equation reference)
2. Assumed: encode the energy E(v,h) in an ancilla via controlled rotations, with amplitude proportional to e^{-E/2}. (eq_1)
3. Assumed: post-select or amplitude-amplify to approximately prepare the Gibbs state with probabilities P(v,h), whose normalization is Z. (eq_2)
4. Assumed: use the prepared state to estimate the model expectation in the gradient; the data term is computed classically. (eq_3)

## Assumptions

- Equations are standard background, not paper-specific.
- Circuit plan and measurement are a generic assumed Gibbs-state-sampling sketch, not taken from the abstract.
- Measurement is computational-basis sampling after ancilla post-selection.

## Missing information

- Quantum algorithm, circuits, and measurement details are not in the abstract.
- Ancilla size and exact state-preparation method unknown.
- Abstract gives no quantitative speedup, full-BM or deep-model details.
- Paper's actual measurement and gradient-estimation procedure is not in the abstract.
