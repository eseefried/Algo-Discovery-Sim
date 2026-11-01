# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate an arbitrary qudit channel within diamond-norm error epsilon by randomly sampling one generalized extreme channel circuit from a convex decomposition of the channel, using a single ancillary qudit plus classical dits.

Scope: Only the convex-decomposition and random-sampling structure with diamond-norm error criterion, plus a tiny assumed instance (single qubit, d=2). The nonlinear coupled algebraic equations, definition of generalized extreme channels, circuit compilation, and the complexity scalings are out of scope because the abstract does not specify them.

## Symbols

- $\mathcal{E}$: Target qudit channel (CPTP map); domain: CPTP maps on d-dimensional Hilbert space
- $d$: Qudit/Hilbert space dimension; domain: integer >= 2
- $\epsilon$: Diamond-norm error tolerance; domain: (0,1)
- $\mathcal{E}_k$: Generalized extreme channel k; domain: CPTP maps
- $p_k$: Convex weights of the decomposition, used as sampling probabilities; domain: p_k>=0, sum_k p_k=1
- $K$: Number of terms in the decomposition; domain: positive integer
- $\|\cdot\|_\diamond$: Diamond norm; domain: norm on superoperators

## eq_1: Convex decomposition

$$
\mathcal{E}=\sum_{k=1}^{K}p_k\,\mathcal{E}_k,\quad p_k\ge0,\ \sum_k p_k=1
$$

Channel written as a convex combination of generalized extreme channels.

Provenance: `abstract_inferred`. Direct reading of the abstract's decomposition claim; the precise definition of the generalized extreme channels is not given.

Abstract evidence: decomposing a quantum channel into a convex combination of generalized extreme channels

Equation assumptions:

- Decomposition may be exact or approximate within epsilon

## eq_2: Diamond-norm tolerance

$$
\Big\|\mathcal{E}-\sum_k p_k\mathcal{E}_k\Big\|_\diamond\le\epsilon
$$

Accuracy criterion for the designed implementation.

Provenance: `abstract_inferred`. The abstract states a diamond-norm tolerance; the inequality form is an inferred formalization.

Abstract evidence: within a pre-specified error tolerance with respect to diamond-norm distance

Equation assumptions:

- Tolerance applies to the mixture of the sampled circuits

## eq_3: Random circuit sampling

$$
\Pr[\text{circuit }k]=p_k,\quad \bar{\mathcal{C}}=\sum_k p_k\,\mathcal{E}_k
$$

Randomly choosing circuit k with probability p_k realizes the averaged channel.

Provenance: `abstract_inferred`. Random selection from a convex decomposition naturally uses the weights as probabilities; the weights being the sampling distribution is an inference.

Abstract evidence: The resultant circuit is a randomly chosen generalized extreme channel circuit

Equation assumptions:

- Sampling distribution equals p_k

## eq_4: Diamond norm definition

$$
\|\Phi\|_\diamond=\sup_{\rho}\|(\Phi\otimes\mathrm{id}_d)(\rho)\|_1
$$

Standard definition of the diamond norm, with the supremum over states on the system plus a reference of the same dimension.

Provenance: `standard_background`. Standard background definition.

Equation assumptions:

- The reference system has dimension d

## Registers

- system: one qudit of dimension d qubits; Qudit on which the channel acts
- ancilla: one qudit qubits; Single ancillary qudit, as stated in the abstract
- classical dits: unknown qubits; Classical control or randomness for the sampling/circuit

## Classical postprocessing

Classical optimization yields the decomposition; any classical-dit processing is unspecified.

## Algorithm steps

1. Classically solve for weights p_k and generalized extreme channels E_k such that the mixture approximates E within epsilon in diamond norm (the nonlinear coupled algebraic equations are unspecified). (eq_1, eq_2)
2. Sample index k with probability p_k. (eq_3)
3. Run the circuit for E_k on the system plus the single ancilla qudit with classical dits; fault-tolerant compilation is unspecified. (eq_3)

## Assumptions

- Illustrative tiny instance would be d=2 (a qubit channel), not given in the abstract
- Exact form of the diamond-norm guarantee for the sampled mixture is assumed

## Missing information

- Definition of generalized extreme channels
- The nonlinear coupled algebraic equations and the optimization procedure
- Circuit construction for each generalized extreme channel
- Exact run-time scaling formulas (logarithmic in 1/epsilon, quadratic in d)
- Role and number of classical dits
