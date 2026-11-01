# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reconstruct a modified Tulsi quantum search algorithm in which the control qubit is measured intermediately, with a different choice of angular parameter. Study how the time lapse between measurements affects success probability, correlations (Mutual Information, Cumulative Correlation Measure) and the algorithm's order, which becomes O(N) when measuring at every step.

Scope: Small finite-instance reconstruction of the search with a control qubit and intermediate control measurements. The abstract does not give the exact oracle, angle definition or circuit, so only the generic structure and background search relations are specified. Eq_2 is a Grover-type stand-in, not the paper's formula.

## Symbols

- $N$: Size of the search space; domain: positive integer
- $\tau$: Number of algorithm steps between control measurements (time lapse); domain: positive integer
- $\theta$: Angular parameter of the search rotation; domain: real, radians
- $P_t$: Probability of finding the marked item after t steps; domain: [0,1]

## eq_1: Brute-force order

$$
O(N)
$$

The order of the modified algorithm becomes classical brute-force search when the control is measured at every step.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: became of order $O(N)$ (classical brute force search) when the measurement is taken in every step

## eq_2: Rotation-angle success probability

$$
P_t=\sin^2\big((2t+1)\theta\big)
$$

Standard Grover-type amplitude amplification with a single marked item, valid only for coherent evolution between measurements. Tulsi's version uses a different angular parameter, not specified here. Intermediate measurements break this coherent form.

Provenance: `standard_background`. Textbook background for amplitude-amplification-type search, not claimed to be the paper's exact formula.

Equation assumptions:

- Single marked item
- Unmeasured coherent evolution between control measurements

## Registers

- search: n = log2 N qubits qubits; Holds the database index; marked item searched
- control: 1 qubit qubits; Control qubit of the Tulsi-type search, measured intermittently every tau steps

## Initial state

Uniform superposition over the search register tensored with a control qubit in an assumed fixed state (e.g. |0> or |+>; not given in the abstract)

## Measurement

Intermediate projective measurement of the control qubit every tau steps (basis assumed computational); final measurement of the search register in the computational basis to read out the marked item.

## Classical postprocessing

Estimate success probability P_t versus tau from repeated runs or simulation; compute Mutual Information and Cumulative Correlation Measure from the resulting state or distributions; fit scaling of steps needed versus N to estimate the order.

## Algorithm steps

1. Prepare the search register in uniform superposition and initialize the control qubit. (no equation reference)
2. Apply one Tulsi-type search iteration (controlled oracle and diffusion-like operators with the chosen angle theta), rotating amplitude toward the marked item. (eq_2)
3. Repeat the iteration for tau steps coherently, then measure the control qubit; repeat this block until the total step count is reached. (eq_2)
4. For tau = 1 (measurement at every step) the performance degrades to classical-like scaling. (eq_1)

## Assumptions

- Standard Grover-type rotation used as background for the unspecified Tulsi dynamics
- Control measured in computational basis, with outcomes either averaged or post-selected (unspecified)
- Initial control state assumed

## Missing information

- Exact Tulsi oracle and control-qubit circuit
- Definition of the chosen angular parameter
- Measurement basis and post-measurement handling of the control
- Definitions of Mutual Information and Cumulative Correlation Measure as used
- Initial control state
- Whether control outcomes are averaged or post-selected
- Exact scaling for intermediate time lapses (only tau=1 giving O(N) is stated)
