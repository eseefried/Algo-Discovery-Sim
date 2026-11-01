# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on a small graph with marked vertex w, H = -gamma*A - |w><w|. Use Lanczos from |s> to get a small Krylov subspace and reduced tridiagonal T, tune gamma and find t* maximizing |<w|e^{-iHt}|s>|^2, then simulate the walk on n qubits and read the marked-vertex probability.

Scope: ONE tiny instance: complete graph K_N with N=8 (n=3 qubits), marked vertex w=5 (binary 101), no ancilla, exact two-projector evolution. The star graph, broken-link complete graphs, transport efficiencies and XY-chain fidelity bound are outside scope and only sketched as Lanczos variants.

## Symbols

- $N$: number of vertices; domain: integer, power of 2, N=8
- $n$: number of vertex qubits, ceil(log2 N); domain: integer, 3
- $A$: graph adjacency matrix; domain: N x N real symmetric 0/1
- $\gamma$: hopping rate; domain: positive real
- $|w\rangle$: marked vertex state; domain: computational basis state
- $|s\rangle$: uniform superposition over vertices; domain: unit vector in C^N
- $|s_\perp\rangle$: normalized projection of |s> orthogonal to |w>; domain: unit vector in C^N
- $T$: Lanczos tridiagonal reduced Hamiltonian; domain: d x d real symmetric
- $t^*$: time of maximal success probability; domain: positive real
- $P_w$: probability of measuring w; domain: [0,1]

## eq_1: Search Hamiltonian

$$
H=-\gamma A-|w\rangle\langle w|
$$

Hamiltonian of the walk with oracle term

Provenance: `standard_background`. Standard Childs-Goldstone CTQW search Hamiltonian; the abstract mentions spatial search but does not state H.

Equation assumptions:

- Adjacency (not Laplacian) form is used

## eq_2: Complete graph adjacency

$$
A=N|s\rangle\langle s|-I,\quad H=-\gamma N|s\rangle\langle s|-|w\rangle\langle w|+\gamma I
$$

For K_N the adjacency is a rank-one projector up to identity; the identity gives only a global phase

Provenance: `standard_background`. Direct identity for complete graph.

Equation assumptions:

- Complete graph without broken links

## eq_3: Lanczos recursion

$$
\beta_{k+1}|q_{k+1}\rangle=H|q_k\rangle-\alpha_k|q_k\rangle-\beta_k|q_{k-1}\rangle,\ \alpha_k=\langle q_k|H|q_k\rangle,\ |q_0\rangle=|s\rangle,\ T_{kk}=\alpha_k,\ T_{k,k+1}=\beta_{k+1}
$$

Classical Lanczos builds the Krylov basis and tridiagonal T; stops when beta=0 (d=2 for complete graph)

Provenance: `abstract_inferred`. Abstract names Lanczos for the invariant subspace; the recursion itself is standard.

Abstract evidence: invariant subspace methods, that can be computed systematically using Lanczos algorithm

Equation assumptions:

- Exact arithmetic or numerical tolerance for beta stop

## eq_4: Reduced 2x2 resonance

$$
\gamma=1/N:\ H_{red}\simeq -\tfrac{1}{2}\mathbb{1}\cdot c-\tfrac{1}{\sqrt N}\,\sigma_x\ \text{in basis }\{|w\rangle,|s_\perp\rangle\}\ (\text{up to diagonal shifts}),\ P_w(t)=\sin^2(t/\sqrt N)\ \text{(large-N approx.)}
$$

At resonance the two-level splitting gives P_w approx 1 at t ~ (pi/2) sqrt(N); finite N=8 has corrections, so use numerics from T

Provenance: `standard_background`. Known Childs-Goldstone result; asymptotic, not exact for N=8.

Equation assumptions:

- Large-N approximation; for N=8 compute t* numerically from exact T

## eq_5: Predicted success probability

$$
P_w(t)=\left|\langle w|e^{-iHt}|s\rangle\right|^2=\left|\left(e^{-iTt}\right)_{w,s}\right|^2,\quad t^*=\arg\max_t P_w(t)
$$

Reduced-space prediction in Krylov coordinates compared with simulation; the Krylov coordinate of |w> is its overlap expressed in the basis

Provenance: `abstract_inferred`. Dynamics confined to Krylov space so reduced evolution reproduces the full amplitude.

Abstract evidence: to obtain the reduced set of states that encompass the dynamics of the problem at hand

Equation assumptions:

- |w> lies in the Krylov space of |s> under H

## eq_6: Exact circuit evolution

$$
e^{-iHt}=e^{-i\gamma t}\,e^{i\gamma N t|s\rangle\langle s|}e^{it|w\rangle\langle w|}\ \text{(exact only if the projectors commute; otherwise use PauliEvolutionGate or Trotter)}
$$

Projectors do not commute, so Trotter product with r steps approximates; |s><s| = H^n X^n C^{n-1}Z X^n H^n phase form, |w><w| = multi-controlled phase with X conjugation on zero bits of w

Provenance: `assumption`. Proposed construction; the product is only first-order Trotter, so tolerance is needed.

Equation assumptions:

- Trotter steps r large enough, or use exact PauliEvolutionGate of the Pauli decomposition of H

## Registers

- q: 3 qubits; vertex register, little-endian: vertex index = sum q_i 2^i

## Initial state

H^{\otimes 3}|000> = |s>

## Measurement

Measure all n qubits in computational basis; P_w = counts[bitstring of w]/shots, with Qiskit little-endian keys (w=5 -> '101').

## Classical postprocessing

Compare the estimated P_w with the Lanczos-reduced prediction in eq_5 within tolerance; gamma and t* chosen classically.

## Algorithm steps

1. Classically build A, H, run Lanczos from |s> to get T, d, and Krylov basis. (eq_1, eq_2, eq_3)
2. Set gamma=1/N (or tune numerically on T near the avoided crossing) and find t* maximizing P_w. (eq_4, eq_5)
3. Prepare |s> with Hadamards and apply exp(-iHt*) via PauliEvolutionGate on the Pauli decomposition of H (exact) or Trotter with enough steps. (eq_6)
4. Measure all 3 qubits and compute P_w from counts for the bitstring of w, reading keys as reversed (last char is qubit 0). (eq_5)

## Assumptions

- N=8 complete graph, w=5 chosen as the smallest instance
- Adjacency form of H, no black-box queries; oracle term is built explicitly from the known w
- Global phase gamma*t is ignored
- Exact PauliEvolutionGate preferred over Trotter

## Missing information

- Exact paper graph families, gamma values and broken-link specifics
- Laplacian vs adjacency convention in the paper
- Transport (sink/trapping) model and XY-chain bound details
- Whether the task supplies an oracle placeholder
