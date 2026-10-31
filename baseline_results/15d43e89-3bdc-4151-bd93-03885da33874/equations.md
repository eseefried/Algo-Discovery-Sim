# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Classical physical-mapping (compilation) problem for fault-tolerant quantum circuits: given a quantum data-flow graph (DFG) of logical FT operations, jointly determine (i) an operation schedule, (ii) a placement of operations onto tiles/Universal Logic Blocks (ULBs) of a 2-D physical fabric, and (iii) qubit routes with their latencies, so as to minimize total circuit latency; additionally choose a single ULB size that minimizes the critical-path-weighted latency of FT operations for a target algorithm. The abstract describes a classical optimization flow, not a quantum algorithm with a circuit to be executed; no quantum registers, initial states, or measurements are defined by it.

Scope: Scoped construction (assumption, since no experiment_scope was supplied): a symbolic specification of the three-stage flow (loose force-directed scheduling, timing-driven placement with approximate Manhattan routing latency, dynamic routing latency) plus the weighted ULB-size selection rule, instantiated on a tiny DFG with |V| = 3 operations (u -> v, u -> w) placed on a 2x2 grid of ULB sites, and a ULB-size candidate set S = {s_1, s_2} with two operation types. Numerical latency tables L_o(s), per-hop delays, and the specific modification of force-directed scheduling are NOT reconstructable from the abstract and are left symbolic. Outside scope: the exact no-cloning DFG transformation, the modified force functions, the iterative placement-scheduler interaction details, the routing algorithm, the benchmark suite, and the reported ~40% latency-reduction result (which cannot be verified or reproduced here).

## Symbols

- $G=(V,E)$: Quantum data-flow graph after the no-cloning transformation; vertices are logical FT operations, edges are qubit data dependencies (predecessor -> successor); domain: Finite directed acyclic graph
- $t_v$: Scheduled start time (control step / level) of operation v; domain: \mathbb{Z}_{\ge 0} (cycles) or \mathbb{R}_{\ge 0}
- $d_v$: Execution latency of FT operation v on the chosen ULB (depends on operation type and ULB size); domain: \mathbb{R}_{>0}
- $r_{uv}$: Routing latency to move the qubit produced by u to the location of v; domain: \mathbb{R}_{\ge 0}
- $S_v, L_v$: ASAP and ALAP start times of v (mobility interval endpoints); domain: \mathbb{Z}_{\ge 0}, S_v \le L_v
- $p_v(\tau)$: Probability that operation v is scheduled at time step \tau (uniform over its mobility interval, as in force-directed scheduling); domain: [0,1]
- $DG(\tau)$: Distribution graph: expected resource demand at time step \tau; domain: \mathbb{R}_{\ge 0}
- $F_v(t)$: Self-force of assigning operation v to time step t; domain: \mathbb{R}
- $\pi(v)$: Placement of operation v: coordinates of its assigned ULB site on the 2-D fabric; domain: \{0,\dots,W-1\}\times\{0,\dots,H-1\}
- $c_h$: Nominal latency per unit Manhattan hop of a qubit move; domain: \mathbb{R}_{>0}
- $P_{uv}$: Actual route (sequence of channel segments) found by the router for edge (u,v); domain: Path in fabric routing graph
- $\delta_e(t)$: Dynamic (time- and congestion-dependent) traversal delay of routing segment e when entered at time t; domain: \mathbb{R}_{>0}
- $T$: Total circuit latency (makespan); domain: \mathbb{R}_{>0}
- $S$: Candidate set of ULB sizes; domain: Finite set
- $O$: Set of FT operation types (e.g., CNOT, H, T, measurement, etc.); domain: Finite set
- $L_o(s)$: Latency of FT operation type o when mapped onto a ULB of size s; domain: \mathbb{R}_{>0}
- $f_o$: Occurrence frequency (count or fraction) of operation type o on critical paths of the target algorithm; domain: \mathbb{R}_{\ge 0}
- $s^*$: Selected single best ULB size; domain: S

## eq_1: Latency-minimizing scheduling with routing-aware precedence constraints

$$
\min_{\{t_v\}} \; T \quad \text{s.t.} \quad t_v \ge t_u + d_u + r_{uv} \;\; \forall (u,v)\in E, \qquad T = \max_{v\in V}\,(t_v + d_v)
$$

The schedule minimizes the makespan subject to data dependencies in the no-cloning-transformed DFG, where each precedence constraint includes the routing latency between the predecessor's and the current operation's locations. The abstract states that distances between predecessor and current operations determine routing latencies, which in turn influence the schedule; this inequality is the standard way to express that coupling.

Provenance: `abstract_inferred`. Inferred from the stated dependence of scheduling on placement/routing-derived latencies and from the objective of minimizing quantum circuit latency; makespan definition is standard scheduling background.

