# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Simulate evolution e^{-iHt} under a d-sparse Hamiltonian H with max entry magnitude ||H||_max to error epsilon, using a linear combination of quantum walk steps with Bessel-function coefficients, achieving query and 2-qubit gate complexity logarithmic in 1/epsilon and nearly linear in tau = t d ||H||_max, together with a lower bound showing no algorithm has sublinear dependence on tau.

Scope: Abstract-level reconstruction of the problem statement, complexity claims and the high-level structure of the algorithm; the detailed circuit, walk operator construction and truncation are not given in the abstract.

## Symbols

- $\tau$: product of evolution time, sparsity, and magnitude of the largest Hamiltonian entry; domain: positive real
- $\epsilon$: allowed simulation error; domain: (0,1)
- $H$: sparse Hamiltonian to be simulated; domain: Hermitian operator
- $J_n$: Bessel function of the first kind, order n, used as combination coefficients; domain: real functions

## eq_1: Definition of tau

$$
\tau = t\, d\, \|H\|_{\max}
$$

Parameter governing the near-linear complexity: time times sparsity times max entry.

Provenance: `abstract_inferred`. The abstract defines tau as this product; the symbols t, d, max-norm are my notation.

Abstract evidence: the product $\tau$ of the evolution time, the sparsity, and the magnitude of the largest entry of the Hamiltonian

Equation assumptions:

- t is evolution time, d is sparsity

## eq_2: Target evolution

$$
U = e^{-iHt}
$$

Unitary to be approximated within error epsilon.

Provenance: `standard_background`. Standard definition of Hamiltonian simulation.

## eq_3: Bessel-weighted walk combination

$$
e^{-iHt}\approx \sum_{n=-K}^{K} c_n(J_n(\tau))\, W^{n}
$$

Schematic: linear combination of quantum walk steps W^n with Bessel-function coefficients, truncated at K; exact coefficients are not stated.

Provenance: `assumption`. Abstract states a linear combination of walk steps with Bessel coefficients; the precise form is a schematic assumption.

Equation assumptions:

- Schematic form only; exact coefficients and walk operator W unspecified

## Registers

- system: n qubits qubits; holds the state acted on by H
- walk_ancilla: unknown (encodes sparse row/column index registers) qubits; ancilla space on which the quantum walk operator W acts via oracle queries
- LCU_index: about log K qubits (K = truncation order, assumed) qubits; selects walk power n with amplitudes from Bessel coefficients

## Initial state

Arbitrary system state |psi> with walk ancillas in a fixed reference state and the LCU index register in the superposition prepared from Bessel-function weights.

## Measurement

Measure the LCU index register (and walk ancillas) in the computational basis; accept when they return the all-zero reference outcome, which heralds the approximate e^{-iHt}|psi> on the system register. Otherwise, or if no heralding is used, the system is measured in a basis of interest to extract observables (assumed).

## Classical postprocessing

Discard runs where the ancilla flag fails (or use amplitude amplification); estimate observables from the system measurement statistics of accepted runs. No further postprocessing is specified in the abstract.

## Algorithm steps

1. Prepare the LCU index register with amplitudes proportional to Bessel-function coefficients, truncated at order K=O(tau + log(1/epsilon)) (assumed). (eq_1, eq_3)
2. Apply controlled powers of the quantum walk operator W, built from sparse-Hamiltonian oracle queries, conditioned on the index register. (eq_3)
3. Unprepare the index register so the successful branch implements the approximation of e^{-iHt}; use amplitude amplification or segmenting if needed (assumed). (eq_2, eq_3)

## Assumptions

- eq_3 is a schematic placeholder, not the paper's exact formula.
- Register sizes, K scaling and amplitude amplification are assumed, not from the abstract.
- Truncation K=O(tau+log(1/epsilon)) is assumed.
- Measurement and postselection scheme is assumed, since the abstract does not specify it.
- Measurement is a heralded ancilla-zero check plus standard system readout (assumed).

## Missing information

- Exact walk operator and Bessel coefficient formula
- Truncation order K
- Exact circuit and register details, including ancilla sizes
- Lower-bound proof
- Paper's actual measurement or success-flag procedure
