# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Sparse Hamiltonian simulation: given a d-sparse Hamiltonian H on n qubits (dimension N=2^n) with largest entry magnitude \|H\|_{\max}, evolution time t, and error tolerance \epsilon, implement an operation \tilde U with \|\tilde U - e^{-iHt}\| \le \epsilon using a number of queries and 2-qubit gates that is nearly linear in \tau = t d \|H\|_{\max} and logarithmic in 1/\epsilon, by applying a linear combination of Szegedy-type quantum-walk steps with Bessel-function coefficients.

Scope: One smallest useful construction (chosen as an assumption since no experiment_scope was supplied): a single-segment truncated Jacobi–Anger linear combination of unitaries (LCU) over powers W^{-k}, |k|\le K, of a Szegedy/Berry–Childs quantum walk W for H, implemented with a coefficient-preparation unitary B and a controlled-walk-power selector, with post-selection on the control register (one round of oblivious amplitude amplification noted as optional background). Tiny explicit instance: n=1, H = \sigma_x (d=1, \|H\|_{\max}=1), t=1 so \tau=1, target \epsilon \approx 10^{-3}, truncation K=4 (9 Bessel coefficients, 4-qubit control register). Outside scope: the paper's exact definition and circuit for the walk state-preparation isometry T (oracle query model), the segmentation of long evolutions into pieces with amplification, the detailed query/gate-complexity accounting, the error-of-approximation proofs, and the new \Omega(\tau) lower bound.

## Symbols

- $H$: d-sparse Hermitian Hamiltonian on n qubits, dimension N=2^n; domain: Hermitian matrix in \mathbb{C}^{N\times N} with at most d nonzero entries per row/column
- $d$: sparsity (max number of nonzero entries per row); domain: positive integer
- $\|H\|_{\max}$: magnitude of the largest entry of H, \max_{j,l}|H_{jl}|; domain: positive real
- $t$: evolution time; domain: positive real
- $\tau$: combined parameter t d \|H\|_{\max}; domain: positive real
- $\epsilon$: allowed spectral-norm error of the simulation; domain: real in (0,1)
- $\lambda, |\lambda\rangle$: eigenvalue and eigenvector of H; domain: \lambda \in [-d\|H\|_{\max}, d\|H\|_{\max}] (since \|H\| \le d\|H\|_{\max})
- $T$: state-preparation isometry of the Szegedy/Berry–Childs walk, mapping the system register into the two-register walk space; domain: isometry \mathbb{C}^N \to \mathbb{C}^N\otimes\mathbb{C}^{2N}
- $S$: swap of the two system-sized registers of the walk space; domain: unitary
- $W$: quantum walk step, W = i S (2 T T^\dagger - I) (standard Berry–Childs convention; phase convention is a choice); domain: unitary on the walk space
- $\theta_\lambda$: walk eigenphase, \theta_\lambda = \arcsin(\lambda/(d\|H\|_{\max})); domain: real in [-\pi/2,\pi/2]
- $J_k(z)$: Bessel function of the first kind of integer order k; domain: k \in \mathbb{Z}, z \in \mathbb{R}
- $K$: truncation order of the Bessel/Jacobi–Anger series; domain: positive integer
- $s$: LCU normalization, s = \sum_{k=-K}^{K}|J_k(\tau)|; domain: positive real
- $|k\rangle$: control-register basis state encoding index k \in \{-K,\dots,K\} as the unsigned integer k+K in \lceil\log_2(2K+1)\rceil qubits (big-endian); domain: computational basis of control register

## eq_1: Combined cost parameter

$$
\tau = t\, d\, \|H\|_{\max}
$$

The single parameter in which the algorithm's complexity is nearly linear: the product of evolution time, sparsity, and largest entry magnitude.

Provenance: `abstract_explicit`. Directly stated definition of \tau in the abstract.

Abstract evidence: nearly linear in the product $\tau$ of the evolution time, the sparsity, and the magnitude of the largest entry of the Hamiltonian

## eq_2: Quantum walk eigenphases (Szegedy/Berry–Childs walk)

