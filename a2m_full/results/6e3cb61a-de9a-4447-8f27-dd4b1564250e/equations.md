# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Search for a single marked vertex on a small regular lattice (assumed: cycle or 2D torus with N=2^n vertices) with a discrete-time quantum walk that applies k walk steps W per oracle query; compare the query count T with the number of walk steps k*T. Output: the marked-vertex probability and the T,k that maximize it.

Scope: One smallest instance: a cycle with N=8 (n=3 vertex qubits) and a 1-qubit coin (a 2D torus with N=16 and a 2-qubit coin is optional), one marked vertex m. The circuit applies the placeholder phase-flip oracle once per iteration, then k coin-reflection and shift steps. T and k are scanned numerically. Not covered: the paper's exact walk, its spectral-gap analysis, the proof of the cubic speedup over the classical hitting time, the continuous-time walk comparison, and asymptotic scaling.

## Symbols

- $n$: number of vertex qubits; domain: positive integer, assumed 3
- $N$: number of vertices, 2^n; domain: positive integer
- $m$: marked vertex; domain: integer in 0..N-1
- $\epsilon$: marked fraction 1/N; domain: (0,1)
- $k$: walk steps per oracle query; domain: positive integer, tuned
- $T$: number of iterations (= oracle queries); domain: positive integer, tuned
- $O$: oracle phase flip on marked vertex, acting as identity on the coin; domain: unitary
- $W$: walk step: coin reflection C followed by shift S; domain: unitary on vertex+coin
- $\delta$: spectral gap of the walk; domain: positive real
- $\theta$: effective rotation angle per iteration in the 2D invariant subspace; domain: (0,pi/2)

## eq_1: Oracle

$$
O=I-2\,|m\rangle\langle m|\otimes I_{coin}
$$

Phase flip of the marked vertex, one query per placement. The runner substitutes the real gate for the placeholder.

Provenance: `assumption`. The sketch specifies a phase-flip oracle. Its exact form and placement are assumed.

Equation assumptions:

- single marked vertex
- coin register untouched by the oracle

## eq_2: Walk step

$$
W=S\,(I_{vertex}\otimes(2|s_c\rangle\langle s_c|-I)),\quad S|v,c\rangle=|v+d_c,c\rangle
$$

Grover-coin reflection followed by a coin-controlled shift. For the cycle, d_c=±1 mod N. For the torus, d_c is one of ±e_x, ±e_y.

Provenance: `standard_background`. Standard Ambainis-style coined walk. The paper's exact walk is unknown.

Equation assumptions:

- s_c is the uniform coin state
- for a 1-qubit coin the Grover coin reduces to X, so a Hadamard-based coin may be needed to avoid a trivial walk

## eq_3: Iteration and final state

$$
|\psi_T\rangle=\big(W^{k}O\big)^{T}|s\rangle|s_c\rangle,\quad |s\rangle=H^{\otimes n}|0\rangle
$$

T iterations, each with one query and k free walk steps, starting from the uniform state.

Provenance: `abstract_inferred`. The abstract's multi-step variant takes k walk steps per query, so each iteration is W^k O.

Abstract evidence: a discrete-time walk typically performs one walk step per oracle query

Equation assumptions:

- initial coin state is uniform

## eq_4: Rotation heuristic

$$
\theta\approx\sqrt{k\,\epsilon},\quad T\approx\frac{\pi}{4\theta},\quad k\sim 1/\delta
$$

Heuristic from the sketch: the rotation angle per query grows with k up to about the inverse gap. The sketch notes 'or better', so this is not exact.

Provenance: `assumption`. Taken from the sketch only. k and T are to be tuned numerically, not derived.

Equation assumptions:

- analysis restricted to the span of the uniform and marked states
- approximate

## eq_5: Success probability

$$
P(T,k)=\sum_{c}\big|\langle m,c|\psi_T\rangle\big|^2
$$

Probability of measuring the marked vertex, summed over coin states. Choose (T,k) to maximize it.

Provenance: `standard_background`. Born rule on the vertex register.

## Registers

- vertex: n=3 qubits; vertex position, little-endian integer encoding v=sum_i b_i 2^i
- coin: 1 (cycle) or 2 (torus) qubits; direction register for the coined walk
- flag: 1 (optional) qubits; oracle ancilla, returned to |0>. Not needed if the oracle acts directly as a phase flip.

## Initial state

H on all vertex qubits, coin in the uniform superposition (H on coin qubits), flag in |0>.

## Measurement

Measure only the vertex qubits. Qiskit is little-endian, so the vertex integer is read from bits[::-1] with bit i from measure(i,i). Do not measure the coin or flag.

## Classical postprocessing

Take the most frequent vertex outcome and check it against m. Choose the (T,k) with the largest marked-vertex frequency. The number of queries is T.

## Algorithm steps

1. Prepare the uniform state on the vertex and coin registers. (eq_3)
2. For each of T iterations, place one oracle placeholder on the vertex register (one query). (eq_1)
3. Apply k walk steps W (coin reflection then shift via controlled increment/decrement), counted in depth but not in queries. (eq_2)
4. Scan T and k classically on small instances and pick the peak of P(T,k). Pick k near 1/delta and T near pi/(4 sqrt(k eps)) as the starting guess. (eq_4, eq_5)

## Assumptions

- small cycle or torus, single marked vertex
- k chosen from the known gap and tuned numerically
- oracle is a phase-flip placeholder, one query per iteration
- walk steps are free in queries but counted in depth
- qubit cap allows vertex + coin + at most one ancilla

## Missing information

- the paper's exact walk (Szegedy vs coined) and graph family
- the exact relation between k, the gap and the oracle strength
- whether the oracle acts on the coin
- the runner's query budget and qubit cap
- evidence that the cubic speedup shows up at tiny N
