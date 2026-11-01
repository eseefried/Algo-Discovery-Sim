# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on a small graph with N<=16 vertices, N a power of two, one marked vertex w behind a phase oracle. Compare a single-stage walk at gamma near critical value with a two-stage schedule (gamma1 for T1, then gamma2 for T2). Success is the marked-vertex probability |<w|U|s>|^2.

Scope: One tiny instance, N=8 or 16 vertices on 3 or 4 qubits with no ancillas. A generic walk Hamiltonian H=-gamma*A-|w><w| is simulated by first-order Trotterization with a fixed number of steps. The two-stage schedule applies two successive (gamma,T) pairs. Outside scope: the paper's actual two graph families, their analytic gap and critical gamma values, the exact stage times, and the connectivity-versus-speed scaling analysis.

## Symbols

- $N$: number of vertices; domain: integer, power of two, <=16
- $n$: number of vertex qubits, n=log2 N; domain: integer 3 or 4
- $A$: graph adjacency matrix; domain: N x N real symmetric 0/1
- $\gamma$: walking rate (hopping amplitude); domain: positive real
- $w$: marked vertex index; domain: {0,...,N-1}
- $|s\rangle$: uniform superposition over vertices; domain: state in C^N
- $\gamma_1,\gamma_2,T_1,T_2$: rates and durations of stage 1 and stage 2; domain: positive reals, chosen by scan
- $r$: number of Trotter steps per stage; domain: positive integer
- $P$: success probability of measuring w; domain: [0,1]

## eq_1: Search Hamiltonian

$$
H(\gamma)=-\gamma A-|w\rangle\langle w|
$$

Walk Hamiltonian with graph hopping term and oracle term. The abstract only says the walk evolves by Schrödinger's equation, so this form is the standard Childs-Goldstone one.

Provenance: `standard_background`. Standard continuous-time quantum search Hamiltonian. The abstract does not state it.

Equation assumptions:

- Adjacency matrix rather than Laplacian
- Sign convention is assumed

## eq_2: Two-stage evolution

$$
U=e^{-iH(\gamma_2)T_2}\,e^{-iH(\gamma_1)T_1}
$$

Two successive walks with different walking rates. This is the form of a two-stage algorithm in which the walking rate is adjusted.

Provenance: `abstract_inferred`. The abstract says the rate is adjusted between two stages. The number of stages is taken as two, with fixed durations.

Abstract evidence: a novel two-stage quantum walk algorithm in which the walking rate must be adjusted to yield high search probability

Equation assumptions:

- Sudden switch of gamma
- T1,T2 are free parameters

## eq_3: Success probability

$$
P=|\langle w|U|s\rangle|^2,\quad |s\rangle=N^{-1/2}\sum_{v}|v\rangle
$$

Probability of reading out the marked vertex from the uniform start state.

Provenance: `standard_background`. Standard figure of merit for spatial search.

Equation assumptions:

- Start state is uniform

## eq_4: Trotter step

$$
e^{-iH(\gamma)t}\approx\left(e^{i\gamma A t/r}\,e^{i|w\rangle\langle w|t/r}\right)^r
$$

First-order Trotter product. The oracle phase is a controlled phase on |w>, one query per step. For a hypercube, A=sum_j X_j, so e^{i\gamma A t/r}=prod_j RX_j(-2\gamma t/r).

Provenance: `assumption`. The sketch proposes Trotterization or an exact decomposition. The oracle must be inserted as a placeholder phase gate.

Equation assumptions:

- Trotter error is small for large r
- Oracle phase angle t/r is realised through the black box or a fixed-phase variant
- Hypercube factorization applies only if the graph is a hypercube

## eq_5: Optimal-time scaling check

$$
T_{opt}(N)=\arg\max_T P(T),\quad T_{opt}\sim c\sqrt{N}\ \text{in the fast case}
$$

Scan T (and gamma) at several N and fit T_opt against sqrt(N). This is a claim for the fast-search example, not a verified result.

Provenance: `abstract_inferred`. O(sqrt N) is the benchmark runtime for fast search, taken here as the target for the low-connectivity fast-search example.

Abstract evidence: searches on $d$-dimensional cubic lattices in $O(\sqrt{N})$ time when $d\geq 5$

Equation assumptions:

- N is too small to see asymptotics reliably

## Registers

- v: n=ceil(log2 N), at most 4 qubits; vertex index register, little-endian binary encoding of the vertex label, no ancillas

## Initial state

Apply H to every qubit of v starting from |0...0> to get |s>.

## Measurement

Measure all n vertex qubits in the computational basis. Qiskit is little-endian, so the last character of the counts key is qubit 0, and w must be matched in that order. Estimate P as the frequency of w.

## Classical postprocessing

Choose gamma1, gamma2, T1, T2 by grid scan to maximize P. Fit T_opt versus sqrt(N). Compute vertex, edge, algebraic and normalized algebraic connectivity of the graph and compare with speed.

## Algorithm steps

1. Prepare |s> with Hadamards on all vertex qubits. (eq_3)
2. Stage 1: run r Trotter steps of the walk at gamma1 for total time T1. Each step applies the graph term, then the oracle phase placeholder. (eq_1, eq_4)
3. Stage 2 (two-stage case only): switch to gamma2 and run r Trotter steps for total time T2. Single-stage case sets T2=0. (eq_2, eq_4)
4. Classically sweep gamma and T and fit T_opt versus N. Compare with connectivity measures. (eq_5)

## Assumptions

- N<=16, a power of two, to fit the qubit cap
- Marked vertex w is given by a phase oracle black box
- Graph A is a small stand-in graph such as a hypercube or a complete-graph pair with a bridge, because the paper's exact graphs are unknown
- First-order Trotterization with enough steps stands in for exact evolution
- Stage times and rates are numerically scanned, not analytic

## Missing information

- Exact graph constructions of the two examples
- Critical gamma values and stage durations
- Which stage targets which intermediate subspace
- Query budget limit and how many Trotter steps fit it
- Whether the oracle is exp(it|w><w|) with a free angle or only a fixed sign flip
