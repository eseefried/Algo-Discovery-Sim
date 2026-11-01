# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Grover search as a quantum walk on the complete graph with self-loops (N=2^n vertices, one marked vertex w), where each hop (diffusion) operator fails with amplitude eps and acts as identity on the failure branch. Determine how the success probability and optimal iteration count depend on eps and N, with the claim that eps=O(1/sqrt(N)) is needed to keep O(sqrt(N)) runtime.

Scope: Tiny instance, n=2..4 search qubits, one marked vertex w, discrete-time walk only, T about (pi/4)sqrt(N) iterations, one oracle placeholder query per step. The hop is modeled as an incoherent-or-coherent eps-mixture of R_s and I using one ancilla per step. The continuous-time version, the physical barrier model, and the proofs are outside the scope.

## Symbols

- $N=2^n$: number of vertices; domain: positive integer power of 2
- $w$: marked vertex, hidden in the oracle; domain: {0,...,N-1}
- $|s\rangle$: uniform superposition over vertices; domain: state on n qubits
- $\epsilon$: hop failure amplitude; domain: [0,1]
- $\theta$: ancilla Ry angle with sin(theta/2)=eps; domain: [0,pi]
- $R_s$: reflection 2|s><s|-I; domain: unitary on n qubits
- $U_w$: oracle phase flip I-2|w><w|, black box; domain: unitary on n qubits
- $T$: number of walk steps; domain: nonnegative integer
- $c$: constant in eps=c/sqrt(N); domain: positive real

## eq_1: Lossy hop operator

$$
H_\epsilon=\sqrt{1-\epsilon^2}\,R_s+\epsilon\,I
$$

Barrier-affected hop: success amplitude times reflection plus failure amplitude times staying put. It is non-unitary on the search register alone, so it needs an ancilla dilation.

Provenance: `abstract_inferred`. Tunnel amplitude and stay-put amplitude are modeled as a coherent sum, as stated in the method sketch; the exact form is an assumption.

Abstract evidence: Then the particle has some amplitude of tunneling through the barriers, and some amplitude of staying put.

Equation assumptions:

- eps is the same at every step
- coherent linear combination form

## eq_2: Ancilla dilation

$$
V=\left(|0\rangle\langle0|\otimes R_s+|1\rangle\langle1|\otimes I\right)\left(R_y(\theta)\otimes I\right),\quad \sin(\theta/2)=\epsilon
$$

Ancilla starts in |0>, is rotated, and controls R_s. The ancilla-0 projection of V gives sqrt(1-eps^2)R_s on the search register and the ancilla-1 projection gives eps I, so the ancilla-1 branch is the failure branch and is not recombined.

Provenance: `assumption`. Standard way to implement a linear combination by dilation. It is a modeling choice, not from the abstract. Using a fresh ancilla per step keeps the branches unmixed, while measuring and resetting gives a mixed-state variant.

Equation assumptions:

- ancilla fresh per step or reset after each step
- branch outcomes are not recombined

## eq_3: Walk step and state after T steps

$$
|\psi_T\rangle=\left(H_\epsilon U_w\right)^T|s\rangle,\quad P(w)=|\langle w|\psi_T\rangle|^2
$$

Ideal Grover walk at eps=0. With eps>0 the success probability is taken from the ancilla-0 branch or from the full dilated simulation.

Provenance: `standard_background`. Standard Grover iteration with the reflection replaced by H_eps.

Equation assumptions:

- single marked vertex
- barrier acts only on the hop, not on the oracle

## eq_4: Ideal Grover iteration count

$$
T^*\approx\frac{\pi}{4}\sqrt{N},\quad \sin\phi=\frac{1}{\sqrt N},\ \text{rotation per step }2\phi\approx\frac{2}{\sqrt N}
$$

Rotation in span{|w>,|s'>} for eps=0.

Provenance: `standard_background`. Textbook Grover analysis.

## eq_5: Scaling condition for failure amplitude

$$
\epsilon=O(1/\sqrt N)\Rightarrow \text{runtime }O(\sqrt N);\quad \epsilon=\Omega(1)\Rightarrow \text{runtime }O(N)
$$

Claimed dichotomy. It is not derived here. The heuristic is that accumulated failure about T*eps stays O(1) only if eps*sqrt(N)=O(1).

Provenance: `abstract_explicit`. Directly stated in the abstract; the precise theorem statement and constants are unknown.

Abstract evidence: We prove that the failure amplitude must scale as $O(1/\sqrt{N})$ for search to retain its quantum $O(\sqrt{N})$ runtime; otherwise, it searches in classical $O(N)$ time.

## Registers

- search: n (2 to 4) qubits; vertex index, little-endian integer encoding where qubit i is bit i
- anc: 1 per step, or 1 reused with reset qubits; hop-failure flag; |1> means the hop failed

## Initial state

H on all search qubits gives |s>; ancilla(s) in |0>.

## Measurement

Measure the n search qubits, with the little-endian bit order of counts keys taken into account. The most frequent outcome estimates w. Optionally postselect on all ancillas=0.

## Classical postprocessing

Take the argmax of the counts, or compute P(w) from the statevector. Determine the optimal T and max P(w) for each N and eps.

## Algorithm steps

1. Prepare |s> by applying H to all search qubits. (eq_3)
2. Repeat T times: apply the oracle placeholder U_w to the search register, one query per step. (eq_3)
3. Apply the lossy hop: Ry(theta) on a fresh ancilla, then R_s on the search register controlled on ancilla=0 (H, X, multi-controlled Z, X, H, with the control added). Note that controlled-R_s applied exactly equals a controlled global-phase-corrected reflection, so the controlled version must keep the correct relative phase, for example by controlling only the central multi-controlled Z. Then reset or discard the ancilla. (eq_1, eq_2)
4. Sweep T and eps, using eps=c/sqrt(N) and eps=const, to find max P(w) and optimal T versus N. (eq_4, eq_5)

## Assumptions

- Complete graph with self-loops, single marked vertex
- eps independent of step
- Barrier affects only the hop
- Ancilla per step is within the qubit cap, otherwise reset is used
- Smallest instance n=2..4

## Missing information

- Exact hop-failure model used in the paper, coherent versus incoherent
- The proof and constants for the eps scaling
- Continuous-time Hamiltonian and barrier-reduced hopping amplitude
- Qubit cap and query budget values
