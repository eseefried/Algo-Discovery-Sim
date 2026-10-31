# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Spatial search by continuous-time quantum walk on a graph of N vertices: a particle evolving under a walk Hamiltonian plus a marked-vertex oracle term should concentrate amplitude on the marked vertex w, and the paper proposes a diagrammatic degenerate-perturbation-theory method to estimate the critical jumping rate, eigenvalue gap and runtime, including a graph whose invariant evolution subspace grows with N.

Scope: Scoped to the standard continuous-time quantum-walk search Hamiltonian and the generic degenerate-perturbation-theory estimate of the critical jumping rate and runtime, instantiated on the smallest nontrivial explicit case: the complete graph K_4 (N=4, one marked vertex, 2-qubit vertex register). The paper's specific contributions - the diagrammatic sketching of small weighted graphs with self-loops, and the particular graph whose evolution subspace dimension grows with N - are NOT reconstructed because the abstract gives no definitions for them.

## Symbols

- $N$: number of vertices of the graph; domain: positive integer; N=4 in the tiny instance
- $A$: adjacency matrix of the graph (A_{uv}=1 if u~v, else 0); domain: N x N symmetric 0/1 matrix
- $\gamma$: jumping rate (walk strength) of the continuous-time quantum walk; domain: positive real
- $|w\rangle$: computational-basis state of the marked vertex; domain: vertex basis state in C^N
- $|s\rangle$: uniform superposition over all vertices (initial state); domain: unit vector in C^N
- $H$: search Hamiltonian; domain: N x N Hermitian matrix
- $H^{(0)}, V$: unperturbed walk Hamiltonian and oracle perturbation; domain: N x N Hermitian matrices
- $\Delta E$: energy gap between the two lowest perturbed eigenstates that are degenerate at leading order; domain: positive real
- $t_*$: runtime at which success probability peaks; domain: positive real
- $p(t)$: success probability of finding w when measuring at time t; domain: [0,1]

## eq_1: Continuous-time quantum walk search Hamiltonian

$$
H = -\gamma A - |w\rangle\langle w|
$$

Standard search Hamiltonian: a walk term proportional to the adjacency matrix plus a rank-one oracle marking vertex w. The paper may instead use the Laplacian L = D - A; for regular graphs the two choices differ only by a constant shift.

Provenance: `standard_background`. The abstract refers to a randomly walking quantum particle searching a graph in continuous time, which is the Childs-Goldstone spatial-search framework; the explicit form is recalled from background, not stated in the abstract.

Equation assumptions:

- Adjacency-matrix form of the walk (Laplacian form not excluded by the abstract)
- Single marked vertex

## eq_2: Initial equal superposition

$$
|s\rangle = \frac{1}{\sqrt{N}} \sum_{v=1}^{N} |v\rangle
$$

The walker starts in the uniform superposition over vertices, the standard initial state for spatial search.

Provenance: `standard_background`. Standard initial state for continuous-time quantum-walk search; not stated in the abstract.

## eq_3: Perturbative split for degenerate perturbation theory

$$
H = H^{(0)} + V,\quad H^{(0)} = -\gamma A,\quad V = -|w\rangle\langle w|
$$

The oracle is treated as a perturbation of the walk Hamiltonian. At a critical \gamma, two (or more) eigenstates of H^{(0)} become degenerate; degenerate perturbation theory then diagonalizes V in that degenerate subspace.

Provenance: `abstract_inferred`. The abstract says degenerate perturbation theory is applied to the search problem; the natural (and standard) split is walk term as unperturbed Hamiltonian and oracle as perturbation. The specific unperturbed eigenstates and the diagrammatic weighted-graph picture are not given.

Abstract evidence: considering degenerate perturbation theory’s effects on them

Equation assumptions:

- Oracle term is the perturbation; walk term is unperturbed

## eq_4: Leading-order degenerate perturbation theory and runtime

$$
H_{ab} = \langle \psi_a | H | \psi_b \rangle,\ a,b \in \{1,\dots,d\};\quad \Delta E = E_{+} - E_{-};\quad t_* \approx \frac{\pi}{\Delta E}
$$

