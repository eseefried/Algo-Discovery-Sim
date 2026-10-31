# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize lazy quantum walks (Childs' construction): their n-th moment scaling O(t^n), the concentration interval of the lazy walk with a DFT coin compared with the Hadamard walk, and a new occupancy number/rate measure showing higher occupancy than normal quantum, classical and lazy classical walks.

Scope: Small finite instance of a 1D lazy discrete-time quantum walk with explicit coin. The abstract gives only qualitative claims, so the exact lazy-walk operator and occupancy definitions are not given and remain assumed or missing. Only the moment scaling and normalization are formalized.

## Symbols

- $M_n(t)$: n-th moment of the position probability distribution after t steps; domain: real, nonnegative
- $P(x,t)$: probability of finding the walker at position x after t steps; domain: [0,1]
- $t$: number of walk steps; domain: nonnegative integers

## eq_1: Moment scaling

$$
M_n(t)=\sum_x x^n P(x,t)=O(t^n)
$$

The n-th moment of the lazy quantum walk distribution scales as t^n, as for normal quantum walks.

Provenance: `abstract_inferred`. Moment definition is standard; the scaling is stated in the abstract.

Abstract evidence: lazy quantum walks have $O(t^{n})$ order of the n-th moment of the corresponding probability distribution

Equation assumptions:

- Moment taken as the sum over x of x^n P(x,t)

## eq_2: Probability normalization

$$
\sum_x P(x,t)=1
$$

The position distribution is normalized at every step.

Provenance: `standard_background`. Unitary evolution preserves total probability.

## Registers

- coin: 2 qubits (4-dim, for DFT coin) or 1 qubit; assumed qubits; Coin/laziness degree of freedom; the extra stay direction is encoded here
- position: ceil(log2(2T+1)) qubits for T steps; assumed qubits; Walker position on a line (cyclic finite register)

## Initial state

Assumed: position |0>, coin in a fixed basis state, e.g. |0>; the paper's initial state is not given in the abstract.

## Measurement

Measure the position register in the computational basis at step t, repeated over many runs to estimate P(x,t) (assumed; not stated in the abstract).

## Classical postprocessing

Compute moments M_n(t) and the concentration interval from the estimated P(x,t); occupancy number/rate cannot be computed since the definitions are missing.

## Algorithm steps

1. Prepare position at the origin and the coin in the assumed initial state. (eq_2)
2. Apply the coin operator (Hadamard or DFT) to the coin register. (no equation reference)
3. Apply a conditional shift moving left, right, or staying (lazy) depending on coin state. (no equation reference)
4. Repeat the coin and shift for t steps, then read the distribution P(x,t) and its moments. (eq_1, eq_2)

## Assumptions

- The 1D line walk is the setting.
- Lazy walk is modeled as a coin with a stay direction (assumed); register sizes are assumed.
- Measurement in the position basis with repeated runs is assumed.
- Measurement is a computational-basis position readout with repeated runs.

## Missing information

- Exact lazy walk operator and laziness parameter
- Definition of occupancy number and occupancy rate
- DFT coin dimension and initial coin state
- Quantitative concentration interval for the DFT lazy walk
