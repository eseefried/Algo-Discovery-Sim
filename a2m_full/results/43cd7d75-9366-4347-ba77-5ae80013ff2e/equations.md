# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate an unknown phase phi, uniform on [0,2pi), encoded by N applications of a phase gate diag(1,e^{i phi}) distributed as n_k over M unentangled |+> probe qubits (sum n_k = N), using X-basis readout and a classical Bayesian posterior-mean estimator, scored by a circular (Holevo) error.

Scope: One tiny non-adaptive instance: M=3 probe qubits with a sample multiplicity vector such as n=(1,2,2) (N=5) or n=(1,1,2,2); lossless; no feedback (theta_k=0); grid-search estimator. Out of scope: numerical optimization of the n_k distribution, the Bayesian bound derivation, the loss analysis and the comparison with entangled strategies, adaptive feedback, and the Shor-type resource-counting proof. The abstract gives no explicit formulas, so everything below is background or an assumed construction.

## Symbols

- $\varphi$: unknown phase; domain: [0,2\pi)
- $M$: number of probe qubits; domain: positive integer, small (e.g. 3)
- $n_k$: number of phase-gate applications on qubit k; domain: positive integers, k=0..M-1
- $N$: total number of gate applications = queries; domain: \sum_k n_k
- $b_k$: measurement outcome of qubit k; domain: {0,1}
- $\theta_k$: feedback phase offset (0 if non-adaptive); domain: real
- $\eta$: per-gate transmission in the loss model (outside scope; eta=1 here); domain: [0,1]
- $\hat\varphi$: posterior-mean-direction phase estimate; domain: [0,2\pi)
- $\Delta$: circular error 4 sin^2((hat phi - phi)/2); domain: [0,4]

## eq_1: Probe state after gates

$$
|\psi_k\rangle=\frac{|0\rangle+e^{i n_k\varphi}|1\rangle}{\sqrt2}
$$

Each probe qubit starts in |+> and acquires phase n_k phi from n_k phase-gate applications.

Provenance: `assumption`. Follows from the assumed diagonal phase gate acting n_k times on |+>; the abstract only says N gates act on M qubits in product state.

Equation assumptions:

- Phase gate is diag(1,e^{i phi}) or an equivalent controlled-U with an eigenstate

## eq_2: Constraint on resources

$$
\sum_{k=0}^{M-1} n_k=N
$$

Total number of gate placements equals the query count N.

Provenance: `abstract_inferred`. The abstract says N gates are distributed arbitrarily among M qubits; the sum constraint is the natural reading.

Abstract evidence: where $N$ phase gates, acting on $M$ qubits prepared in a product state, may be distributed in an arbitrary way

Equation assumptions:

- Each application counts as one query

## eq_3: Outcome likelihood

$$
P(b|\varphi)=\prod_{k}\frac{1+(-1)^{b_k}\cos(n_k\varphi+\theta_k)}{2}
$$

Outcome probabilities after H and computational-basis measurement of each qubit. With loss, cos is multiplied by eta^{n_k}.

Provenance: `standard_background`. Standard result for measuring (|0>+e^{i a}|1>)/sqrt2 in the X basis, where outcome 0 has probability (1+cos a)/2.

Equation assumptions:

- Qubits independent
- theta_k=0 for non-adaptive

## eq_4: Bayesian estimator

$$
\hat\varphi(b)=\arg\int_0^{2\pi}e^{i\varphi'}P(b|\varphi')\,d\varphi'\approx\arg\sum_{j}e^{i\varphi_j}P(b|\varphi_j),\ \varphi_j=2\pi j/G
$$

Posterior mean direction with a uniform prior, computed on a G-point grid. This is a grid approximation, not exact.

Provenance: `assumption`. A standard circular Bayesian estimator for a uniform prior; the paper's exact estimator is unknown.

Equation assumptions:

- Uniform prior
- Grid size G, e.g. 256

## eq_5: Error figure of merit

$$
\Delta=\mathbb{E}_{\varphi,b}\left[4\sin^2\frac{\hat\varphi(b)-\varphi}{2}\right]=\int\frac{d\varphi}{2\pi}\sum_b P(b|\varphi)\,4\sin^2\frac{\hat\varphi(b)-\varphi}{2}
$$

Holevo-style periodic mean square error used to compare strategies. Heisenberg scaling means Delta ~ 1/N^2.

Provenance: `abstract_inferred`. The abstract names the 1/N^2 scaling of the mean square error; the periodic error form is assumed.

Abstract evidence: the optimal generalizations offer the Heisenberg $1/N^{2}$ error scaling

Equation assumptions:

- Circular variance is the error measure

## Registers

- probe: M (e.g. 3) qubits; Each qubit starts in |+>, receives n_k phase-gate placements, then H and measurement; qubit k is classical bit k.
- eigenstate: 1 (optional) qubits; Eigenstate ancilla, only if the black box is a controlled-U. Not needed for a direct phase gate.

## Initial state

|+>^{\otimes M} (H on each probe qubit from |0>), no entanglement.

## Measurement

Measure all M probe qubits after H; the counts key's last character is bit 0, so b_k = key[::-1][k].

## Classical postprocessing

For each observed b, evaluate P(b|phi_j) on the grid, form sum_j exp(i phi_j) P(b|phi_j), take the argument mod 2pi as the estimate, and average the circular error over outcomes.

## Algorithm steps

1. Apply H to each probe qubit. (eq_1)
2. Place the black-box phase gate n_k times on qubit k (controlled on probe k with the eigenstate ancilla if a controlled-U), with total N queries. (eq_1, eq_2)
3. Apply H to each probe qubit and measure all M in the Z basis, with qubit k mapped to classical bit k (Qiskit little-endian: bits[::-1][k] is b_k). (eq_3)
4. Compute the posterior over the grid and return the phase estimate. (eq_4, eq_5)

## Assumptions

- The tiny instance M=3, n=(1,2,2) is a choice made here, not taken from the abstract
- Lossless, non-adaptive
- Uniform prior and circular variance
- Powers of the gate are built by repeated placement, each counted as a query
- Standard Kitaev n_k=2^k is the baseline

## Missing information

- The optimal n_k distributions and the paper's exact estimator and error measure
- Adaptive feedback schedule
- Exact loss model and the entangled-strategy bounds
- Bayesian bound formula and the alternative resource quantification for Shor-type counting
