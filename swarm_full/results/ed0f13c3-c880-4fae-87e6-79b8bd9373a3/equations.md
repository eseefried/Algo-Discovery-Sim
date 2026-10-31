# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Determine whether discrete-time quantum walks on modified cycles C4, C6, C8 (and generalised families) admit perfect state transfer (PST) between antipodal nodes, for three coin choices, and test robustness of periodicity/PST/high-fidelity transfer to initial state, structure interpolation and decoherence.

Scope: Abstract-level reconstruction of a coined discrete-time quantum walk on small graphs (C4, C6, C8 variants); the exact modifications, the three coins and the families are not specified in the abstract, so a generic finite instance is used.

## Symbols

- $U$: One-step discrete-time walk operator, shift times coin; domain: Unitary on coin-node Hilbert space
- $S$: Shift operator along graph arcs; domain: Unitary
- $C$: Coin operator (one of three choices, unspecified); domain: Unitary on coin space
- $|\psi_0\rangle$: Initial state localised at source node; domain: Unit vector in coin-node space
- $F(t)$: Fidelity of transfer to the antipodal node at step t; domain: [0,1]

## eq_1: Walk operator

$$
U = S\,(I\otimes C)
$$

One step of the coined discrete-time quantum walk.

Provenance: `standard_background`. Standard coined-walk definition; the abstract does not give the explicit form.

Equation assumptions:

- Specific coin and shift conventions are assumed

## eq_2: Fidelity at target

$$
F(t)=\sum_{c}\left|\langle b,c|U^{t}|\psi_0\rangle\right|^{2}
$$

Probability of being at antipodal node b at step t; PST means F(t)=1 for some t.

Provenance: `assumption`. Formalises perfect or high-fidelity state transfer; assumed definition.

Equation assumptions:

- Fidelity defined as target-node probability summed over coin states

## Registers

- coin: deg(G) dimensional (2 for a plain cycle, assumed) qubits; Coin degree of freedom (arc direction)
- node: N nodes (N=4, 6, 8 for the cycle instances; ceil(log2 N) qubits if encoded) qubits; Walker position on the graph

## Initial state

Walker localised at source node a with a fixed coin state, |psi_0> = |a>|c_0>; the coin state is varied in robustness tests.

## Measurement

After t steps, measure the node register in the position basis (tracing out coin); the estimated frequency of outcome b over repeated runs estimates F(t). PST corresponds to F(t)=1 at some t. Repeat for t=0..T, for each coin and initial coin state.

## Classical postprocessing

Scan F(t) over t to find the first time with F≈1 (PST) or the maximum (high fidelity), and check periodicity by returning to F at the source. Compare across coins, initial states, structure interpolation parameters and decoherence strengths to assess robustness.

## Algorithm steps

1. Prepare |psi_0> at source node a with chosen coin state. (no equation reference)
2. Apply coin C on the coin register, then the shift S along graph arcs (one application of U), repeated t times. (eq_1)
3. Evaluate target-node probability at the antipodal node b after each step to detect PST (F=1) or high fidelity. (eq_2)

## Assumptions

- Generic coined walk on a finite graph stands in for unspecified modified cycles.
- Fidelity is the target-node probability.
- Coin dimension equals vertex degree (plain cycle: 2).
- Position-basis measurement of the node register is assumed; the abstract does not describe the measurement.

## Missing information

- Exact cycle modifications
- Three coin operators
- Three graph families
- Initial conditions and decoherence model
- Continuous-time walk details
- Exact modifications, coins and families are not in the abstract.
