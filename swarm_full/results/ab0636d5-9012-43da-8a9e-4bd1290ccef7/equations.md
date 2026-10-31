# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Synthesize a Repeat-Until-Success (RUS) circuit over the Clifford+T basis with one ancilla qubit and measurement that approximates a given single-qubit unitary to precision epsilon, using a probabilistically polynomial-time classical algorithm. The expected T-count is compared with the ancilla-free lower bound.

Scope: Abstract-level reconstruction only: problem statement, target precision, and the T-count comparison. The synthesis algorithm, circuit structure, and measurement protocol are not given in the abstract.

## Symbols

- $\varepsilon$: Approximation precision for the target single-qubit unitary; domain: \varepsilon>0
- $U$: Target single-qubit unitary; domain: U\in SU(2)
- $\tilde U$: Unitary or channel implemented by the RUS circuit upon success; domain: single-qubit unitary or channel
- $T_{\mathrm{free}}$: Theoretical lower bound on T-count for ancilla-free decomposition; domain: positive real
- $E[T_{\mathrm{RUS}}]$: Expected T-count of the RUS circuit; domain: positive real

## eq_1: Ancilla-free T-count lower bound

$$
T_{\mathrm{free}}=3\log_{2}(1/\varepsilon)
$$

Theoretical lower bound on T-count for ancilla-free single-qubit circuit decomposition.

Provenance: `abstract_explicit`. The abstract states this lower bound explicitly.

Abstract evidence: 3\log_{2}(1/\varepsilon)

## eq_2: Reported average RUS improvement

$$
E[T_{\mathrm{RUS}}]\approx T_{\mathrm{free}}/2.5
$$

Numerical evidence that the expected T-count is on average about 2.5 times lower than the ancilla-free bound.

Provenance: `abstract_inferred`. The ratio is read directly from the abstract's claim.

Abstract evidence: expected $T$-count on average $2.5$ times lower than the theoretical lower bound

Equation assumptions:

- The factor 2.5 is read as a ratio of average values.

## eq_3: Approximation criterion

$$
d(U,\tilde U)\le\varepsilon
$$

The synthesized operation is within precision epsilon of the target. The distance d is not specified in the abstract.

Provenance: `assumption`. The precision is only stated as epsilon; the metric is assumed.

Equation assumptions:

- d is some unitary distance such as the diamond norm or operator norm.

## Registers

- q: 1 qubits; Data qubit on which the approximation of U is implemented
- a: 1 qubits; Single ancilla qubit measured to herald success or failure

## Initial state

Data qubit q in an arbitrary input state |psi>, ancilla a in |0> (assumed; reset to |0> on each repeat).

## Measurement

Measure the single ancilla qubit in the computational basis after the joint Clifford+T circuit. Assumed convention: outcome 0 means success; outcome 1 means failure, followed by correction or restart. The abstract does not specify the outcome convention.

## Classical postprocessing

Classical control repeats the circuit until the success outcome occurs. Expected T-count is estimated numerically as T per attempt times the expected number of attempts (1/success probability), and compared with 3 log2(1/epsilon). The classical synthesis algorithm itself is not specified in the abstract.

## Algorithm steps

1. Prepare the ancilla in |0> and apply a synthesized Clifford+T sequence acting jointly on data and ancilla; the specific sequence is produced by the classical synthesis algorithm (not given in the abstract). (eq_3)
2. Measure the ancilla. On the success outcome, the data qubit holds the approximation of U within epsilon; on failure, apply a correction (assumed Clifford-type) or restart, repeating until success. (eq_3)
3. Count expected T gates over the geometric number of repetitions and compare with the ancilla-free bound. (eq_1, eq_2)

## Assumptions

- The distance metric is unspecified and assumed to be standard.
- The RUS skeleton (ancilla in |0>, joint Clifford+T circuit, ancilla measurement, repeat on failure) is generic and assumed, not taken from the abstract.
- Ancilla outcome 0 is assumed to signal success.
- The 2.5 factor is an average over tested targets, not a worst-case guarantee.

## Missing information

- The RUS synthesis algorithm
- Circuit structure and ancilla usage
- Success and failure outcomes and the correction procedure
- The classical runtime polynomial
- Exact gate sequence
- Distance metric and test distribution for the numerical average