$$
W\,|\mu_{\pm}^{\lambda}\rangle = \mu_\pm^{\lambda}\,|\mu_\pm^{\lambda}\rangle,\qquad \mu_\pm^{\lambda} = \pm e^{\pm i\theta_\lambda},\qquad \sin\theta_\lambda = \frac{\lambda}{d\,\|H\|_{\max}},\qquad |\mu_\pm^{\lambda}\rangle \in \mathrm{span}\{T|\lambda\rangle,\ S\,T|\lambda\rangle\}
$$

For each eigenpair (\lambda,|\lambda\rangle) of H, the walk W acts on the 2-dimensional invariant subspace spanned by T|\lambda\rangle and S T|\lambda\rangle with eigenvalues whose phases encode \lambda via an arcsin.

Provenance: `standard_background`. Standard spectral correspondence of the discrete-time quantum walk used for sparse Hamiltonian simulation (Childs 2010; Berry–Childs 2012); the abstract names the walk approach but does not state this relation. Requires the walk's state preparation T to normalize entries by d\|H\|_{\max} (or a value X \ge d\|H\|_{\max}).

Equation assumptions:

- T is the Berry–Childs state-preparation isometry built from sparse-access oracles with normalization d\|H\|_{\max}; its explicit circuit is outside scope.
- Overall phase convention of W chosen so eigenvalues are exactly \pm e^{\pm i\theta_\lambda}; other conventions shift all eigenphases by a known constant.

## eq_3: Jacobi–Anger expansion

$$
e^{-i z \sin\theta} = \sum_{k=-\infty}^{\infty} J_k(z)\, e^{-ik\theta},\qquad J_{-k}(z) = (-1)^k J_k(z)
$$

Fourier–Bessel expansion that converts the exponential of a sine of the walk eigenphase into a sum over integer powers of the eigenphase, i.e. into powers of the walk operator.

Provenance: `standard_background`. Classical identity for Bessel functions of the first kind; it is the source of the Bessel-function coefficients mentioned in the abstract.

## eq_4: Truncated Bessel linear combination of walk steps

$$
V_K := \sum_{k=-K}^{K} J_k(\tau)\, W^{-k},\qquad V_K\,|\mu^{\lambda}_{\pm}\rangle = \Big(\sum_{|k|\le K} J_k(\tau) e^{-ik\phi_\pm}\Big)|\mu^{\lambda}_{\pm}\rangle \approx e^{-i\tau\sin\theta_\lambda}|\mu^{\lambda}_{\pm}\rangle = e^{-i\lambda t}|\mu^{\lambda}_{\pm}\rangle,\quad \phi_+ = \theta_\lambda,\ \phi_- = \pi-\theta_\lambda,\qquad \Big\|V_K - \sum_{k\in\mathbb{Z}} J_k(\tau)W^{-k}\Big\| \le \sum_{|k|>K}|J_k(\tau)| \le \epsilon \ \text{for}\ K = O\!\Big(\tau + \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}\Big)
$$

Combining eq_1–eq_3: on each walk eigenvector the truncated Bessel-weighted sum of walk powers reproduces the desired phase e^{-i\lambda t}, since \tau\sin\theta_\lambda = \lambda t and \sin(\pi-\theta_\lambda)=\sin\theta_\lambda handles both eigenvalue branches. The truncation error is the Bessel tail, which decays super-exponentially once K exceeds \tau, giving the logarithmic error dependence.

Provenance: `abstract_inferred`. The abstract states that the algorithm is a linear combination of walk steps with Bessel coefficients and has log(1/\epsilon), ~linear-in-\tau complexity; the specific form follows from substituting the walk eigenphases (eq_2) into the Jacobi–Anger identity (eq_3) with z=\tau. The tail bound form is standard Bessel asymptotics (|J_k(\tau)| \le (\tau/2)^{|k|}/|k|!), not quoted from the paper; the exact constants are unknown to me.

Abstract evidence: By implementing a linear combination of quantum walk steps with coefficients given by Bessel functions, our algorithm’s complexity (as measured by the number of queries and 2-qubit gates) is logarithmic in the inverse error, and nearly linear in the product $\tau$

Equation assumptions:

