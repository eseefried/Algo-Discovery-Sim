# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Spatial search for a single marked vertex on the complete graph K_N using a discrete-time lackadaisical quantum walk (l self-loops per vertex) with the phase-flip coin, as a quantum-walk formulation of Grover's algorithm; the abstract claims l=1 raises the peak success probability from 1/2 to 1 while larger l lowers it.

Scope: One smallest useful construction (chosen as an assumption since no experiment_scope was supplied): the discrete-time coined walk on K_N with l self-loops per vertex, Grover coin, phase-flip marking of one vertex a, flip-flop shift, evolved for t steps from the uniform state, followed by measurement of the vertex register. Tiny explicit instance: N=4, l=1, marked vertex a=0, so the coin space has dimension N-1+l=4 and the total space is 16-dimensional (4 qubits). Out of scope: the Shenvi-Kempe-Whaley coin variant and its l < N^2 threshold, the l < N classical-speedup threshold analysis, the continuous-time walk (where self-loops make no difference), closed-form runtime/success-probability formulas as functions of l, and the generalization to multiple marked vertices.

## Symbols

- $N$: number of vertices of the complete graph K_N; domain: integer, N \geq 2 (instance: N=4)
- $l$: number of self-loops attached to each vertex; domain: non-negative integer (instance: l=1)
- $d$: degree of each vertex including self-loops, d = N-1+l; also the dimension of the coin space at each vertex; domain: positive integer (instance: d=4)
- $a$: the marked vertex; domain: a \in \{0,\dots,N-1\} (instance: a=0)
- $v,w$: vertex labels; domain: \{0,\dots,N-1\}
- $c$: coin/direction index at a vertex; c\in\{0,\dots,N-2\} labels an edge to another vertex, c\in\{N-1,\dots,N-2+l\} labels a self-loop; domain: \{0,\dots,d-1\}
- $|s_c\rangle$: uniform superposition over the d coin directions; domain: unit vector in \mathbb{C}^d
- $|\psi_t\rangle$: walker state after t steps; domain: unit vector in \mathbb{C}^N\otimes\mathbb{C}^d
- $p(t)$: probability of finding the walker at the marked vertex after t steps; domain: [0,1]
- $t$: number of walk steps; domain: non-negative integer

## eq_1: Hilbert space and initial uniform state

$$
\mathcal{H}=\mathbb{C}^N\otimes\mathbb{C}^{d},\quad d=N-1+l,\quad |s_c\rangle=\frac{1}{\sqrt{d}}\sum_{c=0}^{d-1}|c\rangle,\quad |\psi_0\rangle=\frac{1}{\sqrt{N}}\sum_{v=0}^{N-1}|v\rangle\otimes|s_c\rangle
$$

Vertex register tensored with a coin register of dimension d = N-1+l (N-1 outgoing edges plus l self-loops); the walk starts in the uniform superposition over all vertex-direction pairs. Register ordering: vertex register first, coin register second.

Provenance: `abstract_inferred`. Giving each vertex l self-loops on K_N makes every vertex have degree N-1+l, so the coin space per vertex has dimension N-1+l; the uniform initial state is the standard starting point for Grover-type walk search and is inferred from the Grover formulation.

Abstract evidence: each vertex is given $l$ self-loops

Equation assumptions:

- Uniform initial state over vertex-direction pairs (not stated in abstract).

## eq_2: Grover (diffusion) coin on degree-d vertices

$$
C_0 = 2|s_c\rangle\langle s_c| - I_d,\qquad C = I_N\otimes C_0
$$

Grover coin acting identically on every vertex's d-dimensional coin space.

Provenance: `standard_background`. The Grover coin is the standard coin for quantum-walk search on regular graphs (Shenvi-Kempe-Whaley, Ambainis-Kempe-Rivosh); the abstract does not spell it out.

Equation assumptions:

- The lackadaisical walk uses the Grover coin on the enlarged d-dimensional coin space; the paper may use a different weighting of self-loops.

## eq_3: Phase-flip marking of the marked vertex

$$
Q = (I_N - 2|a\rangle\langle a|)\otimes I_d
$$

Oracle that flips the sign of all amplitude located at the marked vertex a, applied before the coin; equivalently the marked vertex experiences coin -C_0 while unmarked vertices experience C_0.

Provenance: `abstract_inferred`. The 'phase flip coin' in the quantum-walk search literature denotes applying a phase flip at the marked vertex followed by the Grover coin everywhere; this is the standard meaning inferred from the abstract's name.

Abstract evidence: For the discrete-time quantum walk using the phase flip coin

Equation assumptions:

- The phase flip is a sign flip of the marked vertex's full coin subspace.

## eq_4: Flip-flop shift with self-loops (direction encoding)

$$
S|v\rangle|c\rangle=\begin{cases}|(v+c+1)\bmod N\rangle\,|N-2-c\rangle, & 0\le c\le N-2,\\ |v\rangle|c\rangle, & N-1\le c\le N-2+l.\end{cases}
$$

