# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantify how imperfect (systematically biased and randomly fluctuating) gate operations degrade Shor's order-finding/factoring algorithm, and determine, for a given N, an error threshold below which the algorithm still succeeds with acceptable probability.

Scope: Single smallest useful instance: order finding for N=15 with base a=7 (order r=4), using an n=4 qubit work register and a t=8 qubit control register, with the standard QFT-based period-finding circuit. Imperfections are modeled only on the single-qubit rotation gates of the (inverse) QFT as (i) a systematic fractional over-rotation and (ii) independent Gaussian random phase errors; the figure of merit is the probability of measuring an outcome that yields the correct order via continued fractions. Outside scope: the paper's actual error model and which gates it perturbs, its 'combined error' category, its specific threshold values and scaling with N, imperfections in the modular-exponentiation network, and any decoherence model.

## Symbols

- $N$: Odd composite integer to be factored; domain: Positive integer, instance N=15
- $a$: Randomly chosen base coprime to N; domain: Integer with 1<a<N, gcd(a,N)=1; instance a=7
- $r$: Multiplicative order of a modulo N; domain: Positive integer; instance r=4
- $n$: Number of work-register qubits, n=\lceil \log_2 N \rceil; domain: Positive integer; instance n=4
- $t$: Number of control (phase-estimation) qubits; domain: Positive integer; instance t=2n=8
- $Q$: Control-register dimension Q=2^t; domain: Positive integer; instance Q=256
- $\theta_k$: Ideal rotation angle of controlled-phase gate R_k in the QFT, \theta_k=2\pi/2^k; domain: Real, k=2,...,t
- $\epsilon$: Systematic (fixed, reproducible) fractional over-rotation of every gate angle; domain: Real
- $\delta_{j}$: Random phase error on the j-th gate application; domain: Real, i.i.d. Gaussian with zero mean and standard deviation \sigma
- $\sigma$: Random-error strength (standard deviation of \delta_j); domain: Non-negative real
- $P_{\mathrm{succ}}$: Probability that the measured control-register outcome yields the correct order r by continued fractions; domain: Real in [0,1]
- $\sigma_{\mathrm{th}}$: Error threshold: largest random-error strength for which P_succ stays above a chosen fraction of its ideal value; domain: Non-negative real

## eq_1: Ideal order-finding state before inverse QFT

$$
\frac{1}{\sqrt{Q}}\sum_{x=0}^{Q-1}|x\rangle_{c}\,|a^{x} \bmod N\rangle_{w},\quad Q=2^{t}
$$

State of the control and work registers after Hadamards on the control register and the controlled modular-exponentiation network, with x encoded in binary (qubit 0 = least significant bit).

Provenance: `standard_background`. Standard Shor order-finding construction; the abstract names Shor's algorithm but does not state this relation.

Equation assumptions:

- Modular-exponentiation network is implemented perfectly (only QFT gates are perturbed in this scope).

## eq_2: Ideal inverse quantum Fourier transform

$$
\mathrm{QFT}^{-1}|x\rangle=\frac{1}{\sqrt{Q}}\sum_{y=0}^{Q-1}e^{-2\pi i xy/Q}|y\rangle,\quad \text{built from } H \text{ and } R_{k}=\mathrm{diag}(1,e^{i\theta_{k}}),\ \theta_{k}=\frac{2\pi}{2^{k}}
$$

Inverse QFT on the control register decomposed into Hadamards and controlled phase rotations R_k; these are the gates whose angles are perturbed in this scope.

Provenance: `standard_background`. Textbook QFT decomposition used to define the gate set subject to imperfections.

## eq_3: Systematic gate error model

$$
R_{k}(\theta_{k})\;\to\;R_{k}\big((1+\epsilon)\theta_{k}\big)\quad \text{for every gate, with fixed } \epsilon
$$

Every controlled rotation is over- or under-rotated by the same reproducible fractional amount; the perturbed circuit is still unitary and deterministic.

Provenance: `assumption`. The abstract names a 'systematic error' category but does not define it; a fixed fractional over-rotation is a minimal concrete model consistent with that name.

Equation assumptions:

- Error is identical on every gate and on every run.
- Hadamards are assumed ideal.

## eq_4: Random gate error model

$$
R_{k}(\theta_{k})\;\to\;R_{k}\big(\theta_{k}+\delta_{j}\big),\quad \delta_{j}\sim\mathcal{N}(0,\sigma^{2})\ \text{i.i.d. over gates } j \text{ and runs}
$$

Each gate application receives an independent zero-mean Gaussian phase error; observables are averaged over the error ensemble.

Provenance: `assumption`. The abstract names a 'random error' category without specifying its distribution; i.i.d. Gaussian angle noise is a minimal concrete model.

