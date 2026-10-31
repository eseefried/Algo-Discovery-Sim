# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Training a (restricted) Boltzmann machine requires gradients of the log-likelihood that involve expectation values under the Gibbs (Boltzmann) distribution of the model; sampling this distribution is classically hard in general (full BMs) or requires contrastive-divergence approximations (RBMs). The abstract claims a quantum method that trains deep restricted and full Boltzmann machines faster and with better optimization of the objective than classical methods, without known classical counterparts. The abstract gives no equations, so the mathematical content below is standard Boltzmann-machine background plus an assumed quantum Gibbs-state preparation construction consistent with (but not established by) the abstract.

Scope: One smallest useful construction chosen as an assumption (no experiment_scope was supplied): coherent preparation of an approximate Gibbs state of a tiny Boltzmann machine by quantum rejection sampling from a classically computable product (mean-field) distribution, followed by computational-basis measurement to estimate the model-expectation term <v_i h_j>_model of the training gradient. Tiny instance: n_v = 2 visible units, n_h = 1 hidden unit (3 state qubits), fixed weights w_11 = 1, w_21 = -1, biases a = b = 0, proposal distribution Q uniform (mean-field means mu = 1/2), so the state register is 3 qubits plus a b-bit ratio register and a 1-qubit flag. Outside scope: the data-clamped term of the gradient, deep/multi-layer and fully connected multi-layer models, the amplitude-estimation variant for the expectation values, the paper's complexity bounds, the claimed 'richer framework' and optimization-improvement results, and all numerical experiments.

## Symbols

- $v$: binary configuration of the visible units, v = (v_1,...,v_{n_v}); domain: \{0,1\}^{n_v}
- $h$: binary configuration of the hidden units, h = (h_1,...,h_{n_h}); domain: \{0,1\}^{n_h}
- $n_v, n_h$: number of visible and hidden units (tiny instance: n_v = 2, n_h = 1); domain: positive integers
- $w_{ij}, a_i, b_j$: visible-hidden coupling weights, visible biases, hidden biases; domain: real numbers
- $E(v,h)$: energy of joint configuration (v,h); domain: real numbers
- $Z$: partition function of the Boltzmann machine; domain: positive reals
- $P(v,h)$: Gibbs (Boltzmann) distribution of the model at unit temperature; domain: [0,1], sums to 1
- $Q(v,h)$: classically computable product proposal distribution (mean-field approximation) with single-unit means mu_i; domain: (0,1], sums to 1
- $\mu_i$: mean-field probability that unit i is on (tiny instance: mu_i = 1/2 for all units); domain: (0,1)
- $\kappa$: rejection-sampling constant bounding the likelihood ratio, kappa >= max_{v,h} P(v,h)/Q(v,h); domain: reals >= 1
- $O(w,a,b)$: training objective: average log-likelihood of the data under the model; domain: real numbers
- $\langle \cdot \rangle_{data}, \langle \cdot \rangle_{model}$: expectation with visible units clamped to training data (hidden units from P(h|v)) and expectation under the unclamped model distribution P(v,h); domain: real numbers in [0,1] for binary products
- $|\psi_Q\rangle$: coherent encoding (qsample) of the proposal distribution Q; domain: unit vector in (C^2)^{\otimes (n_v+n_h)}
- $|\psi_P\rangle$: coherent Gibbs state (qsample of P); domain: unit vector in (C^2)^{\otimes (n_v+n_h)}
- $b$: number of qubits of the fixed-point register holding the ratio P/(kappa Q); domain: positive integer (precision parameter)
- $N_s$: number of measured samples used to estimate a model expectation; domain: positive integer
- $\eta$: learning rate of the gradient-ascent update; domain: positive reals

## eq_energy: Restricted Boltzmann machine energy

$$
E(v,h) = -\sum_{i=1}^{n_v} a_i v_i - \sum_{j=1}^{n_h} b_j h_j - \sum_{i=1}^{n_v}\sum_{j=1}^{n_h} w_{ij} v_i h_j
$$

Energy of a joint visible/hidden configuration of an RBM (bipartite couplings only). A full Boltzmann machine adds visible-visible and hidden-hidden terms; the tiny instance uses a_i = b_j = 0, w_{11} = 1, w_{21} = -1.

Provenance: `standard_background`. Standard definition of the restricted Boltzmann machine energy function; the abstract names the model but states no formula.

Equation assumptions:

- Binary units in {0,1}; unit temperature.
- RBM (bipartite) form chosen as the tiny instance; the full-BM generalization only adds intra-layer quadratic terms.

