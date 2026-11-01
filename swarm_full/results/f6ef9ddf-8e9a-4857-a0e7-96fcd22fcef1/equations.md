# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Approximate the mean value of a black-box function with quantum algorithms (one novel and asymptotically optimal, one a variation on Aharonov's earlier algorithm), and approximate the median of a set of points over an arbitrary distance function.

Scope: Abstract-level problem statement plus a small finite-instance mean-estimation setting for equations; the algorithmic details of the paper are not given in the abstract and are not reconstructed.

## Symbols

- $f$: black-box function whose mean is to be approximated; domain: f:{0,...,N-1}->[0,1] (assumed)
- $\mu$: mean value of f; domain: real in [0,1]
- $\epsilon$: additive accuracy of the estimate; domain: positive real

## eq_1: Mean value

$$
\mu=\frac{1}{N}\sum_{x=0}^{N-1}f(x)
$$

Mean of the black-box function over N points; the standard definition of the target quantity.

Provenance: `standard_background`. The abstract only says 'mean value of a black-box function'; the explicit formula is the standard definition, with domain assumed.

Equation assumptions:

- Uniform distribution over a finite domain of size N
- f takes values in [0,1]

## eq_2: Accuracy goal

$$
|\tilde{\mu}-\mu|\le\epsilon
$$

Target of the approximation: estimate within additive error epsilon.

Provenance: `assumption`. The abstract does not state the error criterion; additive error is an assumed standard choice.

Equation assumptions:

- Additive error model

## Registers

- x: ceil(log2 N) qubits qubits; index register holding a uniform superposition over the domain
- a: 1 qubit qubits; ancilla whose |1> amplitude encodes f(x)

## Initial state

|0>^{\otimes n}|0> on registers x and a (assumed)

## Measurement

In the placeholder amplitude-estimation sketch, measure the phase/counting register of amplitude estimation in the computational basis (the ancilla a is only used as the marked qubit inside the estimation). The paper's actual measurement scheme is not given in the abstract.

## Classical postprocessing

Convert the measured phase integer y over M outcomes to an amplitude estimate via sin^2(pi y/M), and output it as the estimate of mu; repeat and take the median if higher success probability is needed (assumed standard practice).

## Algorithm steps

1. Apply Hadamards to x to prepare the uniform superposition over the domain. (eq_1)
2. Query the oracle for f and rotate ancilla a so that the |1> amplitude squared on branch x is f(x). The probability of measuring a=1 is then mu (assumed encoding). (eq_1)
3. Apply amplitude estimation (assumed generic subroutine, with about 1/epsilon repetitions of the state-preparation unitary) to estimate mu within epsilon. (eq_1, eq_2)

## Assumptions

- Finite domain, uniform distribution, f in [0,1]
- Additive error criterion
- Generic amplitude-estimation sketch used as a placeholder, not the paper's algorithms
- Circuit plan is a generic amplitude-estimation placeholder, not the paper's algorithms
- Measurement and postprocessing are the standard amplitude-estimation ones, not confirmed for the paper

## Missing information

- Details of the novel optimal algorithm
- Details of the Aharonov-variant algorithm
- Median algorithm and distance function formalism
- Query complexity statements and success probability
- Actual circuit structure of the paper's two mean algorithms and the median algorithm
- Actual measurement and postprocessing of the paper's algorithms