Abstract evidence: resulting distances between predecessor and current operations, which in turn determines routing latencies

Equation assumptions:

- Resource-capacity constraints (number of available ULBs per time step) are present but their exact form is not given in the abstract.
- The no-cloning transformation is assumed to produce a DAG in which each qubit value has a single producer and explicitly sequenced consumers; its exact rule is not specified.

## eq_2: Force-directed scheduling: distribution graph and self-force (standard background)

$$
p_v(\tau) = \frac{1}{L_v - S_v + 1}\,\mathbf{1}[S_v \le \tau \le L_v], \qquad DG(\tau) = \sum_{v\in V} p_v(\tau), \qquad F_v(t) = DG(t) - \frac{1}{L_v - S_v + 1}\sum_{\tau=S_v}^{L_v} DG(\tau)
$$

Classical force-directed scheduling (Paulin–Knight style): each operation's start time is treated as uniformly distributed over its ASAP–ALAP mobility interval; the distribution graph estimates resource contention per time step; assigning v to time t has self-force equal to the demand at t minus the average demand over its mobility window. Operations with the most negative force are fixed first, reducing contention. The abstract's 'modified' version is not recoverable.

Provenance: `standard_background`. The abstract names force-directed scheduling as the basis of the loose scheduling step; these are the textbook definitions of that method, recalled from background knowledge, not from the paper.

Equation assumptions:

- Single resource class per operation type; predecessor/successor forces (mobility-propagation terms) are omitted for brevity.
- The paper's specific modification to the force function is unknown and not represented.

## eq_3: Timing-driven placement with approximate (Manhattan) routing latency

$$
\tilde r_{uv} = c_h\,\big\|\pi(u) - \pi(v)\big\|_1, \qquad \min_{\pi}\; \sum_{(u,v)\in E} \omega_{uv}\,\tilde r_{uv}, \quad \omega_{uv} \text{ larger for timing-critical edges}
$$

Placement assigns each scheduled operation to a ULB site so as to minimize the weighted sum of approximate routing latencies estimated from grid distance; timing-driven weights emphasize edges on or near the critical path. After placement changes the estimated r_{uv}, the force-directed scheduler is re-invoked to correct scheduling levels (iteration between eq_3 and eq_1/eq_2).

Provenance: `abstract_inferred`. The abstract states that placement minimizes approximate routing latencies in a timing-driven manner; the Manhattan-distance proxy and the edge-weight form are a conventional concretization, not stated in the abstract.

Abstract evidence: uses timing-driven instruction placement to minimize the approximate routing latencies

Equation assumptions:

- 2-D grid fabric with Manhattan metric and uniform per-hop cost c_h.
- The exact definition of the timing-driven weights \omega_{uv} (e.g., slack-based) is assumed, not sourced.

## eq_4: Dynamic routing latency along the found route

$$
r_{uv} = \sum_{e\in P_{uv}} \delta_e\big(t^{\mathrm{enter}}_e\big) \;\ge\; \tilde r_{uv}
$$

The router finds an actual path P_{uv} for each qubit move; its latency is the sum of segment delays, which are dynamic because they depend on when the segment is entered (channel occupancy/congestion). The dynamic value replaces the placement-stage approximation and is fed back into the precedence constraints of eq_1.

Provenance: `abstract_inferred`. The abstract says routing produces dynamic latency values; the additive path-delay model with time-dependent segment delays is a conventional concretization of 'dynamic'.

Abstract evidence: a routing step that finds dynamic values of routing latencies for the qubits

Equation assumptions:

- Additive segment delays; congestion handled by time-dependent \delta_e rather than by an explicit conflict model.
- The inequality r_{uv} \ge \tilde r_{uv} assumes the Manhattan estimate is a lower bound (shortest path, no detours or waiting).

## eq_5: Critical-path-frequency-weighted ULB size selection

$$
s^* = \arg\min_{s\in S}\; \sum_{o\in O} f_o\, L_o(s)
$$

The single best ULB size for a target algorithm is the one minimizing the latency of FT operation types, each weighted by how often that operation type occurs on the algorithm's critical paths. L_o(s) is obtained by mapping each FT operation onto ULBs of each candidate size with the physical mapper.

Provenance: `abstract_inferred`. Directly follows from the described procedure (per-size latencies weighted by critical-path occurrence frequencies, choose the single best); the linear weighted-sum form is the natural reading but the exact aggregation (e.g., sum vs. normalized average) is not stated.

Abstract evidence: determine the single best ULB size for a target quantum circuit by examining the latency of different FT quantum operations mapped onto different ULB sizes and using information about the occurrence frequency of operations on critical paths of the target quantum algorithm to weigh these latencies

Equation assumptions:

- Linear weighted sum aggregation; weights f_o may be raw counts or normalized fractions (argmin is invariant to a common positive scaling).

