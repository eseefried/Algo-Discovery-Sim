# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Prepare the Gibbs distribution P(v,h)=exp(-E(v,h))/Z of a small Boltzmann machine by mean-field-product-state preparation plus an ancilla rotation with postselection, and read out <v_i h_j> to form the gradient dO/dw_ij = <v_i h_j>_data - <v_i h_j>_model (Wiebe-Kapoor-Svore style).

Scope: One tiny instance: 1 visible and 1 hidden unit (or 2+1), a single weight w, biases b_v,b_h, a single ancilla, postselected exactly on the statevector, then <v h>_model from ZZ parity, and <v h>_data by clamping v. Excluded: QRAM data oracle, full amplitude-estimation phase-estimation register, the paper's exact error analysis, deep multi-layer models beyond a small fully connected example, and any speedup verification.

## Symbols

- $x_i$: binary unit value of visible/hidden unit i, x_i in {0,1}; qubit state |x_i>; domain: {0,1}
- $E(x)$: Boltzmann machine energy; domain: real
- $b_i, w_ij$: biases and weights; domain: real, bounded
- $Z$: partition function sum_x exp(-E(x)); domain: positive real
- $Q(x)$: mean-field product distribution with Q(x)=prod_i q_i^{x_i}(1-q_i)^{1-x_i}; domain: [0,1]
- $\theta_i$: Ry angle with q_i=sin^2(\theta_i/2); domain: [0,\pi]
- $\kappa$: constant with exp(-E(x)) <= kappa Q(x) for all x; domain: >=1 real
- $\epsilon$: target additive error on expectation; domain: (0,1)
- $P_succ$: ancilla postselection probability; domain: [0,1]

## eq_1: Energy

$$
E(x)=-\sum_i b_i x_i-\sum_{i<j} w_{ij} x_i x_j
$$

Boltzmann machine energy over all visible and hidden units (full connectivity allowed); the sketch writes it with the sum over all pairs.

Provenance: `standard_background`. Standard definition; the abstract names Boltzmann machines but gives no formula.

Equation assumptions:

- No separate constant offset; the pair sum counts each pair once

## eq_2: Gibbs and mean-field distributions

$$
P(x)=\frac{e^{-E(x)}}{Z},\quad Q(x)=\prod_i \sin^{2\!\left(\frac{\theta_i}{2}\right)x_i}\ldots
$$

Replace with Q(x)=prod_i q_i^{x_i}(1-q_i)^{1-x_i}, q_i=sin^2(theta_i/2), prepared by Ry(theta_i)|0> on each qubit.

Provenance: `standard_background`. Standard mean-field and Gibbs definitions. Ry(theta)|0>=cos(theta/2)|0>+sin(theta/2)|1> gives P(1)=sin^2(theta/2). Note the Q formula in this latex is a typographical simplification; use the product of q_i factors.

Equation assumptions:

- q_i are mean-field marginals computed classically and strictly inside (0,1)

## eq_3: Ancilla rotation and postselection

$$
\text{state}=\sum_x \sqrt{Q(x)}|x\rangle\left(\sqrt{\tfrac{e^{-E(x)}}{\kappa Q(x)}}|1\rangle+\sqrt{1-\tfrac{e^{-E(x)}}{\kappa Q(x)}}|0\rangle\right),\; P_{succ}=\frac{Z}{\kappa}
$$

Ancilla Ry angle 2 arcsin(sqrt(e^{-E}/(kappa Q))) controlled on x, computed from classical values for tiny instances. Post-selecting ancilla=1 yields sum_x sqrt(P(x))|x>. Because Q is normalized, P_succ=Z/kappa; this equals Z/(kappa Z_Q) in the sketch's convention if Q is unnormalized.

Provenance: `assumption`. Sketch construction; the abstract does not give the rotation. Implementable for small n as a multiplexed Ry (uniformly controlled rotation) using standard gates, since the rotation angle is a function of x computed classically; the energy-into-phase route is an alternative that needs an energy register.

Equation assumptions:

- exp(-E)/(kappa Q)<=1 for all x
- Angle table is built from known b,w (the model parameters are known to the builder, not a hidden black box)

