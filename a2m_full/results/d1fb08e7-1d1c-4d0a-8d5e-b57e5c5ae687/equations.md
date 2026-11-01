# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Min-plus witness search: for fixed source u and target v on a tiny weighted graph with n<=8 vertices, find d'(u,v)=min_w (D[u,w]+W[w,v]) by Grover-based minimum finding (Durr-Hoyer) over the intermediate vertex index w. This is the generic primitive named in the sketch, not the paper's subcubic hybrid algorithms.

Scope: One (u,v) pair, n<=8 (index register <=3 qubits), small integer weights. The runner builds a threshold-marking Grover oracle and one or more Grover rounds, with classical threshold updating. Outside scope: the subcubic O(n^{2.5-eps}) algorithms for small integer weights, geometric weights, few weights per vertex, and earliest arrivals; the classical matrix-multiplication/sampling balancing; QRAM cost accounting; all-pairs union bound. The abstract does not give these constructions.

## Symbols

- $n$: number of vertices / candidate witnesses; domain: integer, 2<=n<=8 in simulation
- $w$: candidate intermediate vertex (witness); domain: {0,...,n-1}
- $c(w)$: candidate cost D[u,w]+W[w,v] for the fixed pair (u,v); domain: nonnegative integer
- $\tau$: current threshold (best cost found so far); domain: nonnegative integer
- $S_\tau$: set of witnesses with c(w)<\tau; domain: subset of {0..n-1}
- $m$: |S_tau|, number of marked witnesses; domain: integer 0..n
- $\theta$: Grover angle, sin^2(theta)=m/N; domain: (0,pi/2]
- $N$: 2^q, size of index space, q=ceil(log2 n); domain: power of 2

## eq_1: Min-plus witness definition

$$
d'(u,v)=\min_{w\in\{0,\dots,n-1\}}\bigl(D[u,w]+W[w,v]\bigr)
$$

Target quantity per pair, found as minimum over witnesses.

Provenance: `abstract_inferred`. The n^3 trivial algorithm and n^2.5 Grover search over n witnesses per pair imply this min-plus form; the exact formula is from the sketch and standard background.

Abstract evidence: The trivial classical algorithm for APSP and most all pairs path problems runs in $O(n^{3})$ time

Equation assumptions:

- Fixed pair (u,v); D and W given as classical tables

## eq_2: Threshold marking oracle

$$
O_\tau|w\rangle=(-1)^{[c(w)<\tau]}|w\rangle
$$

Phase oracle marking witnesses strictly better than the threshold; the value and compare ancillas are uncomputed to |0>. For tiny instances, the runner may implement it as multi-controlled Z on index bit patterns in S_tau, computed classically from the table (the table is known to the builder in simulation).

Provenance: `assumption`. Proposed construction following the sketch's compare-and-flip oracle; the abstract gives no circuit.

Equation assumptions:

- Costs c(w) available to the oracle via lookup (QRAM assumption)
- In the simulation, S_tau is encoded by the builder; a real hidden black box would be a placeholder

## eq_3: Grover iterate and success probability

$$
G=(2|s\rangle\langle s|-I)O_\tau,\; |s\rangle=H^{\otimes q}|0\rangle,\; P_k=\sin^2\bigl((2k+1)\theta\bigr),\; \sin^2\theta=m/N
$$

After k iterations on the uniform superposition, measuring the index gives a marked witness with probability P_k. Optimal k is about floor(pi/(4 theta)).

Provenance: `standard_background`. Standard Grover analysis; the abstract only mentions Grover search.

Equation assumptions:

- Indices w>=n are never marked, and N=2^q may exceed n

## eq_4: Threshold update rule

$$
\tau_{t+1}=c(w_t)\text{ if }c(w_t)<\tau_t\text{ else }\tau_t;\quad \tau_0=c(w_0)\text{ for random }w_0
$$

Durr-Hoyer loop: measure w_t after k_t random-bounded Grover iterations, verify classically, and lower the threshold. Stop when no improvement for a fixed number of rounds, or about 22.5 sqrt(n)+1.4 log^2 n total iterations in the original analysis.

Provenance: `standard_background`. Durr-Hoyer minimum finding, named in the sketch; constants are recalled, not from the abstract.

Equation assumptions:

- Random k_t drawn uniformly from {0..ceil(sqrt(N))-1} or growing schedule

## eq_5: Query complexity target

$$
T_{\text{pair}}=\tilde O(\sqrt n),\quad T_{\text{APSP,trivial}}=n^2\tilde O(\sqrt n)=\tilde O(n^{2.5})
$$

The trivial quantum bound the paper improves to O(n^{2.5-eps}) for structured inputs.

Provenance: `abstract_explicit`. The abstract states the trivial bound; the per-pair sqrt(n) split is the natural reading.

Abstract evidence: the trivial algorithm in the quantum setting runs in $\tilde{O}(n^{2.5})$ time, using Grover search

## Registers

- idx: q=ceil(log2 n) (<=3) qubits; witness index w, little-endian: qubit i is bit i of w
- val: O(log(nW)), omitted in tiny instances if the oracle is compiled from the table qubits; candidate cost register for the adder-based oracle
- flag: 1 (optional) qubits; compare ancilla, returned to |0>
- creg: q qubits; classical bits measuring idx; counts key last char is bit 0

## Initial state

|0>^{q} on idx (ancillas |0>), then H on every idx qubit to give the uniform superposition over w.

## Measurement

Measure only the idx qubits, one round per circuit; bit i of w corresponds to classical bit i.

## Classical postprocessing

Verify each measured witness against the table, track the minimum, and output the final threshold and its witness; stop after a fixed number of non-improving rounds.

## Algorithm steps

1. Classically choose the initial threshold tau_0=c(w_0) for random w_0 (or w_0=0). (eq_4)
2. Build the circuit: H on idx, then k repetitions of oracle O_tau followed by diffusion (H, X, multi-controlled Z, X, H) on idx; measure idx into creg. (eq_2, eq_3)
3. Read the measured w (reverse the counts string for bit order), classically verify c(w)<tau, and update tau. (eq_4)
4. Repeat with fresh random k until m=0 is reached or the iteration budget is exhausted. The final tau is d'(u,v). (eq_4, eq_1)

## Assumptions

- Scope choice: a single pair (u,v), n<=8, instead of full APSP.
- The oracle is compiled from the classical table, since the true QRAM and black box are unavailable.
- If the runner supplies a hidden black box, the oracle must be a placeholder call, and only the threshold comparison is built around it.
- Ties are broken by strict inequality c(w)<tau.

## Missing information

- Actual subcubic constructions: small-integer-weight hybrid with threshold parameter, geometric weights, few-weights-per-vertex, earliest arrivals
- Cost balance and the value of eps
- Exact oracle interface and query budget of the runner
- Handling of unknown m (exponential search schedule) beyond the standard recalled loop
