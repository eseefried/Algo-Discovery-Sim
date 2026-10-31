# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct a fixed-point version of quantum amplitude amplification that needs only a lower bound on the target fraction lambda of the initial state, retains the quadratic (Grover-type) query speedup, and guarantees an adjustable failure-probability bound over the broadest possible range of lambda for a given number of oracle queries.

Scope: Abstract-level problem statement plus minimal background equations for standard amplitude amplification and a failure-probability criterion. The specific fixed-point construction (phases, query count) is not given in the abstract and is not reconstructed.

## Symbols

- $\lambda$: fraction (probability weight) of the initial state in the target subspace; domain: (0,1]
- $\delta$: adjustable bound on failure probability; domain: (0,1)
- $\lambda_0$: known lower bound on lambda; the guaranteed range is lambda >= lambda_0; domain: (0,1]
- $Q$: number of oracle queries; domain: positive integers

## eq_1: Initial target fraction

$$
\lambda=\|\Pi|\psi_0\rangle\|^2
$$

Target fraction of the initial state under target projector Pi.

Provenance: `abstract_inferred`. Defines lambda as the target-state weight in the initial state.

Abstract evidence: what fraction $\lambda$ of the initial state is comprised of the target states

Equation assumptions:

- Pi is a projector onto target states

## eq_2: Standard Grover success probability

$$
P_{\text{succ}}(k)=\sin^2\!\big((2k+1)\arcsin\sqrt{\lambda}\big)
$$

Success probability after k standard amplification iterations; requires knowing lambda to choose k.

Provenance: `standard_background`. Textbook amplitude amplification; shown for contrast, not as the paper's fixed-point method.

Equation assumptions:

- Standard Grover iterations

## eq_3: Fixed-point failure guarantee

$$
1-P_{\text{succ}}(\lambda)\le\delta\quad\forall\,\lambda\ge\lambda_0
$$

Target guarantee: failure probability at most delta over a range of lambda with Q queries.

Provenance: `abstract_inferred`. Formalizes the adjustable failure bound; the range optimality is not derived.

Abstract evidence: Our result incorporates an adjustable bound on the failure probability

Equation assumptions:

- The range is lambda>=lambda_0

## Registers

- work: n qubits; holds the search state; initial state prepared by unitary A
- anc: 1 qubits; oracle flag qubit marking target states (assumed; could be absorbed in work)

## Initial state

|psi_0> = A|0>, with target weight lambda = ||Pi|psi_0>||^2 (eq_1)

## Measurement

Measure the work register (with the flag qubit) in the computational basis after the Q queries; success means the outcome lies in the target subspace (projector Pi), which occurs with probability at least 1-delta for lambda >= lambda_0 (assumed from eq_3).

## Classical postprocessing

Check the measured outcome with the marking predicate (one classical or oracle check); accept if marked, otherwise repeat the run. Repetition count is not specified in the abstract.

## Algorithm steps

1. Prepare |psi_0> by applying the state-preparation unitary A to |0>. (eq_1)
2. Apply a sequence of Q oracle queries interleaved with reflections about |psi_0> using phases (generalized, non-Grover phases) chosen from delta and lambda_0 so that failure <= delta for all lambda >= lambda_0. The phase sequence is NOT given in the abstract and is left unspecified. (eq_3)
3. For contrast, standard amplification with k iterations needs lambda known to pick k, and overshoots otherwise. (eq_2)

## Assumptions

- Guarantee formalized as failure <= delta for all lambda >= lambda_0
- Register layout and generic oracle-plus-reflection structure assumed from standard amplitude amplification
- Circuit uses oracle queries interleaved with reflections about the initial state, as in generalized amplitude amplification
- Measurement is a standard computational-basis readout with classical verification; not stated in the abstract
- Measurement is a computational-basis readout with classical verification of the marked outcome

## Missing information

- Explicit fixed-point phase sequence and query-count scaling
- Exact optimal range of lambda for given Q and delta
- Actual phase angles for the fixed-point sequence
- Measurement and verification details are not given in the abstract