## eq_6: Tiny explicit instance (assumed) for the scoped reconstruction

$$
V=\{u,v,w\},\; E=\{(u,v),(u,w)\},\; \pi(u)=(0,0),\;\pi(v)=(1,0),\;\pi(w)=(0,1) \Rightarrow \tilde r_{uv}=\tilde r_{uw}=c_h,\quad T = d_u + c_h + \max(d_v, d_w) \;\text{(if } r = \tilde r\text{)};\qquad S=\{s_1,s_2\},\; O=\{o_1,o_2\},\; s^* = \arg\min_{s\in S}\,[f_{o_1}L_{o_1}(s) + f_{o_2}L_{o_2}(s)]
$$

Smallest useful instance: a three-operation fan-out DFG (consistent with no-cloning since u produces one qubit consumed by v and another by w only if u is a two-output operation; otherwise the transformation would serialize v and w) on a 2x2 ULB grid, with symbolic latencies. Under the idealized assumption that dynamic routing latency equals the Manhattan estimate, the makespan is closed-form. The ULB-size rule is evaluated over two sizes and two operation types with symbolic inputs.

Provenance: `assumption`. No experiment_scope was provided; this instance is chosen to exercise eq_1, eq_3 and eq_5 with explicit structure while keeping all unsourced numerical values symbolic.

Equation assumptions:

- Idealized routing (r_{uv} = \tilde r_{uv}, no congestion).
- u is assumed to legitimately produce two distinct output qubits; otherwise the no-cloning transformation would force a sequential chain u -> v -> w.

## Classical postprocessing

Entire method is classical. Output is (schedule {t_v}, placement \pi, routes {P_{uv}} with latencies {r_{uv}}, makespan T) for the target circuit, plus the selected ULB size s^*. Comparison against prior work (the reported ~40% average latency reduction) requires the paper's benchmark set and baseline mapper, neither of which is available here, so that result is not reproducible from this specification.

## Algorithm steps

1. Input: logical FT quantum DFG, physical fabric dimensions W x H, candidate ULB sizes S, and FT operation latency table L_o(s). Transform the DFG so that no qubit value is implicitly duplicated (no-cloning-aware DFG G=(V,E)); exact transformation rule unknown. (eq_1)
2. Loose scheduling: compute ASAP/ALAP times, build the distribution graph, and iteratively fix operations using (modified) force-directed scheduling to reduce resource contention while minimizing makespan; initial routing latencies r_{uv} are estimates (e.g., zero or nominal). (eq_2, eq_1)
3. Timing-driven placement: assign operations to ULB sites minimizing weighted approximate Manhattan routing latency; after each placement update, re-invoke the force-directed scheduler with the updated \tilde r_{uv} to correct scheduling levels; iterate until convergence or iteration limit (criterion unknown). (eq_3, eq_2, eq_1)
4. Routing: for each edge (u,v), find a route P_{uv} on the fabric and compute its dynamic latency r_{uv}; recompute start times and total latency T from eq_1 with the dynamic values. (eq_4, eq_1)
5. ULB size selection: for each s in S, map each FT operation type o with the above flow to obtain L_o(s); extract critical-path occurrence frequencies f_o from the target algorithm; select s^* by the weighted-latency argmin. (eq_5)
6. Evaluate on the tiny assumed instance to sanity-check the pipeline symbolically. (eq_6)

## Assumptions

- No experiment_scope was supplied; the scoped tiny instance in eq_6 is the reconstructor's choice, not from the paper.
- The physical fabric is modeled as a 2-D grid of ULB sites with Manhattan distance and uniform per-hop latency c_h.
- Force-directed scheduling is taken in its textbook form; the paper's modification is unknown.
- Routing latency is additive over route segments with time-dependent segment delays.
- ULB size selection uses a linear weighted sum of per-type latencies.
- All latency values L_o(s), d_v, c_h, and frequencies f_o are left symbolic because the abstract provides no numbers.

## Missing information

- Definition and internal structure of a Universal Logic Block (code, tile layout, which FT operations it supports) and the candidate size set S.
- The exact no-cloning DFG transformation rule.
- The specific modification to force-directed scheduling (force definitions, resource model, tie-breaking, loose vs. tight scheduling distinction).
- The timing-driven placement algorithm (objective weights, move set, convergence criterion, and how often the scheduler is re-invoked).
- The routing algorithm and congestion/time model behind the 'dynamic' routing latencies.
- Numerical FT operation latency tables L_o(s) and the method for extracting critical-path occurrence frequencies f_o.
- Benchmark circuits, the 'previous work' baseline, and details behind the reported ~40% average latency reduction.
- No quantum circuit, registers, initial state, or measurement are defined by the abstract; a later circuit-generation stage would need an input DFG from elsewhere.
