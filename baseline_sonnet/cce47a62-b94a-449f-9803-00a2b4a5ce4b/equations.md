# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Physical mapping of fault-tolerant quantum circuits (scheduling, placement, routing) onto Universal Logic Blocks, plus selecting a single best ULB size by weighting operation latencies with critical-path occurrence frequencies. The abstract gives no formal equations.

Scope: Smallest useful construction: a weighted-latency ULB size selection criterion and a schedule latency with routing delays on a dependency DAG, with a generic force-directed scheduling force term as background. The full mapper (loose scheduling with no-cloning DFG transformation, timing-driven placement, dynamic routing) and the 40% experimental result are outside scope. No quantum circuit or state preparation is specified.

## Symbols

- $s$: candidate ULB size; domain: finite candidate set S
- $o$: FT quantum operation type; domain: finite set O
- $L(o,s)$: latency of FT operation o mapped onto ULB of size s; domain: nonnegative reals
- $f_o$: occurrence frequency of operation o on critical paths of the target algorithm; domain: [0,1], normalized sum to 1 (assumed)
- $\bar L(s)$: weighted latency for ULB size s; domain: nonnegative reals
- $s^*$: chosen best ULB size; domain: S
- $G=(V,E)$: quantum data flow graph, a DAG whose edges are qubit dependencies; domain: directed acyclic graph
- $t_v$: start time (schedule level) of operation v; domain: nonnegative reals
- $d_v$: execution latency of operation v; domain: nonnegative reals
- $r_{uv}$: routing latency between predecessor u and operation v, depending on placement; domain: nonnegative reals
- $T$: circuit latency; domain: nonnegative reals

## eq_1: Weighted ULB latency

$$
\bar L(s)=\sum_{o\in O} f_o\,L(o,s)
$$

Weighted average latency of FT operations for ULB size s, weighted by critical-path frequency.

Provenance: `abstract_inferred`. The abstract says latencies are weighed by critical-path occurrence frequency; a linear weighted sum is the simplest reading, but the exact weighting is not stated.

Abstract evidence: using information about the occurrence frequency of operations on critical paths of the target quantum algorithm to weigh these latencies

Equation assumptions:

- Weighting is linear
- f_o normalized to sum to 1

## eq_2: Best ULB size

$$
s^*=\arg\min_{s\in S}\bar L(s)
$$

Select the single ULB size minimizing weighted latency.

Provenance: `abstract_inferred`. Choosing the best size by examining weighted latencies implies minimization; the details are not given.

Abstract evidence: an approach is presented to determine the single best ULB size for a target quantum circuit

Equation assumptions:

- Minimization of weighted latency is the criterion

## eq_3: Precedence with routing latency

$$
t_v\ge t_u+d_u+r_{uv}\quad\forall (u,v)\in E
$$

Start of an operation must follow its predecessor's completion plus the routing latency determined by placement distance.

Provenance: `abstract_inferred`. The abstract says placement distances determine routing latencies that influence scheduling; the additive form is a modeling assumption.

Abstract evidence: resulting distances between predecessor and current operations, which in turn determines routing latencies

Equation assumptions:

- Routing latency is additive between dependent operations

## eq_4: Circuit latency

$$
T=\max_{v\in V}(t_v+d_v)
$$

Makespan to be minimized by the scheduler subject to eq_3 and resource constraints.

Provenance: `standard_background`. Standard makespan definition for DAG scheduling.

Equation assumptions:

- Resource constraints handled separately

## eq_5: Generic force-directed scheduling force

$$
F(v,j)=\sum_{k}DG(k)\,\Delta p_v(k)
$$

Self-force of tentatively assigning operation v to level j, where DG is the distribution graph of resource usage per level and \Delta p_v is the change in v's probability at level k.

Provenance: `standard_background`. Classical force-directed scheduling background; the paper's modified version is not specified.

Equation assumptions:

- Classical unmodified form; the paper's modification is unknown

## Classical postprocessing

Classical compilation flow only; no quantum measurement. Output is a schedule, placement, routing and chosen ULB size.

## Algorithm steps

1. Build the quantum data flow graph and transform it to make the no-cloning constraint explicit (details not given). (no equation reference)
2. Run loose force-directed scheduling to reduce resource contention and latency. (eq_3, eq_4, eq_5)
3. Place operations by timing-driven placement, iteratively calling the scheduler to correct levels. (eq_3)
4. Route qubits to obtain dynamic routing latencies r_uv. (eq_3)
5. For each candidate ULB size, compute weighted latency and select the best size. (eq_1, eq_2)

## Assumptions

- Scope choice: a classical mapping and optimization problem with no quantum state evolution
- Linear frequency-weighted latency and additive routing delay are assumed models

## Missing information

- Actual ULB definition and architecture model
- FT code and operation latency model L(o,s)
- Modified force-directed scheduling formulas
- Placement cost function and routing algorithm
- Benchmark circuits and baseline for the 40% result
- Exact weighting formula for ULB size selection
