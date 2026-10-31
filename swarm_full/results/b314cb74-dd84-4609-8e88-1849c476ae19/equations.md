# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Determine how the failure amplitude of hop operations (amplitude of staying put instead of hopping through a potential barrier) in the quantum walk formulation of Grover search affects runtime: the failure amplitude must scale as O(1/sqrt(N)) to retain O(sqrt(N)) search time, otherwise runtime degrades to classical O(N).

Scope: Abstract-level reconstruction of the scaling condition on hop failure amplitude for quantum-walk Grover search (discrete- and continuous-time). The detailed walk operators, proof, and circuits are not given in the abstract, so only the scaling relations are specified.

## Symbols

- $N$: Number of items in the searched database (number of vertices); domain: positive integer
- $\epsilon$: Failure amplitude of a hop (amplitude of staying put instead of hopping); domain: complex or real, |\epsilon| in [0,1]
- $T$: Search runtime (number of walk steps or evolution time); domain: positive real

## eq_1: Failure amplitude condition

$$
\epsilon = O(1/\sqrt{N})
$$

Condition on hop failure amplitude for the search to keep quantum speedup

Provenance: `abstract_inferred`. Directly stated in the abstract as a necessary scaling condition.

Abstract evidence: the failure amplitude must scale as $O(1/\sqrt{N})$

Equation assumptions:

- epsilon denotes the failure amplitude

## eq_2: Quantum runtime

$$
T = O(\sqrt{N})
$$

Retained quantum search runtime when the condition holds

Provenance: `abstract_inferred`. Abstract states the quantum runtime is O(sqrt(N)).

Abstract evidence: quantum $O(\sqrt{N})$ runtime

## eq_3: Classical runtime otherwise

$$
T = O(N)
$$

Runtime when failure amplitude is too large

Provenance: `abstract_inferred`. Abstract states the fallback runtime is classical O(N).

Abstract evidence: it searches in classical $O(N)$ time

Equation assumptions:

- applies when epsilon is not O(1/sqrt(N))

## Registers

- vertex: ceil(log2 N) qubits (assumed) qubits; Walker position register encoding the N database items/vertices
- coin_or_aux: unknown qubits; Optional coin/direction register for a discrete-time walk; absent in continuous-time

## Initial state

Uniform superposition over all N vertices (assumed standard walk-search start).

## Measurement

Assumed: after the walk runs for time T, measure the vertex register in the computational basis to read out the marked vertex. The abstract does not specify the measurement.

## Classical postprocessing

Assumed: check whether the measured vertex is marked using the oracle or a classical check; if not, repeat the run. Not specified in the abstract.

## Algorithm steps

1. Prepare the uniform superposition over vertices. (no equation reference)
2. Repeat walk steps: apply a marked-vertex oracle/perturbation, then a hop operator that succeeds with amplitude ~1 and fails (stays put) with amplitude epsilon, for T steps or evolution time. (eq_1, eq_2)
3. If epsilon is not O(1/sqrt(N)), the hop errors accumulate and the search needs T = O(N) steps. (eq_3)

## Assumptions

- Symbol epsilon is introduced for the failure amplitude.
- Register sizes and the initial state are assumed from the standard quantum-walk search setup, not stated in the abstract.
- Standard uniform-superposition initial state and log2 N qubit vertex register.
- Measurement is a computational-basis readout of the vertex register, with classical verification and repetition (assumed).

## Missing information

- Explicit walk operators and barrier model
- Proof details
- Exact circuit/coin construction
- Coin register structure and oracle implementation are unspecified.
- Actual measurement protocol and success probability are not given in the abstract.
