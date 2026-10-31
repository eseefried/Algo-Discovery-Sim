# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Analyze how systematic phase-inversion errors affect the success rate and required iteration count of the optimized quantum random-walk search algorithm, using a geometric model, and compare its robustness with Grover's algorithm.

Scope: Abstract-level reconstruction of a phase-error model for a search over a database of size N. The explicit forms of the optimized operator and the error-dependent formulas are not given in the abstract. Equations are limited to a generic geometric rotation picture and are labeled as background or assumption.

## Symbols

- $N$: database size; domain: positive integer
- $k$: number of iterations; domain: non-negative integer
- $\beta$: systematic phase error in the phase inversions; domain: real
- $P_k(N,\beta)$: success rate after k iterations with phase error; domain: [0,1]

## eq_1: Success rate dependence

$$
P_k = P_k(N,k,\beta)
$$

The success rate depends on database size, iteration count and phase error.

Provenance: `abstract_inferred`. The abstract states this relationship exists but gives no explicit formula.

Abstract evidence: the relationship between the success rate of the algorithm, the database size, the number of iterations and the phase error is depicted

Equation assumptions:

- Explicit functional form is not given in the abstract.

## eq_2: Ideal geometric rotation (Grover-type background)

$$
P_k=\sin^2\big((2k+1)\theta\big),\ \sin\theta=1/\sqrt{N}
$$

Standard ideal-case Grover geometric picture, used only as a baseline. It is not the optimized quantum random-walk algorithm.

Provenance: `standard_background`. Familiar textbook baseline for the comparison; it is not claimed to be the paper's optimized walk.

Equation assumptions:

- No phase error
- Grover baseline only

## Registers

- search: \lceil\log_2 N\rceil (assumed) qubits; Database index register on which the search is performed
- coin_or_ancilla: unknown qubits; Possible coin or ancilla register of the quantum random walk; not specified in the abstract

## Initial state

Assumed uniform superposition over all N database states (standard for search; not stated in the abstract).

## Measurement

Assumed: after the chosen number of iterations k, measure the search register in the computational basis; success means obtaining the marked item, with probability P_k(N,beta). The abstract does not detail the measurement.

## Classical postprocessing

Assumed: repeat runs and compare observed success frequency with the predicted P_k; check whether the measured item is the marked one. Compare the maximum success rate and required k versus beta against Grover's algorithm to assess robustness. The paper's exact procedure is not given.

## Algorithm steps

1. Prepare the initial state, assumed to be the uniform superposition. (eq_2)
2. Repeat k times an iteration of two phase inversions (target-state and initial-state inversion) of the optimized random-walk search, each carrying a systematic phase error beta. The explicit operators are not given in the abstract. (eq_1)
3. Choose the iteration count k that maximizes the success rate for the given N and beta. The paper's formula is not available; the ideal Grover baseline serves only for comparison. (eq_1, eq_2)

## Assumptions

- Grover formula is only a baseline, not the paper's optimized algorithm.
- Register sizes and the initial state are assumed standard choices, not taken from the abstract.
- Index register of about log2 N qubits and a uniform-superposition initial state are assumed.
- Computational-basis measurement of the search register is assumed.

## Missing information

- Explicit optimized random-walk operators
- Error-dependent success-rate and iteration formulas
- Circuit and measurement details
- Whether a coin register is used and its size
