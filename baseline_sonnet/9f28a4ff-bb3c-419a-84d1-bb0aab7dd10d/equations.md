# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Estimate an unknown phase phi using a generalized Kitaev scheme in which N phase gates are distributed arbitrarily among M qubits prepared in a product state, with the goal of reaching Heisenberg-type 1/N^2 mean square error scaling.

Scope: Smallest useful construction: M=2 qubits in |+> product states, with n_1 and n_2 applications of the phase gate and n_1+n_2=N, together with the mean square error definition and the scaling claims. The optimal gate distribution, the lossy analysis, the Bayesian bound derivation and the Shor-type resource quantification are outside this scope.

## Symbols

- $\varphi$: unknown phase to estimate; domain: [0,2\pi)
- $N$: total number of phase gate applications; domain: positive integer
- $M$: number of qubits; domain: positive integer
- $n_k$: number of phase gates applied to qubit k; domain: nonnegative integers
- $\tilde\varphi$: estimator of the phase from measurement outcomes; domain: [0,2\pi)
- $\delta^2$: mean square error of the estimate; domain: nonnegative real

## eq_1: Resource constraint

$$
\sum_{k=1}^{M} n_k = N
$$

N phase gates are distributed in an arbitrary way among the M qubits.

Provenance: `abstract_inferred`. The abstract states that N gates act on M qubits with an arbitrary distribution. The sum constraint is the natural formalization of this.

Abstract evidence: where $N$ phase gates, acting on $M$ qubits prepared in a product state, may be distributed in an arbitrary way

Equation assumptions:

- Each gate acts on a single qubit
- The total gate count is the resource

## eq_2: Single-qubit state after n_k gates

$$
|\psi_k\rangle=\frac{1}{\sqrt2}\left(|0\rangle+e^{i n_k\varphi}|1\rangle\right)
$$

A qubit prepared in |+> that receives n_k phase gates U=diag(1,e^{i\varphi}).

Provenance: `assumption`. Standard Kitaev-type phase encoding, assumed here for the tiny instance. The abstract does not state it.

Equation assumptions:

- Phase gate U=diag(1,e^{i\varphi})
- Initial state |+>
- No loss

## eq_3: Product probe state

$$
|\Psi\rangle=\bigotimes_{k=1}^{M}|\psi_k\rangle
$$

The product state of all M qubits after the gates have been applied.

Provenance: `abstract_inferred`. The abstract says the qubits are prepared in a product state. The explicit form follows from eq_2.

Abstract evidence: acting on $M$ qubits prepared in a product state

Equation assumptions:

- The state stays a product state because there is no entangling operation

## eq_4: Mean square error

$$
\delta^2=\mathbb{E}\left[\,4\sin^2\!\left(\tfrac{\tilde\varphi-\varphi}{2}\right)\right]\approx\mathbb{E}\left[(\tilde\varphi-\varphi)^2\right]
$$

A periodic mean square error for a circular variable, which approximates the usual squared error when the error is small.

Provenance: `standard_background`. A common choice for phase estimation. The abstract names the mean square error but does not define it.

Equation assumptions:

- The precise cost function used in the paper may differ

## eq_5: Scaling claims

$$
\delta^2_{\mathrm{standard}}\propto \frac{1}{N},\qquad \delta^2_{\mathrm{optimal\ generalized}}\propto \frac{1}{N^2}
$$

Scaling of the error for the standard Kitaev algorithm and for the optimal generalized versions.

Provenance: `abstract_explicit`. These are the scalings stated in the abstract. Prefactors and the optimal distributions are not given.

Abstract evidence: where the mean square error scales as $1/N$, the optimal generalizations offer the Heisenberg $1/N^{2}$ error scaling

Equation assumptions:

- Lossless setting

## Registers

- q_1..q_M: M (taken as 2 in the tiny instance) qubits; probe qubits, each in a product state, each acted on by n_k phase gates

## Initial state

|+>^{\otimes M} (assumed)

## Measurement

Not specified in the abstract. A Kitaev-type single-qubit measurement in the X/Y basis of each qubit is a plausible assumption.

## Classical postprocessing

Not specified in the abstract. The estimate would be combined from the single-qubit outcomes, for example by a Bayesian or maximum-likelihood estimator.

## Algorithm steps

1. Choose a distribution (n_1,...,n_M) with total N (for example M=2, n_1+n_2=N). (eq_1)
2. Prepare each qubit in |+> and apply n_k phase gates to qubit k. (eq_2, eq_3)
3. Measure the qubits and form an estimate of phi, then evaluate its mean square error. The estimator is not specified in the abstract. (eq_4)
4. Compare the error scaling against the 1/N and 1/N^2 claims. (eq_5)

## Assumptions

- The scope is M=2 qubits with |+> inputs and the ideal lossless setting.
- The phase gate is diag(1,e^{i phi}).
- The mean square error is the periodic cost in eq_4.

## Missing information

- The optimal gate distributions n_k and the proofs of the 1/N^2 scaling
- The measurement and estimator used
- The Bayesian bound and its comparison
- The loss model and the comparison with entanglement-based strategies
- The alternative resource quantification for Shor's algorithm and the optimality proof for the standard procedure