- Sign convention W^{-k} (equivalently \sum_k (-1)^k J_k(\tau) W^k) matches eq_2's eigenphase convention; with the opposite convention use W^{k}.
- The approximation is only guaranteed on the walk subspace T(\mathbb{C}^N) \oplus S T(\mathbb{C}^N); the final state is returned to the system register by T^\dagger.

## eq_5: LCU implementation via coefficient preparation and controlled walk powers

$$
B|0\rangle = \frac{1}{\sqrt{s}}\sum_{k=-K}^{K}\sqrt{|J_k(\tau)|}\,|k\rangle,\quad s=\sum_{k=-K}^{K}|J_k(\tau)|,\quad \mathrm{SEL} = \sum_{k=-K}^{K} |k\rangle\langle k| \otimes \mathrm{sgn}\big(J_k(\tau)\big)\, W^{-k},\qquad (B^\dagger\otimes I)\,\mathrm{SEL}\,(B\otimes I)\,|0\rangle|\Phi\rangle = \frac{1}{s}\,|0\rangle\, V_K|\Phi\rangle + |\Phi^{\perp}\rangle,\quad (|0\rangle\langle 0|\otimes I)|\Phi^{\perp}\rangle = 0
$$

Standard LCU circuit: prepare the (unsigned) Bessel amplitudes on a control register, apply walk powers controlled on the index (absorbing coefficient signs into the selector), uncompute the preparation; the |0\rangle control branch carries V_K/s.

Provenance: `standard_background`. Generic LCU construction (Childs–Wiebe 2012) applied to the coefficients and unitaries of eq_4; the abstract says the linear combination is implemented but gives no circuit. W^{-k} controlled on |k\rangle can be built from O(K) controlled applications of W or W^{-1} (or by a binary-powering structure), which is where the O(\tau+\log(1/\epsilon)) query count arises.

Equation assumptions:

- Index k is stored as the unsigned integer k+K in \lceil\log_2(2K+1)\rceil control qubits; unused basis states have zero amplitude.
- Sign of J_k(\tau) is applied as a controlled phase (-1) within SEL; J_{-k}=(-1)^kJ_k makes these signs simple.

## eq_6: Post-selection success and oblivious amplitude amplification (optional)

$$
P(\text{control}=0) = \frac{\|V_K|\Phi\rangle\|^2}{s^2} \approx \frac{1}{s^2},\qquad \text{if } s = 2:\ \ -\,\mathcal{W}\,R\,\mathcal{W}^\dagger R\,\mathcal{W}\,|0\rangle|\Phi\rangle \approx |0\rangle V_K|\Phi\rangle,\quad \mathcal{W} = (B^\dagger\otimes I)\mathrm{SEL}(B\otimes I),\ R = I - 2|0\rangle\langle 0|\otimes I
$$

Without amplification the LCU succeeds with probability about 1/s^2 on measuring the control in |0\rangle. Because V_K is close to a unitary on the walk subspace, oblivious amplitude amplification can boost this; when the normalization s equals 2 (achieved by splitting the evolution into short segments), a single amplification round suffices up to O(\epsilon) error.

Provenance: `standard_background`. Oblivious amplitude amplification (Berry et al. 2014 BQP-complete/fractional-query line of work) is the standard tool making LCU-based simulation deterministic; the abstract does not state the segmentation or amplification schedule, so the s=2 choice is recalled background, not paper evidence.

Equation assumptions:

- V_K is \epsilon-close to unitary on the relevant subspace (follows from eq_4).
- The paper's actual segment length and amplification details are not reconstructed here; for the tiny instance, plain post-selection is used instead.

## Registers

- ctrl: \lceil\log_2(2K+1)\rceil (4 qubits for the tiny instance with K=4) qubits; LCU control register holding Bessel coefficient index k encoded as k+K
- sys: n (1 qubit for the tiny instance) qubits; system register carrying the input state |\psi\rangle and, after T^\dagger, the output e^{-iHt}|\psi\rangle
- walk_aux: n+1 (symbolic; depends on the T construction) qubits; second system-sized register plus one ancilla of the Berry–Childs walk state preparation T; together with sys forms the walk space on which W and S act

## Initial state

