# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Analyze search for a marked vertex on the complete graph of N vertices by a lackadaisical quantum walk, where each vertex has l self-loops. Compare the discrete-time phase-flip coin, the SKW (2003) coin, and the continuous-time walk, and determine how success probability and runtime depend on l.

Scope: Abstract-level reconstruction of the single-marked-vertex complete-graph search. Only the qualitative effects of l are stated in the abstract. Explicit coin operators, the walk Hamiltonian, optimal l and runtimes, and the multiple-marked-vertex generalization are not given and are left unreconstructed.

## Symbols

- $N$: number of vertices of the complete graph; domain: positive integer
- $l$: number of self-loops attached to each vertex; domain: nonnegative integer (may scale with N)
- $p$: success probability of finding the marked vertex; domain: [0,1]

## eq_1: Phase-flip coin success with one self-loop

$$
p(l=0)=\tfrac12,\quad p(l=1)=1
$$

For the phase flip coin, adding one self-loop to each vertex raises the success probability from 1/2 to 1.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: adding a self-loop to each vertex boosts the success probability from $1/2$ to $1$

Equation assumptions:

- Single marked vertex
- Phase flip coin

## eq_2: Quantum speedup conditions

$$
l=o(N)\ \text{(phase flip coin)},\qquad l=o(N^{2})\ \text{(SKW coin)}
$$

The scaling of l below which the walk is faster than classical search: l less than N for the phase flip coin and less than N^2 for the SKW coin.

Provenance: `abstract_inferred`. Paraphrases the abstract's scaling statements as asymptotic conditions.

Abstract evidence: the first is faster than classical when $l$ scales less than $N$, while the second requires that $l$ scale less than $N^{2}$

Equation assumptions:

- Asymptotic reading of 'scales less than'

## Registers

- position: N vertices (basis states |v>) qubits; walker location; marked vertex is one basis state
- coin: N-1+l directions per vertex (assumed) qubits; edge and self-loop directions; N-1 edges to other vertices plus l self-loops

## Initial state

Assumed: uniform superposition over all vertices and all coin directions (including self-loops). Not specified in the abstract; for the lackadaisical walk the weighting of self-loop components may differ.

## Measurement

Assumed: after the chosen number of walk steps (or evolution time), measure the position register in the vertex basis and accept the outcome if it equals the marked vertex; the coin register is ignored/traced out. Success probability p is the probability of obtaining the marked vertex.

## Classical postprocessing

Assumed: check whether the measured vertex is the marked one (one oracle query); if not, repeat the walk and measurement. Expected repetitions are about 1/p. The optimal stopping time is not given in the abstract.

## Algorithm steps

1. Prepare the assumed initial state on the position and coin registers. (no equation reference)
2. Repeat for discrete-time walks: apply an oracle coin at the marked vertex (phase flip coin or SKW coin) and other vertices use a Grover diffusion coin over N-1+l directions; then apply the shift, which swaps along edges and leaves self-loop components in place. Uses l=1 for the phase flip coin to reach p=1. (eq_1, eq_2)
3. For continuous-time walk, evolve under a walk Hamiltonian with an oracle term; per the abstract, self-loops make no difference to the outcome. The Hamiltonian is not given. (no equation reference)

## Assumptions

- Single marked vertex baseline.
- Register sizes and initial state are assumed finite instances, not taken from the abstract.
- Coin register has N-1+l directions per vertex.
- Measurement is a standard position-basis measurement with repetition; not stated in the abstract.
- Measurement is a position-basis measurement with classical repetition, assumed.

## Missing information

- Explicit coin operators and the oracle
- Initial state definition
- Optimal l for the phase flip coin beyond l=1
- Runtime formulas and optimal stopping times
- Continuous-time Hamiltonian
- Multiple-marked-vertex details
- Optimal stopping time for measurement is not given.