## eq_gibbs: Gibbs distribution and partition function

$$
P(v,h) = \frac{e^{-E(v,h)}}{Z}, \qquad Z = \sum_{v \in \{0,1\}^{n_v}} \sum_{h \in \{0,1\}^{n_h}} e^{-E(v,h)}
$$

Exact model distribution over joint configurations. For the tiny instance Z = 7 + e + e^{-1}... (explicitly Z = sum over 8 configurations; Z = 6 + e + e^{-1} since only (v,h)=(1,0,1) and (0,1,1) have nonzero energy -1 and +1).

Provenance: `standard_background`. Standard definition of the Boltzmann machine model distribution; needed to define what the quantum sampler must approximate.

Equation assumptions:

- Unit temperature (inverse temperature absorbed into weights).

## eq_gradient: Log-likelihood gradient of the weights

$$
\frac{\partial O}{\partial w_{ij}} = \langle v_i h_j \rangle_{data} - \langle v_i h_j \rangle_{model}, \qquad \langle v_i h_j \rangle_{model} = \sum_{v,h} P(v,h)\, v_i h_j
$$

Exact gradient of the average log-likelihood with respect to a coupling weight; analogous expressions with v_i or h_j alone hold for the biases. The model term is the intractable quantity that the scoped quantum construction estimates by sampling.

Provenance: `standard_background`. Standard result for maximum-likelihood training of Boltzmann machines; the abstract's claim of improved optimization of 'the underlying objective function' is interpreted as referring to this log-likelihood objective (an inference, not stated explicitly).

Equation assumptions:

- Objective is the average log-likelihood of the training set; the abstract does not name the objective explicitly.

## eq_proposal_state: Coherent proposal (mean-field) state

$$
Q(v,h) = \prod_{i=1}^{n_v} \mu_i^{v_i}(1-\mu_i)^{1-v_i} \prod_{j=1}^{n_h} \nu_j^{h_j}(1-\nu_j)^{1-h_j}, \qquad |\psi_Q\rangle = \sum_{v,h} \sqrt{Q(v,h)}\,|v\rangle|h\rangle = \bigotimes_{i} R_y(2\arcsin\sqrt{\mu_i})|0\rangle \otimes \bigotimes_{j} R_y(2\arcsin\sqrt{\nu_j})|0\rangle
$$

Product proposal distribution and its exact preparation by single-qubit rotations. Register ordering is |v_1 ... v_{n_v}>|h_1 ... h_{n_h}>, bit value 1 meaning the unit is on. Tiny instance: all means 1/2, so |psi_Q> = H^{\otimes 3}|000> and Q = 1/8 for every configuration.

Provenance: `assumption`. A product (mean-field) proposal is a natural classically computable distribution from which a Gibbs qsample can be refined; this construction is proposed here as the smallest useful instance and is not stated in the abstract.

Equation assumptions:

- Proposal distribution is a product distribution with strictly positive probabilities so that P/Q is finite.
- Mean-field parameters mu_i, nu_j are obtained classically (tiny instance fixes them to 1/2).

## eq_rejection_rotation: Coherent rejection-sampling rotation

$$
|v,h\rangle|0\rangle_{b}|0\rangle_{f} \mapsto |v,h\rangle\,\Big|\tfrac{P(v,h)}{\kappa Q(v,h)}\Big\rangle_{b}\Big(\sqrt{1-\tfrac{P(v,h)}{\kappa Q(v,h)}}\,|0\rangle_{f} + \sqrt{\tfrac{P(v,h)}{\kappa Q(v,h)}}\,|1\rangle_{f}\Big), \qquad \kappa \ge \max_{v,h}\frac{P(v,h)}{Q(v,h)}
$$

