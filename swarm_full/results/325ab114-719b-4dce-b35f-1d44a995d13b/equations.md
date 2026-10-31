# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Study how imperfect gate operations (systematic, random, and combined errors) affect Shor's prime factorization algorithm, and determine an error threshold for factoring a given number N.

Scope: Abstract-level reconstruction of the error-model framing and qualitative findings only; the explicit gate error model, circuit, and threshold formula are not given in the abstract.

## Symbols

- $N$: Integer to be factorized; domain: positive composite integer
- $\epsilon$: Gate error strength (assumed parameter for threshold); domain: real, nonnegative

## eq_1: Error threshold condition

$$
\epsilon < \epsilon_{th}(N)
$$

Algorithm succeeds when gate error is below a threshold that depends on N.

Provenance: `abstract_inferred`. The abstract states a threshold depending on N; the functional form is not given.

Abstract evidence: Error threshold is given to the algorithm for a given number N to be factorized.

Equation assumptions:

- Threshold treated as a single scalar epsilon_th(N); form unknown.

## Registers

- control: t ~ 2*ceil(log2 N) (assumed) qubits; Holds the phase estimation / QFT input for period finding
- work: ceil(log2 N) (assumed) qubits; Holds modular exponentiation values a^x mod N

## Initial state

Control register in |0>^t and work register in |1>, assuming standard Shor structure.

## Measurement

Assumed standard Shor readout: measure the control register in the computational basis to obtain an integer y approximating a multiple of 2^t/r; the success probability of obtaining useful y is degraded by gate errors. The abstract does not specify the measurement scheme.

## Classical postprocessing

Assumed standard Shor postprocessing: compute y/2^t, use continued fractions to extract the period r, check a^r = 1 mod N, and if r is even compute gcd(a^(r/2) +/- 1, N) to get factors; repeat on failure. Success rate versus epsilon is compared with the threshold epsilon_th(N).

## Algorithm steps

1. Apply Hadamard gates to the control register to create a uniform superposition; each gate carries an error of strength epsilon (systematic or random). (eq_1)
2. Apply controlled modular exponentiation x -> a^x mod N into the work register using imperfect gates. (eq_1)
3. Apply an inverse QFT, built from imperfect Hadamard and controlled-phase gates, to the control register. (eq_1)

## Assumptions

- Error strength is modeled by a scalar epsilon.
- Circuit follows the standard Shor layout; the paper's exact circuit and register sizes are not given in the abstract.
- Measurement and postprocessing follow textbook Shor; the paper's specific scheme is not given in the abstract.

## Missing information

- Explicit gate error models (systematic, random, combined)
- Functional form of the threshold epsilon_th(N)
- Exact circuit details and register sizes from the paper
- Paper's specific measurement and success criterion