|0\rangle_{\mathrm{ctrl}} \otimes T|\psi\rangle_{\mathrm{sys},\mathrm{walk\_aux}}, where |\psi\rangle is the system state to be evolved (tiny instance: |\psi\rangle=|0\rangle, n=1) and T is the walk state-preparation isometry (walk_aux initialized to |0\rangle before T).

## Measurement

Measure the control register in the computational basis and accept on outcome 0 (success probability \approx 1/s^2 \approx 0.27 for the tiny instance without amplification; \approx 1 after oblivious amplitude amplification with s=2). Optionally verify walk_aux returns to |0\rangle. The system register then holds an \epsilon-approximation of e^{-iHt}|\psi\rangle, on which the observable of interest is measured (for the tiny instance, compare against the exact e^{-i\sigma_x}|0\rangle = \cos(1)|0\rangle - i\sin(1)|1\rangle).

## Classical postprocessing

Discard runs where the control register is not 0 (or, with amplification, treat the output as deterministic). For validation of the tiny instance, estimate the fidelity of the post-selected system state with the exact e^{-iHt}|\psi\rangle, expecting infidelity on the order of the Bessel tail bound (\lesssim 10^{-3} for K=4, \tau=1).

## Algorithm steps

1. Classical precomputation: set \tau = t d \|H\|_{\max} (tiny instance: \tau = 1), choose truncation K so that \sum_{|k|>K}|J_k(\tau)| \le \epsilon (tiny instance: K=4, Bessel values J_0(1)\approx0.765, J_1\approx0.440, J_2\approx0.115, J_3\approx0.0196, J_4\approx0.0025, s\approx1.92), and compute the coefficient-preparation unitary B. (eq_1, eq_3, eq_4, eq_5)
2. Map the system state into the walk space by applying the state-preparation isometry T (requires sparse-access oracles to H). (eq_2)
3. Apply B to the control register to prepare \sqrt{|J_k(\tau)|/s} amplitudes. (eq_5)
4. Apply SEL: for each control value k, apply \mathrm{sgn}(J_k(\tau)) W^{-k} to the walk space (controlled walk steps built from T, S, and the reflection 2TT^\dagger - I). (eq_2, eq_5)
5. Apply B^\dagger to the control register; the |0\rangle branch now holds V_K T|\psi\rangle / s \approx e^{-iHt} embedded in the walk space. (eq_4, eq_5)
6. Optionally apply oblivious amplitude amplification (background; requires segmenting so that s=2). For the tiny instance, skip and post-select instead. (eq_6)
7. Apply T^\dagger to return the walk-space state to the system register (walk_aux returns to |0\rangle up to O(\epsilon)). (eq_2, eq_4)

## Assumptions

- No experiment_scope was supplied; the single-segment LCU with post-selection and the tiny instance (n=1, H=\sigma_x, d=1, \|H\|_{\max}=1, t=1, \tau=1, K=4) are chosen by the reconstructing agent, not taken from the abstract.
- The quantum walk W is the Berry–Childs/Szegedy walk with the eigenphase relation of eq_2 and normalization d\|H\|_{\max}; its state-preparation circuit T (from sparse-access oracles) is treated as a black box.
- Sign/phase conventions of W and of the index direction (W^{-k} vs W^{k}) are chosen consistently with eq_2; other conventions change only bookkeeping.
- Bessel tail bound and K = O(\tau + \log(1/\epsilon)/\log\log(1/\epsilon)) are recalled background asymptotics; the paper's precise constants are not reproduced.
- Segmentation of long evolutions into pieces with s=2 and one round of oblivious amplitude amplification is recalled as standard background, not reconstructed from the abstract.

## Missing information

- Exact definition and gate/query implementation of the walk state-preparation isometry T and the walk operator W used in the paper.
- The paper's precise choice of truncation order K, segment length, and amplification procedure, and the resulting constants in the O(\tau \log(\tau/\epsilon)/\log\log(\tau/\epsilon))-type bound.
- Rigorous error analysis showing the total simulation error is \le \epsilon (including effects of the walk's non-system subspace and amplification).
- Gate-complexity accounting for implementing controlled W^{-k} for all k and for the coefficient-preparation unitary B.
- Statement and proof of the new lower bound showing no algorithm can have sublinear dependence on \tau.
- Comparison details with the fractional-query simulation approach mentioned in the abstract.
