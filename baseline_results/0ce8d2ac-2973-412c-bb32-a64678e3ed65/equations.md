# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Characterize (learn the Hamiltonian parameters of) a large quantum device whose dynamics cannot be classically simulated, using a smaller trusted quantum simulator to evaluate Bayesian likelihoods for local measurements. The abstract describes a bootstrapping protocol combining Bayesian inference, Lieb-Robinson bounds (to truncate the large system to a small local patch), and interactive quantum learning; it reports numerics for an 8-qubit Ising simulator calibrating a 50-qubit Ising simulator and gives Fisher-information upper bounds showing short-time experiments are inefficient.

Scope: ONE smallest useful instance (chosen as an assumption): an unknown 1D transverse-field Ising chain on N=4 qubits with open boundaries; a trusted n=2 qubit simulator emulates the local patch {1,2} via a truncated Hamiltonian H_S(x). The unknown parameters are x=(J_1,h_1) (edge coupling and edge field); all other couplings/fields are assumed known. Each experiment prepares |00> on the patch, evolves under H_S(x) for time t, and measures Z on qubit 1; the outcome probability is used as the likelihood in a Bayes update (sequential Monte Carlo / particle filter). A Lieb-Robinson bound provides the truncation error controlling how large t may be for a patch of linear size l. Outside scope: the full 8-qubit-to-50-qubit numerical result and its 750 kbit data budget, the precise 'epistemic Lieb-Robinson velocity' statement, the paper's specific Fisher-information bounds, the interactive (inverse-evolution/swap) variant, control-model learning, and adaptive experiment design heuristics.

## Symbols

- $N$: number of qubits in the large (untrusted) Ising device; domain: positive integer; N=4 in the scoped instance
- $n$: number of qubits in the small trusted simulator / truncated patch; domain: positive integer with n<N; n=2 in the scoped instance
- $x$: vector of unknown Hamiltonian parameters to be learned; domain: \mathbb{R}^{2}, x=(J_1,h_1) in the scoped instance
- $J_i$: nearest-neighbour ZZ coupling between sites i and i+1; domain: real; i=1,\dots,N-1
- $h_i$: transverse field on site i; domain: real; i=1,\dots,N
- $H(x)$: full Hamiltonian of the N-qubit device; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes N}
- $H_S(x)$: truncated Hamiltonian restricted to the patch S of n qubits containing the measured site; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $t$: evolution time of an experiment; domain: t>0
- $d$: measurement outcome of Z on qubit 1; domain: d\in\{0,1\}
- $\Pi_d$: projector onto outcome d of qubit 1, \Pi_d=|d\rangle\langle d|_1\otimes I; domain: projector on the patch Hilbert space
- $P(x)$: prior distribution over parameters; domain: probability density on \mathbb{R}^2
- $D$: record of all experimental outcomes (d_1,t_1),\dots,(d_M,t_M); domain: finite sequence
- $v,\ \xi,\ C$: Lieb-Robinson velocity, decay length and constant for the local Hamiltonian; domain: positive reals (depend on bounded interaction strengths)
- $\ell$: graph distance from the measured site to the boundary of the patch S; domain: non-negative integer; \ell=1 in the scoped instance
- $I(x;t)$: Fisher information about a parameter from one experiment of duration t; domain: non-negative real

## eq_1: Transverse-field Ising Hamiltonian of the large device

$$
H(x)=\sum_{i=1}^{N-1} J_i\, Z_i Z_{i+1}+\sum_{i=1}^{N} h_i\, X_i,\qquad N=4
$$

Open-chain Ising model with ZZ couplings and transverse fields; qubit i is the i-th tensor factor (qubit 1 leftmost).

Provenance: `assumption`. The abstract says only 'Ising model simulator'; the transverse-field 1D open-chain form and N=4 are chosen as the smallest useful instance.

Equation assumptions:

- 1D open chain
- transverse-field Ising form (ZZ + X terms)
- N=4 sites

## eq_2: Truncated (compressed) patch Hamiltonian on the small simulator