Equation assumptions:

- Gaussian distribution and independence across gates are chosen, not sourced.

## eq_5: Success probability figure of merit

$$
P_{\mathrm{succ}}(\epsilon,\sigma)=\mathbb{E}_{\delta}\Big[\sum_{y\in S_{r}}\big|\langle y|\,\widetilde{\mathrm{QFT}}^{-1}_{\epsilon,\delta}\,|\psi_{c}\rangle\big|^{2}\Big],\quad S_{r}=\{y:\ \mathrm{CF}(y/Q)\ \text{returns } r\}
$$

Probability, averaged over random errors, that the measured outcome y lies in the set S_r of outcomes from which the continued-fraction expansion of y/Q recovers the true order r. |psi_c> is the reduced control state after the work register is traced out/measured.

Provenance: `abstract_inferred`. Comparing robustness across error types requires a scalar performance metric; the probability of recovering the correct order is the natural one, though the abstract does not state which metric is used.

Abstract evidence: Shor's algorithm is robust against the systematic errors but is vulnerable to the random errors

Equation assumptions:

- The paper may use a different metric (e.g., fidelity of the output distribution).

## eq_6: Error threshold definition

$$
\sigma_{\mathrm{th}}(N)=\max\{\sigma\ge 0:\ P_{\mathrm{succ}}(0,\sigma)\ \ge\ \kappa\,P_{\mathrm{succ}}(0,0)\},\quad 0<\kappa<1
$$

Threshold on the random-error strength for a given N, defined as the largest sigma for which the success probability remains at least a fixed fraction kappa of its ideal value.

Provenance: `abstract_inferred`. The abstract states a threshold depending on N exists but gives neither its definition nor values; this is one concrete operationalization with kappa as a free choice.

Abstract evidence: Error threshold is given to the algorithm for a given number N to be factorized.

Equation assumptions:

- kappa (e.g., 1/2) is an unsourced choice.
- The threshold is defined on the random-error strength because the abstract says the algorithm is vulnerable to random errors.

## Registers

- control: t = 8 (instance) ; general t = 2n qubits; Phase-estimation register; holds superposition over exponents x and is Fourier-transformed and measured. Qubit 0 is the least significant bit of x.
- work: n = 4 (instance) ; general \lceil \log_2 N \rceil qubits; Holds a^x mod N after controlled modular multiplication; initialized to |1>.

## Initial state

|0\rangle^{\otimes t}_{c}\otimes|1\rangle_{w} = |0\ldots0\rangle_{c}|0001\rangle_{w} (binary 1 in the work register, LSB = qubit 0)

## Measurement

Computational-basis measurement of all t control qubits, giving integer y in [0, Q-1]; repeated over many runs (and over independent random-error samples) to estimate the outcome distribution.

## Classical postprocessing

Continued-fraction expansion of y/Q to obtain a candidate denominator r'; verify a^{r'} ≡ 1 (mod N); if r' is even and a^{r'/2} ≢ -1 (mod N), output gcd(a^{r'/2} ± 1, N). For N=15, a=7: r=4 and the factors are gcd(48,15)=3 and gcd(50,15)=5. P_succ is estimated as the fraction of outcomes in S_r.

## Algorithm steps

1. Apply H to each control qubit and the controlled-U^{2^j} modular multiplications (U|y>=|a y mod N>) to produce the ideal entangled state. (eq_1)
2. Apply the inverse QFT to the control register using the H and R_k decomposition. (eq_2)
3. Replace each R_k by its imperfect version: systematic over-rotation (case A), random Gaussian phase error (case B), or both (combined case, outside the scoped equations). (eq_3, eq_4)
4. Measure the control register and compute the success probability, averaging over random-error samples for cases B. (eq_5)
5. Sweep epsilon and sigma; identify the error threshold for N=15 from the decay of P_succ. (eq_6)

## Assumptions

- Instance choice N=15, a=7, t=8, n=4 is a smallest-useful selection, not sourced from the abstract.
- Only the QFT controlled-phase gates are perturbed; Hadamards and the modular-exponentiation network are ideal.
- Systematic error modeled as a uniform fractional over-rotation; random error modeled as i.i.d. Gaussian angle noise.
- Success probability of recovering the true order is used as the performance metric.
- Threshold defined via a fixed fraction kappa of the ideal success probability.

## Missing information

- The paper's precise definition of systematic, random, and combined gate errors (which gates, which parameters, which distributions).
- Whether errors are applied to the modular-exponentiation gates, the QFT, or both.
- The performance metric actually used and the quantitative definition of the error threshold.
- Numerical threshold values and their dependence on N.
- Any analytic result explaining robustness to systematic errors (e.g., coherent error cancellation) versus vulnerability to random errors.
