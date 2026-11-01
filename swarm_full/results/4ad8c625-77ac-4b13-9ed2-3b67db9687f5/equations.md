# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Classically design quantum circuits that simulate an arbitrary qudit channel on a fault-tolerant quantum computer within a prescribed diamond-norm error, by decomposing the channel into a convex combination of generalized extreme channels and randomly sampling one such channel circuit.

Scope: Abstract-level reconstruction of the decomposition and sampling framework only; the nonlinear coupled equations, circuit construction, measurement details, and gate-level details are not given in the abstract.

## Symbols

- $\mathcal{E}$: target qudit channel to be simulated; domain: CPTP maps on a d-dimensional Hilbert space
- $p_k$: convex mixture weights; domain: probability vector, p_k>=0, sum_k p_k=1
- $\mathcal{E}_k$: generalized extreme channels; domain: CPTP maps on a d-dimensional Hilbert space
- $\epsilon$: diamond-norm error tolerance; domain: positive real
- $d$: qudit Hilbert space dimension; domain: integer >= 2

## eq_1: Convex decomposition

$$
\mathcal{E}=\sum_k p_k\,\mathcal{E}_k
$$

Target channel as a convex combination of generalized extreme channels.

Provenance: `abstract_inferred`. Directly states the decomposition; the explicit symbolic form is an inferred rendering.

Abstract evidence: decomposing a quantum channel into a convex combination of generalized extreme channels

Equation assumptions:

- Exact or approximate decomposition within tolerance

## eq_2: Diamond-norm tolerance

$$
\left\|\mathcal{E}-\tilde{\mathcal{E}}\right\|_{\diamond}\le\epsilon
$$

Simulated channel is within epsilon of the target in diamond distance.

Provenance: `abstract_inferred`. Abstract specifies the error criterion; the inequality form is inferred.

Abstract evidence: within a pre-specified error tolerance with respect to diamond-norm distance

Equation assumptions:

- tilde E denotes the randomized simulated channel

## Registers

- system: 1 qudit of dimension d (the channel's input) qubits; holds the state on which the channel acts
- ancilla: 1 qudit qubits; single ancillary qudit used to realize the generalized extreme channel
- classical_dits: unknown qubits; classical dits used by the circuit, e.g. to store the sampled index k or outcomes

## Initial state

System in arbitrary input state rho; ancilla qudit in a fixed reference state (assumed |0>); classical dits initialized to 0.

## Measurement

No measurement is specified in the abstract. The output is the channel's output state on the system register, with the ancilla discarded. Any mid-circuit measurement or classical-dit recording inside a generalized extreme channel circuit is unspecified. Assumed: the user measures the system in whatever basis their downstream task requires.

## Classical postprocessing

Classical stage (from the abstract): solve the nonlinear coupled algebraic equations to get {p_k, E_k}, then randomly sample k per p_k. Verifying epsilon is not detailed. Any outcome-dependent processing via the classical dits is unspecified.

## Algorithm steps

1. Classically solve the nonlinear coupled algebraic equations to decompose the target channel into weights p_k and generalized extreme channels E_k, to within tolerance epsilon. (eq_1, eq_2)
2. Randomly sample an index k with probability p_k. (eq_1)
3. Apply the fault-tolerant circuit implementing the sampled generalized extreme channel E_k on the system plus the single ancilla qudit, using classical dits as needed. (eq_1)
4. Discard or reset the ancilla; the averaged output is the simulated channel within epsilon in diamond norm. (eq_2)

## Assumptions

- Symbolic forms are generic renderings of abstract statements.
- Ancilla is initialized to |0> and discarded at the end (assumed).
- Register roles inferred from the single-ancilla plus classical dits statement.
- Classical dits record the sampled index or intermediate outcomes.
- Measurement is left to the downstream user.

## Missing information

- Explicit nonlinear coupled algebraic equations
- Definition of generalized extreme channels
- Gate-level construction of generalized extreme channel circuits
- Exact role of classical dits and any mid-circuit measurements
- Derivation of the run-time scaling (logarithmic in error tolerance, quadratic in d)
- Specific measurement protocol, if any
