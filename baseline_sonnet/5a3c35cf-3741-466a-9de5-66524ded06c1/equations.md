# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate a given single-qubit unitary U to precision epsilon with a Repeat-Until-Success (RUS) circuit over Clifford+T plus one ancilla and measurement, minimizing expected T-count. The abstract claims a probabilistically polynomial-time classical synthesis algorithm, but gives no construction.

Scope: Only the generic RUS success/failure structure and the T-count comparison with the ancilla-free bound 3 log2(1/epsilon) are specified. The paper's actual synthesis algorithm (how the RUS circuit is found, the polynomial-time method, the numerics) is outside this scope.

## Symbols

- $U$: target single-qubit unitary; domain: SU(2)
- $\varepsilon$: approximation precision; domain: (0,1)
- $W$: Clifford+T circuit acting on data qubit and one ancilla; domain: 4x4 unitary
- $K_0$: 2x2 operator on the data qubit applied upon the success measurement outcome (ancilla |0>); domain: 2x2 complex matrices
- $p$: success probability per attempt; domain: (0,1]
- $\tilde U$: unitary implemented on success, K_0 up to normalization; domain: SU(2)
- $T_a$: T-count of one RUS attempt; domain: positive integers
- $\mathbb{E}[T]$: expected total T-count; domain: positive reals

## eq_1: Ancilla-free T-count lower bound

$$
T_{\text{free}} \ge 3\log_2(1/\varepsilon)
$$

Theoretical lower bound for ancilla-free single-qubit Clifford+T decomposition quoted in the abstract.

Provenance: `abstract_explicit`. Stated directly in the abstract as a bound.

Abstract evidence: theoretical lower bound of $3\log_{2}(1/\varepsilon)$ for ancilla-free single-qubit circuit decomposition

Equation assumptions:

- Asymptotic/leading-order meaning; additive constants not given

## eq_2: Reported expected T-count ratio

$$
\mathbb{E}[T_{\text{RUS}}] \approx \frac{1}{2.5}\cdot 3\log_2(1/\varepsilon)
$$

Numerical average claim: RUS expected T-count is about 2.5 times lower than the ancilla-free bound.

Provenance: `abstract_inferred`. Inferred by translating the 2.5 times lower claim into a ratio. It is an empirical average, not an exact equality.

Abstract evidence: expected $T$-count on average $2.5$ times lower than the theoretical lower bound

Equation assumptions:

- Average over tested targets
- Approximate relation

## eq_3: RUS attempt structure

$$
(\langle 0|_a\otimes I)\,W\,(|0\rangle_a\otimes|\psi\rangle)=K_0|\psi\rangle,\quad p=\|K_0|\psi\rangle\|^2
$$

Success branch of one attempt: measuring the ancilla in |0> applies K_0 to the data qubit. Ideally K_0 = sqrt(p) times a unitary close to U.

Provenance: `standard_background`. Generic RUS structure; the abstract names RUS with one ancilla and measurement but gives no explicit W or K_0.

Equation assumptions:

- Success is ancilla outcome 0
- K_0 proportional to a unitary independent of psi

## eq_4: Approximation condition

$$
\|\tilde U-U\|\le\varepsilon,\quad \tilde U=K_0/\sqrt p
$$

Precision requirement on the success-branch unitary.

Provenance: `assumption`. The abstract states approximation within epsilon but not the norm. The operator norm is assumed (global phase handling unspecified).

Equation assumptions:

- Operator norm or a comparable metric
- Global phase handling unspecified

## eq_5: Expected T-count with geometric repetition

$$
\mathbb{E}[T]=T_a/p
$$

If each attempt costs T_a T gates and succeeds independently with probability p, the number of attempts is geometric with mean 1/p. Failure branches are assumed correctable or restartable at no extra cost.

Provenance: `standard_background`. Standard geometric-trial expectation; the paper's actual cost model is not given in the abstract.

Equation assumptions:

- Independent attempts
- Failures restart cleanly without extra T cost
- Constant T_a and p across attempts

## Registers

- data: 1 qubits; qubit on which the approximation of U is implemented
- ancilla: 1 qubits; ancilla measured to herald success or failure

## Initial state

Assumed: ancilla |0> and data in an arbitrary state |psi>.

## Measurement

Ancilla measured in the computational basis after each attempt; the success outcome is assumed to be 0.

## Classical postprocessing

The classical probabilistic polynomial-time synthesis search that finds W for given U and epsilon is not specified in the abstract.

## Algorithm steps

1. Prepare ancilla in |0> and apply the Clifford+T circuit W on data and ancilla (the specific W is not given in the abstract). (eq_3)
2. Measure the ancilla. On the success outcome the data holds K_0|psi>/sqrt(p), approximating U. On failure, correct or restart, repeating until success. (eq_3, eq_4, eq_5)
3. Compare the expected T-count with the ancilla-free bound. (eq_1, eq_2, eq_5)

## Assumptions

- The success outcome is ancilla 0.
- Failure branches are handled by restarting, with no extra cost.
- The error metric is the operator norm.
- No explicit tiny instance is chosen because the construction is unknown.

## Missing information

- The actual synthesis algorithm and its polynomial runtime analysis
- Explicit RUS circuit structure, W, and failure-correction scheme
- Exact definition of the error metric and cost model
- Numerical details such as target distribution and sample sizes
- Previous exponential-time algorithm details