$$
H_S(x)=J_1 Z_1 Z_2 + h_1 X_1 + h_2 X_2,\qquad S=\{1,2\},\ n=2
$$

Restriction of H(x) to the patch S by dropping all terms not fully supported on S; this is what the trusted n-qubit simulator implements.

Provenance: `abstract_inferred`. Using a small simulator for a larger device requires simulating a reduced model; truncation to a local patch is the natural compression consistent with the abstract's use of Lieb-Robinson bounds. The specific truncation rule is an assumption.

Abstract evidence: uses small quantum simulators to efficiently characterize and learn control models for larger devices

Equation assumptions:

- terms are dropped by simple support restriction (no boundary corrections)
- only J_1 and h_1 are unknown; h_2 is known

## eq_3: Likelihood of a local measurement from the compressed simulation

$$
P(d\mid x,t)\approx \mathrm{Tr}\!\left[\Pi_d\, e^{-iH_S(x)t}\,|00\rangle\langle 00|\, e^{iH_S(x)t}\right],\qquad \Pi_d=|d\rangle\langle d|_1\otimes I_2
$$

The probability of observing outcome d on qubit 1 after time t under the true device H(x) is approximated by the same quantity computed on the truncated patch; the approximation error is bounded by eq_4.

Provenance: `standard_background`. Born rule for a projective Z measurement after unitary evolution; the approximation sign reflects truncation rather than exact equality.

Equation assumptions:

- initial state |00> on the patch (device initialised to |0>^{\otimes N})
- ideal state preparation and measurement

## eq_4: Lieb-Robinson truncation error bound

$$
\left|\mathrm{Tr}[\Pi_d\, e^{-iH t}\rho e^{iH t}]-\mathrm{Tr}[\Pi_d\, e^{-iH_S t}\rho e^{iH_S t}]\right|\le C\, e^{(v t-\ell)/\xi},\qquad \ell=\mathrm{dist}(\{1\},\partial S)
$$

Standard Lieb-Robinson-type statement: the influence of Hamiltonian terms outside the patch on an observable localized at site 1 is exponentially small until the light cone v t reaches the patch boundary at distance l. Controls the admissible t for a given patch size.

Provenance: `standard_background`. Recalled form of Lieb-Robinson locality bounds for local Hamiltonians with bounded interaction strength; the abstract invokes Lieb-Robinson bounds but does not state this inequality or its constants.

Equation assumptions:

- bounded interaction strengths |J_i|,|h_i|\le J_{max} so that v,\xi,C exist
- rho is a product state

## eq_5: Bayesian update (sequential, particle approximation)

