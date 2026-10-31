# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Analyze a generalized Kitaev phase estimation algorithm in which N phase gates acting on M qubits prepared in a product state may be distributed arbitrarily. Compare its mean square error scaling (Heisenberg 1/N^2 versus standard 1/N) and its closeness to the Bayesian bound, its behavior under losses against entanglement-based strategies, and its optimality under an alternative resource quantification relevant to Shor's algorithm.

Scope: Abstract-level reconstruction only: a small finite-instance model of distributing N phase gates over M product-state qubits and the resulting mean square error scalings. The optimal gate distributions, the loss model, the Bayesian bound derivation, and the alternative resource counting are not specified in the abstract.

## Symbols

- $N$: total number of phase gates (resource count); domain: positive integer
- $M$: number of qubits in a product state; domain: positive integer
- $\varphi$: unknown phase to be estimated; domain: [0,2\pi)
- $\hat\varphi$: phase estimate; domain: [0,2\pi)
- $\Delta^2\varphi$: mean square error of the estimate; domain: nonnegative real

## eq_1: Standard Kitaev scaling

$$
\Delta^2\varphi \propto 1/N
$$

Mean square error scaling of the standard algorithm

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: the mean square error scales as $1/N$

## eq_2: Heisenberg scaling of generalized algorithm

$$
\Delta^2\varphi \propto 1/N^2
$$

Optimal generalized distributions achieve Heisenberg error scaling

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: the optimal generalizations offer the Heisenberg $1/N^{2}$ error scaling

## eq_3: Mean square error definition

$$
\Delta^2\varphi=\langle (\hat\varphi-\varphi)^2\rangle
$$

Naive MSE; a periodic-phase version would be needed in practice

Provenance: `standard_background`. Standard definition; the abstract does not give the exact error measure.

Equation assumptions:

- Phase periodicity handled by a suitable circular error measure

## Registers

- q_1..q_M: M qubits; Probe qubits, each prepared in a product state (e.g. |+>), each receiving n_j phase gates with sum_j n_j = N

## Initial state

Product state of M qubits, e.g. (|0>+|1>)/sqrt2 on each qubit (assumed form)

## Measurement

Assumed: measure each qubit j independently in the X/Y basis (equivalently, a phase-sensitive projective measurement) to obtain outcomes whose statistics depend on n_j*phi. The abstract does not specify the actual basis.

## Classical postprocessing

Assumed: combine all qubit outcomes into an estimate of phi, e.g. by a Bayesian or maximum-likelihood estimator on the likelihood built from the cos/sin(n_j*phi) outcome probabilities, and evaluate the circular mean square error. The optimal estimator is not given in the abstract.

## Algorithm steps

1. Prepare each of the M qubits independently in a product superposition state. (no equation reference)
2. Choose a distribution {n_j} of the N phase gates over the qubits (arbitrary in the generalized scheme; standard Kitaev uses n_j=2^j). Qubit j acquires phase n_j*phi. (eq_1, eq_2)
3. Apply the phase gates to each qubit, then read out each qubit in a suitable basis (details below). (eq_3)

## Assumptions

- Error measure details are assumed.
- Each qubit j receives n_j gates with sum n_j = N, and the initial state is |+> on every qubit; the specific optimal distribution is not given in the abstract.
- Product state taken as |+> on each qubit.
- Standard Kitaev distribution n_j=2^j assumed as the reference case.
- Measurement basis and estimator are assumed, not taken from the abstract.
- Measurement is independent per-qubit phase-sensitive readout with Bayesian or ML postprocessing (assumed).

## Missing information

- Optimal gate distribution
- Loss model
- Bayesian bound formula
- Alternative resource quantification details
- Actual measurement basis and estimator used in the paper
