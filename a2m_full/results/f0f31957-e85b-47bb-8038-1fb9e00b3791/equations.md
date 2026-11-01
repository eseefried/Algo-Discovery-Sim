# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Classical quantum physical mapping (scheduling, placement, routing, ULB sizing) with a small testable circuit realization: a Clifford+T circuit mapped onto a line or grid of qubits via SWAP routing, verified by statevector equality up to qubit permutation.

Scope: One tiny instance: a 3-4 qubit Clifford+T circuit (e.g. H, T, CX gates) on a 2x2 or 1x4 grid. Build a QDFG, compute ASAP/ALAP slack, apply one pass of force-directed scheduling, place logical qubits on grid nodes, and route non-adjacent CX gates with SWAPs (3 CX each). Not covered: the ULB internals, FT code latencies, simulated-annealing placement iteration, congestion-aware routing, and the ULB size search except as a weighted-sum formula. The 40% latency result is not reproduced.

## Symbols

- $G=(V,E)$: quantum dataflow graph; nodes are operations, edges are qubit values; domain: DAG
- $\ell_v^{ASAP},\ell_v^{ALAP}$: earliest and latest level of operation v; domain: nonnegative integers
- $s_v$: slack of operation v; domain: nonnegative integers
- $DG_t(k)$: distribution graph: expected number of type-k operations at level t; domain: nonnegative reals
- $F_v(t)$: total force of placing v at level t; domain: real
- $d(p_u,p_v)$: Manhattan distance between tiles of operations u and v; domain: nonnegative integers
- $w_e$: criticality weight of edge e, derived from slack; domain: positive reals
- $\tau$: per-hop move latency; domain: cycles, given
- $\pi$: qubit permutation accumulated by SWAP routing; domain: permutations of n qubits
- $L_o(b), f_o$: latency of FT operation o for ULB size b; frequency of o on critical paths; domain: cycles; nonnegative reals

## eq_1: Slack

$$
s_v=\ell_v^{ALAP}-\ell_v^{ASAP}
$$

Time frame width of each operation in the QDFG; the candidate levels are ASAP..ALAP.

Provenance: `abstract_inferred`. Force-directed scheduling operates on time frames defined by ASAP/ALAP levels; the formula is standard, not stated in the abstract.

Abstract evidence: performs instruction scheduling based on a modified force-directed scheduling approach

Equation assumptions:

- Unit-latency levels, or latencies given as inputs

## eq_2: Distribution graph and force

$$
DG_t(k)=\sum_{v:\,type(v)=k}\frac{\mathbf 1[\ell_v^{ASAP}\le t\le \ell_v^{ALAP}]}{s_v+1},\quad F_v(t)=\sum_{t'}DG_{t'}(k)\,\Delta p_v(t')+F^{pred}_v(t)+F^{succ}_v(t)
$$

Self force from the distribution graph plus predecessor and successor forces. Fix the (v,t) pair with the lowest force, then update time frames.

Provenance: `standard_background`. Classic force-directed scheduling (Paulin-Knight); the paper's modification is unknown.

Equation assumptions:

- Paper's modification not reproduced
- Delta p_v(t') is the change in v's occupancy probability at t'

## eq_3: Timing-driven placement cost

$$
C(p)=\sum_{(u,v)\in E} w_{uv}\,d(p_u,p_v),\quad w_{uv}=\frac{1}{1+\min(s_u,s_v)},\quad \hat r_{uv}=\tau\,d(p_u,p_v)
$$

Placement minimizes the criticality-weighted Manhattan wirelength. The routing latency estimate is fed back to rescheduling.

Provenance: `assumption`. The abstract mentions timing-driven placement and approximate routing latencies; the specific weight form is my choice.

Equation assumptions:

- Weight 1/(1+slack) is a chosen form
- Latency proportional to Manhattan distance

## eq_4: SWAP routing and correctness criterion

$$
\mathrm{SWAP}=\mathrm{CX}_{ab}\mathrm{CX}_{ba}\mathrm{CX}_{ab},\quad |\psi_{map}\rangle=P_\pi|\psi_{orig}\rangle,\quad F=|\langle\psi_{orig}|P_\pi^\dagger|\psi_{map}\rangle|^2=1
$$

Routing is implemented with SWAPs, and the mapped state must equal the original state up to the final permutation.

Provenance: `assumption`. Circuit realization of routing chosen for testability; the abstract states no such relation.

Equation assumptions:

- Little-endian qubit ordering
- P_pi maps logical qubit i to its final physical position

## eq_5: Weighted ULB size selection

$$
b^*=\arg\min_{b}\sum_{o} f_o\,L_o(b)
$$

Pick the single ULB size minimizing the critical-path-frequency-weighted latency of FT operations.

Provenance: `abstract_inferred`. The weighted-sum form is inferred from the described weighting of latencies by frequency.

Abstract evidence: using information about the occurrence frequency of operations on critical paths of the target quantum algorithm to weigh these latencies

Equation assumptions:

- Normalized weights f_o
- L_o(b) given as input

## Registers

- q: n=3 or 4 (physical qubits on the grid, one per logical qubit) qubits; data qubits; the SWAP network permutes their contents; no ancillas

## Initial state

|0...0>, with the input circuit's Clifford+T gates applied to produce the reference state

## Measurement

None; the statevector is read directly, with no measurements.

## Classical postprocessing

Compute total latency in cycles, undo the permutation on the mapped statevector, compute the fidelity, and evaluate the argmin over ULB sizes.

## Algorithm steps

1. Build the QDFG from the small circuit, with serialization edges for multi-consumer values (no-cloning), and compute ASAP/ALAP levels and slack. (eq_1)
2. Run force-directed scheduling: compute forces, fix the lowest-force operation, update time frames, repeat. (eq_2)
3. Place logical qubits on grid nodes by minimizing the weighted Manhattan cost; add the routing latency estimate and reschedule until stable. (eq_3)
4. Route non-adjacent two-qubit gates by inserting SWAPs (3 CX each) along the shortest path, tracking the permutation; the actual latency is the schedule length plus the routing latency. (eq_4)
5. Compare the mapped and original statevectors after undoing the permutation; optionally compute the ULB size choice from given latencies. (eq_4, eq_5)

## Assumptions

- The testable circuit is only a correctness check of a classical compiler
- Tiny instance: 4 qubits on a 1x4 line with a few non-adjacent CX gates
- Operation and ULB latencies are given inputs
- No oracle or black box is used, so the query budget is zero

## Missing information

- Paper's exact force modification and QDFG construction
- ULB architecture and latencies
- Placement algorithm details
- Routing congestion model
- Benchmark circuits