## eq_4: Model expectation

$$
\langle v_i h_j\rangle_{model}=\sum_x P(x)x_i x_j=\frac{1-\langle Z_i\rangle-\langle Z_j\rangle+\langle Z_iZ_j\rangle}{4}
$$

Model correlator read from postselected Gibbs state via Z expectations (Z|x>=(-1)^x|x>).

Provenance: `standard_background`. Algebraic identity x_i x_j=(1-Z_i)(1-Z_j)/4.

Equation assumptions:

- Postselection exact

## eq_5: Data expectation with clamped visible units

$$
\langle v_i h_j\rangle_{data}=\frac{1}{N}\sum_{k=1}^{N} x^{(k)}_i\,\langle h_j\rangle_{P(h|v=x^{(k)})}
$$

Visible qubits set to training vector x^(k) by X gates, hidden units Gibbs-prepared conditioned on v (same construction with v fixed, energy restricted to h), averaged over data classically (looped) in the small case.

Provenance: `abstract_inferred`. Training gradient requires data and model terms; the exact data-term circuit is inferred from the sketch, not stated in the abstract.

Abstract evidence: leads to significant improvements in the optimization of the underlying objective function

Equation assumptions:

- Small training set looped over classically; no QRAM

## eq_6: Gradient and update

$$
\frac{\partial O}{\partial w_{ij}}=\langle v_i h_j\rangle_{data}-\langle v_i h_j\rangle_{model},\quad w_{ij}\leftarrow w_{ij}+\eta\,\frac{\partial O}{\partial w_{ij}}
$$

Log-likelihood gradient and classical gradient ascent update with learning rate eta.

Provenance: `standard_background`. Standard Boltzmann machine maximum-likelihood gradient.

Equation assumptions:

- O is average log-likelihood
- eta chosen classically

## Registers

- vis: n_v (e.g. 1 or 2) qubits; visible units, qubit index i is bit i (little-endian)
- hid: n_h (e.g. 1) qubits; hidden units
- anc: 1 qubits; rotation ancilla; postselect on |1>
- ae: optional, 0 in minimal scope qubits; amplitude estimation register; omitted in the exact-statevector scope

## Initial state

All qubits |0>; apply Ry(theta_i) on each vis/hid qubit to make the mean-field state sum_x sqrt(Q(x))|x>.

## Measurement

Measure vis and hid qubits and the ancilla in the Z basis; keep shots with ancilla=1. Qiskit little-endian: bit i of the counts key (read from the right) is qubit i.

## Classical postprocessing

Estimate <x_i x_j> from postselected counts or from the identity in eq_4; average data terms; compute gradient and update weights.

## Algorithm steps

1. Classically compute mean-field marginals q_i and theta_i=2 arcsin(sqrt(q_i)); choose kappa >= max_x e^{-E}/Q. (eq_1, eq_2)
2. Prepare the mean-field product state with Ry rotations. (eq_2)
3. Apply the x-controlled ancilla rotation (multiplexed Ry from the classical angle table) so ancilla=1 has amplitude sqrt(e^{-E}/(kappa Q)). (eq_3)
4. Postselect ancilla=1 (exact projection on the statevector, or conditioned counts; optionally Grover amplification of the ancilla-1 subspace) to get the Gibbs state. (eq_3)
5. Read the model correlator via Z and ZZ expectations; repeat with v clamped to each training vector for the data term. (eq_4, eq_5)
6. Classical gradient and weight update. (eq_6)

## Assumptions

- Smallest construction: 1-2 visible and 1 hidden unit with a known tiny weight set
- Rotation angles are computed classically from known parameters, which is legitimate here as the machine parameters are not a hidden oracle
- Postselection is simulated exactly
- Amplitude estimation replaced by direct readout; the O(sqrt(kappa)/epsilon) scaling is not tested
- Weights bounded so e^{-E}<=kappa Q

## Missing information

- The abstract gives no equations; all constructions come from the sketch and background
- Exact energy-oracle or phase-based implementation of the paper
- Exact amplitude estimation and Grover circuit details and error bounds
- QRAM data access scheme
- Handling of the biased gradient for general deep models