$$
P(x\mid d_k,t_k,D_{k-1})=\frac{P(d_k\mid x,t_k)\,P(x\mid D_{k-1})}{\int P(d_k\mid x',t_k)\,P(x'\mid D_{k-1})\,dx'},\qquad P(x\mid D_{k-1})\approx\sum_{j=1}^{N_p} w_j\,\delta(x-x_j)
$$

After each experiment the posterior over (J_1,h_1) is updated with the likelihood from eq_3; a particle filter with N_p weighted particles represents the distribution, with the estimate taken as the posterior mean.

Provenance: `abstract_inferred`. Bayes' rule follows directly from the stated use of Bayesian inference; the sequential Monte Carlo particle representation is a standard implementation choice, not stated in the abstract.

Abstract evidence: using Bayesian inference in concert with Lieb-Robinson bounds

Equation assumptions:

- uniform prior on a bounded box, e.g. J_1,h_1\in[0,1]
- N_p particles with resampling (details unspecified)

## eq_6: Short-time Fisher information scaling (background form)

$$
I(x;t)\le 4t^2\,\big\|\partial_x H\big\|^2 \;\Rightarrow\; M_{\mathrm{experiments}}\gtrsim \frac{1}{\epsilon^2\, I(x;t)}=\Omega\!\left(\frac{1}{\epsilon^2 t^2}\right)
$$

Generic quantum Fisher information bound for a parameter entering a Hamiltonian evolution of duration t, implying (via Cramer-Rao) that the number of experiments to reach precision epsilon diverges as t -> 0. The paper's specific bounds are not available and may differ in form.

Provenance: `standard_background`. The abstract claims Fisher-information upper bounds showing divergence of experiment count as duration shrinks; this recalled background bound exhibits that qualitative behaviour but is not the paper's stated result.

Equation assumptions:

- parameter enters linearly in H
- single-parameter Cramer-Rao scaling used for the experiment count

## Registers

- sim: 2 qubits; Trusted small-simulator register implementing the truncated patch Hamiltonian H_S(x); qubit 1 is the measured edge site, qubit 2 its neighbour (qubit 1 = leftmost tensor factor).
- device: 4 qubits; Large untrusted Ising device whose edge-site Z statistics are collected experimentally (not simulated in the scoped construction; it is the data source).

## Initial state

|00\rangle on the sim register (and |0\rangle^{\otimes 4} on the device register at the start of each experiment).

## Measurement

Single-qubit computational-basis (Z) measurement on qubit 1 of the sim register (and on qubit 1 of the device), outcome d in {0,1}; repeated shots estimate P(d | x_j, t).

## Classical postprocessing

Particle-filter Bayesian update of weights w_j <- w_j P(d|x_j,t) followed by normalisation and resampling; estimate x-hat = sum_j w_j x_j and posterior covariance as the uncertainty. Stopping when the posterior variance falls below a chosen threshold.

## Algorithm steps

1. Fix the model class: the device is assumed to be the N=4 open transverse-field Ising chain of eq_1 with unknown x=(J_1,h_1) and known h_2,h_3,h_4,J_2,J_3; choose a uniform prior on a bounded box and initialise N_p particles. (eq_1, eq_5)
2. Choose an experiment time t such that the Lieb-Robinson light cone does not exit the patch, i.e. v t < l (with slack so that the error in eq_4 is below the target tolerance); this is the compression condition that allows the n=2 simulator to stand in for the N=4 device. (eq_4)
3. Run the experiment on the device: prepare |0>^{\otimes 4}, evolve for time t under the true H(x), measure Z on qubit 1, record outcome d. (eq_1, eq_3)
4. For each particle x_j, run the trusted simulator: prepare |00>, evolve under H_S(x_j) for time t (eq_2), measure Z on qubit 1 repeatedly to estimate P(d | x_j, t) per eq_3. (eq_2, eq_3)
5. Update the particle weights with Bayes' rule (eq_5), resample if the effective sample size is low, and report the posterior mean as the current estimate of (J_1,h_1). Repeat steps 2-5; prefer longer t (within the eq_4 constraint) because short-t experiments carry little Fisher information (eq_6). (eq_5, eq_6)

## Assumptions

- No experiment_scope was provided; the smallest useful construction (N=4 device, n=2 patch, two unknown edge parameters) is a chosen instance, not from the abstract.
- Transverse-field Ising form with open boundaries and bounded couplings.
- Truncation is by simple support restriction to the patch; no boundary-correction terms.
- Non-interactive (likelihood-only) quantum Hamiltonian learning is used in scope; the abstract's 'interactive quantum learning methods' are not reconstructed.
- Ideal preparation, evolution and measurement on both simulator and device.
- Likelihoods on the simulator are estimated from finite shots; sampling error is ignored in the equations.

## Missing information

- The paper's actual bootstrapping protocol: how the 8-qubit simulator is iteratively used to calibrate progressively larger patches of the 50-qubit device, and how learned parameters are transferred.
- Precise statement and formula of the 'epistemic Lieb-Robinson velocity' (dependence of the effective velocity on Hamiltonian uncertainty).
- The paper's explicit Fisher-information upper bounds and the regime in which experiment count diverges.
- Interactive learning details (e.g., inverse evolution on the simulator, swap/overlap measurements) and how they are combined with truncation.
- Experiment-design heuristic for choosing t and measured sites, particle numbers, resampling rules, and how the ~750 kilobit data budget was counted.
- Control-model learning component (how calibrated Hamiltonian parameters are turned into control of the 50-qubit simulator).