Within the d-dimensional degenerate eigenspace of H^{(0)} at the critical \gamma, the perturbed eigenstates are obtained by diagonalizing the d x d matrix H_{ab}. If |s\rangle and |w\rangle are each approximately a superposition of the two resulting lowest eigenstates with energies E_\pm, the evolution rotates |s\rangle to |w\rangle in time approximately \pi/\Delta E (approximation, not exact equality).

Provenance: `standard_background`. Generic degenerate-perturbation-theory estimate of the gap and runtime used in quantum-walk search analyses; recalled from background.

Equation assumptions:

- Leading-order degenerate perturbation theory suffices
- Initial and marked states lie predominantly in the span of the two relevant eigenstates

## eq_5: Tiny explicit instance: complete graph K_N with N=4

$$
A = J - I,\quad \gamma_c = \frac{1}{N},\quad \Delta E \approx \frac{2}{\sqrt{N}},\quad t_* \approx \frac{\pi\sqrt{N}}{2},\quad p(t_*) \approx 1;\quad N=4:\ \gamma_c = \tfrac{1}{4},\ t_* \approx \pi
$$

Proposed smallest instance: complete graph on 4 vertices (J is the all-ones matrix). Known background results for complete-graph search: critical jumping rate 1/N, gap 2/\sqrt{N}, runtime \pi\sqrt{N}/2 with success probability approaching 1 asymptotically. This instance has a 2-dimensional invariant subspace span{|w\rangle,|s\rangle}, so it does NOT exhibit the paper's growing-dimension feature.

Provenance: `assumption`. No scope was supplied, so a minimal explicit instance is chosen; complete-graph values are standard results, and the N=4 numbers follow from them (asymptotic approximations, so finite-N values are approximate).

Equation assumptions:

- Instance choice K_4 is the reconstructor's, not the paper's
- Asymptotic formulas applied at small N are approximate

## eq_6: Success probability

$$
p(t) = \left| \langle w | e^{-iHt} | s \rangle \right|^2
$$

Probability of measuring the marked vertex after evolving for time t; the algorithm measures at t = t_*.

Provenance: `standard_background`. Standard definition of success probability for continuous-time search.

## Registers

- vertex: n = \lceil \log_2 N \rceil (2 qubits for N=4) qubits; Encodes the vertex index v in binary (big-endian, |v\rangle = |v_1 v_0\rangle with v = 2 v_1 + v_0); the walker's position.

## Initial state

|s\rangle = \frac{1}{\sqrt{N}}\sum_v |v\rangle; for N=4 this is H^{\otimes 2}|00\rangle.

## Measurement

Computational-basis measurement of the vertex register at time t_*; the outcome is a vertex label v, success if v = w.

## Classical postprocessing

Repeat the experiment to estimate p(t_*) as the fraction of runs returning w; compare with the perturbation-theory prediction (approximately 1 for the complete graph).

## Algorithm steps

1. Prepare the uniform superposition over vertices (for N=4: Hadamards on both qubits). (eq_2)
2. Fix the jumping rate at the critical value predicted by degenerate perturbation theory (for K_4: \gamma_c = 1/4) and form the search Hamiltonian. (eq_1, eq_3, eq_5)
3. Evolve under e^{-iHt} for time t_* \approx \pi/\Delta E (for K_4: t_* \approx \pi); the exponential may be realized by exact diagonalization in simulation or by Trotterization of the walk and oracle terms (assumption). (eq_4, eq_5, eq_6)
4. Measure the vertex register in the computational basis. (eq_6)

## Assumptions

- No experiment_scope was supplied; the smallest useful construction (complete graph K_4, one marked vertex, 2 qubits) was chosen by the reconstructor
- Adjacency-matrix form of the walk Hamiltonian is assumed; the paper may use the Laplacian
- Single marked vertex
- Leading-order degenerate perturbation theory suffices to predict the gap and runtime
- Hamiltonian simulation method (exact exponentiation vs Trotterization) is left to the circuit stage

## Missing information

- The diagrammatic method itself: how the small weighted graphs with self-loops are drawn from the original graph and how perturbation-theory quantities are read off them
- The specific graph used as the paper's example whose invariant evolution subspace has dimension growing with N, and its resulting critical \gamma, gap, runtime and success probability
- Whether the walk term is the adjacency matrix or the Laplacian, and the number/placement of marked vertices
- Any higher-order perturbative corrections or rigorous error bounds stated in the paper
