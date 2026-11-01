# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Compare quantum search by discrete-time and continuous-time quantum walks relative to their classical random walks. The abstract says a discrete-time walk typically makes one walk step per oracle query, while a continuous-time walk can effectively make multiple walk steps per query when only query time is counted. Allowing the discrete-time walk multiple steps per query matches the continuous-time runtime, giving a cubic speedup over its corresponding classical random walk.

Scope: Conceptual query-complexity comparison only. The abstract gives no graph family, oracle construction, explicit runtimes, circuit, or measurement protocol, so only symbolic scaling relations and a generic search-walk framing can be reconstructed.

## Symbols

- $T_{\mathrm{cl}}$: Hitting time of the corresponding classical random walk; domain: positive real
- $T_{\mathrm{q}}$: Quantum search runtime counted in oracle query time; domain: positive real

## eq_1: Quadratic speedup

$$
T_{\mathrm{q}}=\Theta\left(\sqrt{T_{\mathrm{cl}}}\right)
$$

Generic quadratic speedup over the classical random walk, as in standard walk search.

Provenance: `standard_background`. The abstract mentions quadratic speedups but gives no formula; this is a standard-form placeholder.

Equation assumptions:

- Applies to the standard single-step-per-query regimes

## eq_2: Cubic speedup

$$
T_{\mathrm{q}}=\Theta\left(T_{\mathrm{cl}}^{1/3}\right)
$$

Cubic speedup over the classical random walk when multiple walk steps per query are allowed and only queries are counted.

Provenance: `abstract_inferred`. A cubic speedup is read as an exponent of 1/3 on the classical time; the exact model is unspecified.

Abstract evidence: it is a cubic speedup over its corresponding classical random walk

Equation assumptions:

- Cubic speedup interpreted as T_cl^{1/3} scaling

## Registers

- V: unknown (vertex space, dimension N) qubits; Walk position register over graph vertices; discrete-time version may need an added coin or edge register

## Initial state

Assumed uniform superposition over vertices (or the stationary-state analogue); the abstract does not specify it.

## Measurement

Assumed: after the evolution time/query count, measure the vertex register in the computational basis and check whether the outcome is the marked vertex; the abstract does not specify this.

## Classical postprocessing

Assumed: verify the measured vertex with one oracle query and repeat on failure; the expected number of repetitions is constant if the success probability is constant. Runtime scaling is compared to T_cl.

## Algorithm steps

1. Prepare the initial walk state on the vertex register. (no equation reference)
2. Alternate oracle queries marking the target with walk evolution. Standard regime: one walk step per query, giving quadratic scaling. (eq_1)
3. Multi-step regime: apply many walk steps (continuous-time evolution or repeated discrete steps) between oracle queries, counting only queries, giving cubic scaling. (eq_2)

## Assumptions

- Speedups are interpreted as power-law exponents in the classical hitting time.
- Registers, initial state and step structure are a generic assumed walk-search template, not taken from the abstract.
- Generic walk-search register and step template assumed.
- Measurement is a standard computational-basis vertex readout with constant success probability, not stated in the abstract.

## Missing information

- Graph family and marked-vertex model
- Oracle definition and cost model
- Explicit runtimes and walk-step counts per query
- Circuit, state and measurement details
- Number of walk steps per query and coin/edge register structure
- Actual success probability and readout protocol
