# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk search on a graph with self-loops, H = -gamma*A - |w><w|, simulated by a second-order Trotter product formula on the hypercube (n=2 or 3 qubits) to estimate the marked-vertex success probability. The abstract's diagrammatic degenerate-perturbation-theory method is not reconstructed.

Scope: One tiny instance: hypercube Q_n with n=3 (N=8) and a single phase-oracle query per Trotter step. Gamma is scanned numerically, T is near pi*sqrt(N)/2, and the readout is the marked-string probability. Out of scope: the diagrammatic method, the weighted-loop graphs, and the proof of search in a subspace whose dimension grows with N.

## Symbols

- $n$: number of vertex qubits; domain: integer, 2 or 3
- $N=2^n$: number of vertices; domain: 4 or 8
- $\gamma$: hopping rate; domain: positive real, scanned
- $A=\sum_i X_i$: hypercube adjacency; domain: operator on n qubits
- $w$: marked vertex (bit string); domain: {0,1}^n
- $dt$: Trotter step size, T/r; domain: positive real
- $r$: number of Trotter steps; domain: positive integer
- $O_w$: phase oracle I-2|w><w|, the opaque gate; domain: unitary

## eq_1: Search Hamiltonian

$$
H=-\gamma A-|w\rangle\langle w|
$$

Hamiltonian for continuous-time search on a graph with adjacency A; self-loops would add diagonal terms.

Provenance: `assumption`. Standard CTQW search form (Childs-Goldstone). The abstract names only continuous-time search on graphs with self-loops, not this exact H.

Equation assumptions:

- The hypercube replaces the paper's weighted loop graphs.
- Loop weights are zero in this instance.

## eq_2: Oracle step identity

$$
e^{i\,dt\,|w\rangle\langle w|}=I+(e^{i\,dt}-1)|w\rangle\langle w|=e^{i\,dt/2}e^{-i\,dt\,O_w/2}
$$

Since |w><w|=(I-O_w)/2, the oracle factor is e^{i dt/2} times e^{-i dt O_w/2}. Implementing it with one oracle call needs a controlled-O_w, or an ancilla phase kick built from one oracle call.

Provenance: `standard_background`. Algebra from O_w=I-2|w><w|. The e^{i dt/2} prefactor is a global phase.

Equation assumptions:

- The placeholder oracle can be controlled by one reserved qubit, giving n+1 qubits total.
- The sign of the exponent follows from e^{-iHdt}, which contains e^{+i dt |w><w|}.

## eq_3: Second-order Trotter step

$$
U\approx\left(e^{i\gamma A\,dt/2}\,e^{i\,dt|w\rangle\langle w|}\,e^{i\gamma A\,dt/2}\right)^r,\quad e^{i\gamma A\,dt/2}=\bigotimes_i R_X(-\gamma\,dt)
$$

Symmetric product formula for e^{-iHT} with T=r dt. The hopping half-step is a layer of RX gates, since RX(theta)=exp(-i theta X/2), so theta=-gamma*dt.

Provenance: `standard_background`. Strang splitting; the X terms commute, so the hopping layer is exact.

Equation assumptions:

- Trotter error is O(dt^2) and is controlled by large r.

## eq_4: Initial state

$$
|s\rangle=H^{\otimes n}|0\rangle^{\otimes n}=N^{-1/2}\sum_x|x\rangle
$$

Uniform superposition, the ground state of -A.

Provenance: `standard_background`. Standard CTQW search start state.

## eq_5: Success probability

$$
P_{\rm succ}(T)=|\langle w|U(T)|s\rangle|^2
$$

Marked-string probability, maximized over gamma and T.

Provenance: `assumption`. The sketch defines success as the marked-vertex probability at an optimal time.

Equation assumptions:

- gamma is near a critical value, to be found numerically; the 1/N value in the sketch is unverified.

## Registers

- v: n qubits; vertex register, little-endian integer encoding (qubit i is bit i of x)
- a: 1 qubits; optional ancilla that controls the oracle; return it to |0>

## Initial state

All qubits |0>, then H on each vertex qubit.

## Measurement

Measure the n vertex qubits in the computational basis. The marked string is read with qubit 0 as the last character of the counts key. The ancilla is not measured.

## Classical postprocessing

Estimate P_succ from counts, or from the statevector if allowed. Sweep gamma and T and report the peak probability and its time.

## Algorithm steps

1. Apply H to every vertex qubit to prepare |s>. (eq_4)
2. Repeat r times: RX layer for half a hopping step, one oracle-phase step with dt, RX layer for half a hopping step. (eq_2, eq_3)
3. Measure the vertex qubits only. Read the count of the marked string, taking care with little-endian key order. Scan gamma and T to maximize the probability. (eq_5)

## Assumptions

- Hypercube with zero loop weights stands in for the paper's weighted loop graphs.
- N=8 is the instance.
- One oracle query per Trotter step, with a controlled-oracle ancilla.
- The Hamiltonian sign convention is H=-gamma*A-|w><w|.

## Missing information

- The paper's actual graphs and loop weights.
- The diagrammatic perturbation-theory rules.
- The critical gamma and run time for the paper's graphs.
- How the growing-dimension subspace is used.
- The query budget.
