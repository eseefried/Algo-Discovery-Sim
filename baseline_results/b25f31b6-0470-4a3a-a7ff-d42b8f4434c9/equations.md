# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Spatial search by continuous-time quantum walk (Schrödinger evolution under a graph Hamiltonian plus a marked-vertex oracle) on graphs whose connectivity does not predict search speed; the abstract claims one low-connectivity graph with O(sqrt(N)) search and one high-connectivity graph with slow search, the latter requiring a two-stage walk with an adjusted walking rate (jumping rate) gamma.

Scope: Reconstruct only the generic continuous-time quantum-walk search framework (Schrödinger evolution under H = -gamma*A - |w><w| from the uniform superposition, success probability at the marked vertex) and a parametrized two-stage template in which gamma and evolution time are changed once. Because the abstract does not define the two specific graphs, the connectivity measures' values, or the stage parameters, a tiny explicit sanity instance is chosen as an ASSUMPTION: the complete graph K_4 (N=4, 2 qubits, single stage with gamma=1/N). Outside scope: the paper's actual two example graphs, their adjacency/Laplacian spectra, the degenerate-perturbation-theory analysis yielding optimal gamma values and runtimes, the proof of slow search on the high-connectivity example, and the specific values of (gamma_1,t_1,gamma_2,t_2) for the two-stage algorithm.

## Symbols

- $G=(V,E)$: Simple undirected graph on which the walk takes place; domain: finite graph, |V|=N
- $N$: Number of vertices (search space size); domain: positive integer; N=4 in the assumed instance
- $|v\rangle$: Computational-basis state labelling vertex v, encoded as the binary expansion of an integer index 0..N-1 on n=\lceil\log_2 N\rceil qubits (qubit 0 = least significant bit); domain: orthonormal basis of \mathbb{C}^N
- $A$: Adjacency matrix of G, A_{uv}=1 if {u,v}\in E else 0; domain: N\times N symmetric 0/1 matrix
- $L$: Graph Laplacian L = D - A with D the degree matrix; domain: N\times N real symmetric PSD matrix
- $\gamma$: Walking (jumping) rate multiplying the graph term of the Hamiltonian; domain: \gamma>0 real
- $|w\rangle$: Marked (target) vertex state; domain: one of the basis states |v\rangle
- $|s\rangle$: Uniform superposition over all vertices (initial state); domain: unit vector in \mathbb{C}^N
- $H(\gamma)$: Search Hamiltonian for walking rate \gamma; domain: N\times N Hermitian matrix
- $t, t_1, t_2$: Evolution times (total, stage 1, stage 2); domain: non-negative reals
- $\gamma_1,\gamma_2$: Walking rates in stage 1 and stage 2 of the two-stage algorithm; domain: positive reals (values not given by abstract)
- $p(t)$: Success probability of measuring the marked vertex at time t; domain: [0,1]
- $d$: Lattice dimension in the motivating cubic-lattice result; domain: positive integer

## eq_1: Schrödinger evolution of the walker

$$
i\,\frac{d}{dt}|\psi(t)\rangle = H|\psi(t)\rangle, \qquad |\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle \ (\hbar=1,\ H\ \text{time-independent within a stage})
$$

Continuous-time quantum walk dynamics: the state evolves unitarily under a time-independent Hamiltonian; exact equality (no approximation).

Provenance: `abstract_explicit`. The abstract states the particle evolves by Schrödinger's equation; the closed form e^{-iHt} is the exact solution for a time-independent H.

Abstract evidence: A randomly walking quantum particle evolving by Schrödinger’s equation

Equation assumptions:

- Units with \hbar = 1
- H is constant within each stage

## eq_2: Continuous-time quantum-walk search Hamiltonian

$$
H(\gamma) = -\gamma A - |w\rangle\langle w|
$$

Childs–Goldstone-type search Hamiltonian: graph kinetic term with walking rate gamma plus a marked-vertex oracle term. For regular graphs, using -gamma L instead of -gamma A differs only by a multiple of the identity (global phase), so success probabilities are identical.

Provenance: `standard_background`. Standard continuous-time quantum walk search Hamiltonian; the abstract's 'walking rate' corresponds to gamma. The paper's exact choice (A vs L, sign conventions) is not stated in the abstract.