Direction c<N-1 at vertex v points to w=(v+c+1) mod N; the flip-flop shift moves the walker to w and reverses the direction so that it points back to v (the index N-2-c satisfies (w+(N-2-c)+1) mod N = v). Self-loop directions leave the walker in place. S is an involution.

Provenance: `assumption`. The abstract does not specify the shift; the flip-flop shift is the standard choice for quantum-walk search on the complete graph, and the explicit direction encoding is a reconstruction choice to make the shift a permutation of basis states suitable for circuits.

Equation assumptions:

- Flip-flop (reversing) shift rather than a moving shift.
- Direction encoding c -> (v+c+1) mod N chosen for circuit convenience.

## eq_5: One step of the search walk and success probability

$$
U = S\,C\,Q,\qquad |\psi_t\rangle=U^{t}|\psi_0\rangle,\qquad p(t)=\sum_{c=0}^{d-1}\left|\langle a,c|\psi_t\rangle\right|^2
$$

Each step applies the phase flip, the Grover coin, and the shift; the success probability is the total probability on the marked vertex regardless of coin state.

Provenance: `standard_background`. Standard composition of oracle, coin, and shift for coined-walk search; success probability is the marginal probability of the vertex register being a.

Equation assumptions:

- Operator ordering S C Q (oracle first, then coin, then shift).

## eq_6: Abstract's claim on peak success probability

$$
\max_t p(t)\to \tfrac{1}{2}\ (l=0),\qquad \max_t p(t)\to 1\ (l=1),\qquad \max_t p(t)<1\ \text{decreasing for } l>1
$$

Asymptotic (large-N) peak success probability of the phase-flip-coin walk as a function of the number of self-loops, as claimed in the abstract; the exact dependence on l and the corresponding runtimes are not given in the abstract.

Provenance: `abstract_explicit`. Direct restatement of the abstract's quantitative claim; the 'decreasing' part is qualitative only. Values are asymptotic in N and may differ for the tiny instance N=4.

Abstract evidence: adding a self-loop to each vertex boosts the success probability from $1/2$ to $1$. Additional self-loops, however, decrease the success probability.

Equation assumptions:

- The stated values refer to the large-N limit of the peak success probability.

## Registers

- vertex: \lceil \log_2 N\rceil (instance: 2 qubits) qubits; Holds the walker's vertex label v in binary (integer encoding, little-endian or big-endian fixed consistently).
- coin: \lceil \log_2 (N-1+l)\rceil (instance: 2 qubits) qubits; Holds the direction index c; values 0..N-2 are edges to other vertices, values N-1..N-2+l are self-loops. Basis states with c \geq d are unused when d is not a power of 2.

## Initial state

|\psi_0\rangle = \frac{1}{\sqrt{N d}}\sum_{v=0}^{N-1}\sum_{c=0}^{d-1}|v\rangle|c\rangle with d=N-1+l (eq_1). For N=4, l=1: uniform superposition over all 16 basis states of 4 qubits, preparable by Hadamards on all qubits.

## Measurement

Measure the vertex register in the computational basis after t steps; the outcome equals a with probability p(t) (eq_5). The coin register is discarded.

## Classical postprocessing

Verify a candidate vertex with one classical oracle query; estimate p(t) from shot frequencies for a range of t and locate the first peak; compare l=0 and l=1 peak values against eq_6. The optimal number of steps must be found by scanning since the abstract gives no runtime formula.

## Algorithm steps

1. Prepare the uniform superposition over vertices and the d = N-1+l coin directions (eq_1). (eq_1)
2. Repeat t times: apply the phase flip Q on the marked vertex a (eq_3), then the Grover coin C on the coin register (eq_2), then the flip-flop shift S with self-loops fixed (eq_4); this realises U = S C Q (eq_5). (eq_3, eq_2, eq_4, eq_5)
3. After t steps, measure the vertex register; estimate p(t) and compare to the abstract's claim that the peak approaches 1 for l=1 versus 1/2 for l=0 (eq_6). The optimal t is not given in the abstract and must be scanned over. (eq_5, eq_6)

## Assumptions

- No experiment_scope was supplied, so the discrete-time phase-flip-coin walk on K_N with a single marked vertex was chosen as the single smallest useful construction, with tiny instance N=4, l=1, a=0.
- Grover coin on the enlarged (N-1+l)-dimensional coin space, with self-loops weighted equally to ordinary edges.
- Flip-flop shift with the explicit direction encoding of eq_4; self-loop directions act as identity.
- Operator ordering U = S C Q and uniform initial state.
- Asymptotic claims in eq_6 are large-N statements and may not hold exactly for N=4.

## Missing information

- Closed-form success probability and runtime as functions of N and l for the phase-flip coin (abstract only states 1/2 -> 1 for l=0 -> 1 and qualitative decrease for l>1).
- Exact definition of the Shenvi-Kempe-Whaley coin variant used, and the derivation of the l < N versus l < N^2 classical-speedup thresholds.
- Continuous-time walk Hamiltonian and the demonstration that self-loops have no effect there.
- Treatment of multiple marked vertices.
- Whether the paper weights self-loops equally with edges in the coin and which shift operator it uses (assumed here).