A reversible arithmetic circuit writes a b-bit fixed-point approximation of the acceptance ratio into the ratio register (so the map is an approximation to precision 2^{-b}, not exact), and a controlled R_y rotation on the flag qubit encodes it as an amplitude. Because Z is unknown in general, in practice one uses e^{-E(v,h)}/(kappa' Q(v,h)) with kappa' >= max e^{-E}/Q, which equals the stated ratio with kappa = kappa'/Z. Tiny instance: kappa' = 8e, Q = 1/8, so the ratio is e^{-E(v,h)-1} in [e^{-2},1].

Provenance: `assumption`. Standard quantum rejection-sampling step, proposed here as the mechanism turning a proposal qsample into a Gibbs qsample; not stated in the abstract.

Equation assumptions:

- An upper bound kappa (or kappa') on the likelihood ratio is known classically; for the tiny instance it is computed exactly.
- Fixed-point arithmetic with b bits; rounding error of order 2^{-b} in the amplitudes is neglected in the stated equations.
- The ratio register is uncomputed after the controlled rotation (omitted from the formula).

## eq_postselect: Post-selected Gibbs state and success probability

$$
\big(I\otimes \langle 1|_f\big)\,U_{rej}\,|\psi_Q\rangle|0\rangle_f = \frac{1}{\sqrt{\kappa}}\sum_{v,h}\sqrt{P(v,h)}\,|v,h\rangle = \frac{1}{\sqrt{\kappa}}|\psi_P\rangle, \qquad p_{succ} = \frac{1}{\kappa}, \qquad N_{AA} = \Big\lfloor \frac{\pi}{4\arcsin(1/\sqrt{\kappa})} \Big\rfloor
$$

Measuring the flag in |1> (success probability exactly 1/kappa in the idealized infinite-precision case) leaves the state register in the coherent Gibbs state |psi_P>, whose computational-basis measurement statistics are exactly P(v,h). Optionally, amplitude amplification on the flag with about N_AA ~ O(sqrt(kappa)) Grover iterations raises the success probability to near 1, giving the quadratic speed-up over classical rejection sampling (expected 1/p_succ = kappa trials). For the tiny instance kappa = 8e/Z (approximately 2.49), so p_succ is approximately 0.40 and post-selection alone suffices.

Provenance: `assumption`. Follows algebraically from eq_proposal_state and eq_rejection_rotation; the amplitude-amplification iteration count is the standard Brassard-Hoyer-Mosca-Tapp formula. The abstract's claim that quantum computing 'reduces the time required to train' is consistent with, but does not establish, this particular speed-up mechanism.

Equation assumptions:

- Infinite-precision ratio register (b -> infinity) for exact equality; finite b gives an approximation to |psi_P>.
- Amplitude amplification is optional for the tiny instance and requires that 1/kappa be known to set N_AA.

## eq_estimator: Sample-mean estimator of the model expectation and update rule

$$
\widehat{\langle v_i h_j\rangle}_{model} = \frac{1}{N_s}\sum_{s=1}^{N_s} v_i^{(s)} h_j^{(s)}, \qquad \big|\widehat{\langle v_i h_j\rangle}_{model} - \langle v_i h_j\rangle_{model}\big| \le \epsilon \text{ w.p. } \ge 1-\delta \text{ if } N_s \ge \frac{\ln(2/\delta)}{2\epsilon^2}, \qquad w_{ij} \leftarrow w_{ij} + \eta\Big(\langle v_i h_j\rangle_{data} - \widehat{\langle v_i h_j\rangle}_{model}\Big)
$$

Each successful run yields one sample (v^{(s)},h^{(s)}) drawn (up to precision error) from P; the empirical mean estimates the model term with Hoeffding error epsilon; the weight is then updated by stochastic gradient ascent. This is an approximate (statistical) estimate, not an exact equality.

Provenance: `standard_background`. Hoeffding bound and gradient-ascent update are standard; they close the loop from quantum samples to a training step. An amplitude-estimation variant with O(1/epsilon) scaling is plausible but not reconstructed here.

Equation assumptions:

- Samples are independent and drawn from the ideal Gibbs distribution (precision and amplitude-amplification imperfections neglected).
- Data term <v_i h_j>_data is computed classically for the RBM instance via P(h_j = 1 | v) = sigma(b_j + sum_i w_{ij} v_i).

## Registers

- visible register |v>: n_v (tiny instance: 2) qubits; holds visible-unit configuration; qubit i encodes v_i with |1> = unit on; most significant / first qubit is v_1
- hidden register |h>: n_h (tiny instance: 1) qubits; holds hidden-unit configuration; follows the visible register in the tensor-product ordering |v>|h>
- ratio register: b (precision parameter, assumed) qubits; fixed-point work register holding P(v,h)/(kappa Q(v,h)) during the controlled rotation; uncomputed afterwards
- flag qubit f: 1 qubits; rejection-sampling acceptance flag; |1> marks acceptance and is the target of post-selection / amplitude amplification

## Initial state

|0\rangle^{\otimes n_v}|0\rangle^{\otimes n_h}|0\rangle^{\otimes b}|0\rangle_f (all registers in the all-zeros computational basis state); tiny instance: |000\rangle|0\rangle^{\otimes b}|0\rangle_f

## Measurement

Flag qubit measured in the computational basis (post-selection on outcome 1, or after amplitude amplification); then all n_v + n_h state qubits measured in the computational basis, yielding a bit string (v_1,...,v_{n_v},h_1,...,h_{n_h}) distributed (approximately, up to 2^{-b} precision effects) according to the Gibbs distribution P(v,h). For the tiny instance the 8 outcome frequencies should approach e^{-E(v,h)}/Z with Z = 6 + e + e^{-1}.

## Classical postprocessing

Discard runs with flag = 0 (if no amplitude amplification); compute empirical means of v_i h_j, v_i, h_j over accepted samples; compute data-clamped expectations classically for the RBM; form the gradient per eq_gradient and apply the update rule in eq_estimator; repeat for subsequent training iterations. Verification for the tiny instance: compare the accepted-sample histogram to the exactly enumerable P(v,h).

## Algorithm steps

1. Classical preprocessing: fix model parameters (w, a, b), compute the proposal (mean-field) means mu_i, nu_j and the rejection constant kappa' >= max_{v,h} e^{-E(v,h)}/Q(v,h). Tiny instance: mu = nu = 1/2, kappa' = 8e. (eq_energy, eq_gibbs, eq_proposal_state)
2. Prepare the coherent proposal state |psi_Q> on the visible and hidden registers with single-qubit R_y rotations (Hadamards for the tiny instance). (eq_proposal_state)
3. Coherently evaluate the energy and the acceptance ratio e^{-E(v,h)}/(kappa' Q(v,h)) into the b-bit ratio register using reversible fixed-point arithmetic. (eq_energy, eq_rejection_rotation)
4. Apply the controlled R_y rotation on the flag qubit with angle 2 arcsin sqrt(ratio), then uncompute the ratio register. (eq_rejection_rotation)
5. Either measure the flag and keep the run only if the outcome is 1 (success probability 1/kappa), or apply N_AA rounds of amplitude amplification on flag = 1 before measuring it; on success the state register holds (an approximation to) |psi_P>. (eq_postselect)
6. Measure the visible and hidden registers in the computational basis to obtain one sample (v,h) ~ P(v,h); repeat steps 2-6 N_s times. (eq_postselect, eq_estimator)
7. Classically form the sample-mean estimate of <v_i h_j>_model, combine with the classically computed data term, and update the weights by gradient ascent; iterate training epochs. (eq_gradient, eq_estimator)

## Assumptions

- No experiment_scope was given; the scope (quantum rejection sampling from a product proposal to approximate the Gibbs state of a 2-visible, 1-hidden RBM with w_11 = 1, w_21 = -1, zero biases) is a choice of this reconstruction, not a claim about the paper's experiments.
- The quantum method is assumed to be a coherent Gibbs-state preparation whose output is sampled to estimate the model term of the log-likelihood gradient; the abstract does not describe the mechanism.
- The training objective is assumed to be the data log-likelihood.
- Unit temperature, binary {0,1} units, and register ordering |v_1..v_{n_v}>|h_1..h_{n_h}> with |1> = on.
- A valid rejection constant kappa (or kappa') is available classically; for the tiny instance it is computed exactly by enumeration.
- Finite-precision arithmetic errors (2^{-b}) and amplitude-amplification imperfections are neglected in the exact-equality statements.
- The data-clamped term is computed classically (exact for RBMs); for full Boltzmann machines it would require the same quantum procedure with visible units clamped, which is outside scope.

## Missing information

- The abstract provides no equations; the specific quantum algorithm (proposal distribution, use of amplitude estimation versus sampling, how the rejection constant is bounded, treatment of the partition function) is not stated and has been replaced by an explicitly labelled assumed construction.
- Complexity bounds justifying the claimed reduction in training time are not reconstructable from the abstract.
- Definition and treatment of 'full Boltzmann machines' and 'multi-layer, fully connected models' (intra-layer couplings, layer-wise versus joint training) are not specified.
- The sense in which the quantum approach yields a 'richer and more comprehensive framework' and 'significant improvements in the optimization of the underlying objective function' is not specified; no numerical results or benchmarks are available.
- Precision parameter b, number of samples N_s, learning rate, and any error analysis linking sampling error to gradient quality are not given and are left symbolic.
- Whether the paper trains on the exact gradient (via amplitude estimation) or stochastic samples, and how the data-dependent term is handled quantumly for full BMs, is unknown.