Equation assumptions:

- Adjacency-matrix form chosen; Laplacian form equivalent for regular graphs only
- Single marked vertex

## eq_3: Initial uniform superposition

$$
|s\rangle = \frac{1}{\sqrt{N}}\sum_{v\in V}|v\rangle, \qquad |\psi(0)\rangle = |s\rangle
$$

The walk starts in the equal superposition over all vertices (no knowledge of w). For N=2^n this is H^{\otimes n}|0\rangle^{\otimes n}.

Provenance: `standard_background`. Standard initial state for quantum-walk spatial search; it is the unique state symmetric under all vertex permutations.

Equation assumptions:

- N is a power of two in the circuit instance so that Hadamards prepare |s\rangle exactly

## eq_4: Success probability

$$
p(t) = \left|\langle w|e^{-iH(\gamma)t}|s\rangle\right|^2
$$

Probability that a computational-basis measurement at time t yields the marked vertex; exact for the single-stage walk.

Provenance: `standard_background`. Born rule applied to the walker state after evolution; this is the quantity whose growth to Theta(1) in time O(sqrt N) defines 'fast search' in the abstract.

## eq_5: Two-stage walk with adjusted walking rate (template)

$$
|\psi_{\mathrm{final}}\rangle = e^{-iH(\gamma_2)t_2}\,e^{-iH(\gamma_1)t_1}\,|s\rangle, \qquad p_{\mathrm{final}} = |\langle w|\psi_{\mathrm{final}}\rangle|^2, \quad \gamma_1\neq\gamma_2
$$

Piecewise-constant schedule: evolve under the search Hamiltonian with rate gamma_1 for time t_1, then with rate gamma_2 for time t_2. The abstract gives no values for (gamma_1,t_1,gamma_2,t_2) nor the graph; this equation only fixes the structure.

Provenance: `abstract_inferred`. Inferred from the abstract's description of a two-stage algorithm with an adjusted walking rate: the natural reading is two consecutive Schrödinger evolutions (eq_1, eq_2) with different gamma. The exact stage parameters and target graph are paper content not available here.

Abstract evidence: a novel two-stage quantum walk algorithm in which the walking rate must be adjusted to yield high search probability

Equation assumptions:

- Exactly two piecewise-constant stages with the same oracle term
- Stage boundary is a sharp switch (no ramp)
- Values of gamma_1,gamma_2,t_1,t_2 and the graph are unspecified

## eq_6: Fast-search criterion (runtime scaling)

$$
T_{\mathrm{search}} = O(\sqrt{N}) \ \text{with}\ p(T_{\mathrm{search}}) = \Theta(1)
$$

Definition of 'fast' search used to classify the examples: constant success probability reached in time scaling as the square root of the number of vertices (asymptotic statement, not exact equality).

Provenance: `abstract_explicit`. The abstract uses O(sqrt N) time as the benchmark for fast quantum search; the Theta(1) success-probability requirement is the standard accompanying condition.

Abstract evidence: searches on $d$-dimensional cubic lattices in $O(\sqrt{N})$ time when $d\geq 5$

Equation assumptions:

- Success probability requirement Theta(1) added as standard convention; amplitude amplification/repetition overhead not counted

## eq_7: Assumed tiny sanity instance: complete graph K_4

$$
G=K_4,\ N=4,\ A=J-I,\ \gamma=\tfrac{1}{N}=\tfrac14,\ |w\rangle=|0\rangle,\ t^{*}=\tfrac{\pi}{2}\sqrt{N}=\pi,\ p(t^{*})=1 \ (\text{single stage},\ \gamma_1=\gamma_2)
$$

Explicit instance for later circuit generation: 2 qubits, H = -(1/4)(J-I) - |00><00|, where J is the all-ones matrix. On the complete graph with gamma=1/N the walk reaches the marked vertex with probability 1 at t=(pi/2)sqrt(N) (standard result). This instance is NOT one of the paper's two example graphs; it only validates the framework.

Provenance: `assumption`. The abstract does not define its example graphs, so a smallest nontrivial, analytically known instance is chosen to make the specification concrete. The K_N result (gamma=1/N, t=pi sqrt(N)/2, p=1) is standard background recalled from knowledge.

Equation assumptions:

- Instance chosen by the reconstruction agent, not from the paper
- Marked vertex fixed to index 0 without loss of generality by vertex transitivity of K_4

## Registers

- vertex: n = \lceil \log_2 N \rceil (2 qubits for the assumed N=4 instance) qubits; Holds the walker's position as the binary index of a vertex; qubit 0 is the least significant bit of the vertex index.
- ancilla (optional): 0 to a few qubits, implementation dependent qubits; Only if the Hamiltonian simulation method (e.g., LCU/block-encoding) requires it; not needed for exact-unitary or Trotterized simulation of the 4x4 instance.

## Initial state

|\psi(0)\rangle = |s\rangle = H^{\otimes n}|0\rangle^{\otimes n} = \frac{1}{\sqrt N}\sum_{v=0}^{N-1}|v\rangle (eq_3); for N=4 this is (|00\rangle+|01\rangle+|10\rangle+|11\rangle)/2.

## Measurement

Projective measurement of all n vertex-register qubits in the computational basis; success event is outcome bitstring equal to the binary index of w (for the instance: '00'). Repeat M shots to estimate p = (#successes)/M.

## Classical postprocessing

Estimate success probability from shot counts; optionally repeat for a grid of evolution times t (and rates \gamma, or stage parameters \gamma_1,t_1,\gamma_2,t_2) to locate the maximum success probability and the corresponding runtime; compare runtime scaling across N against eq_6. No further classical processing is implied by the abstract.

## Algorithm steps

1. Prepare the uniform superposition over vertices on the vertex register. (eq_3)
2. Stage 1: apply the unitary e^{-iH(\gamma_1)t_1} with H(\gamma_1) = -\gamma_1 A - |w\rangle\langle w| (compiled either as an exact 2-qubit unitary for the N=4 instance or via product-formula splitting of the graph term and the oracle term; a product formula introduces an approximation error controlled by the step count). (eq_1, eq_2)
3. Stage 2 (two-stage template only): switch the walking rate to \gamma_2 and apply e^{-iH(\gamma_2)t_2}. In the assumed K_4 instance this stage is omitted (\gamma_1=\gamma_2, t_2=0). (eq_5, eq_2)
4. Measure the vertex register in the computational basis and record whether the outcome equals the marked index w. (eq_4)
5. For the K_4 sanity instance, compare the empirical success frequency against the analytic prediction p(t^*)=1 at t^*=\pi; for other graphs, scan t (and \gamma) to estimate the time at which p first reaches its maximum and compare against the O(\sqrt N) benchmark. (eq_7, eq_6)

## Assumptions

- Hamiltonian uses adjacency matrix with coefficient -\gamma and oracle -|w><w| (Laplacian form equivalent only for regular graphs).
- Single marked vertex.
- Two-stage algorithm modelled as two piecewise-constant Schrödinger evolutions with different \gamma and a sharp switch.
- Tiny instance chosen as K_4 with \gamma=1/4, w=0, t=\pi, single stage; this is an agent-selected sanity instance, not a graph from the paper.
- Vertex index encoded in binary on n qubits with qubit 0 as least significant bit; N assumed a power of two for exact Hadamard state preparation.
- \hbar=1; success-probability threshold \Theta(1) assumed in the definition of fast search.

## Missing information

- Definition (vertex set, edge set, parametrization in N) of the low-connectivity/fast-search example graph.
- Definition of the high-connectivity/slow-search example graph on which the two-stage algorithm runs.
- Values or asymptotic forms of the stage parameters \gamma_1, t_1, \gamma_2, t_2 and the resulting runtime and success probability for the two-stage algorithm.
- The paper's precise connectivity measures (vertex, edge, algebraic, normalized algebraic) and their values for the two examples.
- Whether the paper uses the Laplacian or adjacency form of the walk Hamiltonian and its sign/oracle conventions.
- The perturbative or spectral analysis that determines critical \gamma values and proves the runtime claims.
- The precise 'progressively slower runtime' expressions for cubic lattices with d<5 (only qualitatively stated in the abstract).
