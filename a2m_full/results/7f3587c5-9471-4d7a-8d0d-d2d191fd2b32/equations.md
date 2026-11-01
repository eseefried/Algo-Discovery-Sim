# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Lackadaisical quantum walk search for one marked vertex on the complete graph K_N with l self-loops per vertex (scoped to l=1, N=4), using the phase-flip Grover coin. Compute the marked-vertex probability versus step count T from position-register measurement.

Scope: One tiny instance: N=4 vertices, l=1 self-loop, so 4 arcs per vertex (3 neighbors + 1 loop). Position is 2 qubits and coin is 2 qubits, 4 qubits total. Marked vertex w=0 is a known constant. Phase-flip coin only. The SKW coin, l>1, multiple marked vertices, runtime scaling claims, and the continuous-time walk are outside the circuit scope.

## Symbols

- $N$: number of vertices; domain: integer, power of two, N=4 in scope
- $l$: self-loops per vertex; domain: nonnegative integer, l=1 in scope
- $w$: marked vertex; domain: {0,...,N-1}
- $|v,c\rangle$: walker at vertex v with coin c; c labels an arc (a neighbor or a loop); domain: v in [0,N-1], c in [0,N-1]
- $|s_c\rangle$: weighted uniform coin state; domain: unit vector in C^{N-1+l}
- $C_0, C_1$: coin on unmarked / marked vertices; domain: unitary on the coin space
- $S$: flip-flop shift; domain: permutation of arcs
- $T$: number of walk steps; domain: nonnegative integer
- $\theta$: Ry angle preparing |s_c\rangle; domain: real

## eq_1: Weighted coin state

$$
|s_c\rangle=\sqrt{\tfrac{N-1}{N-1+l}}\,|\text{nbrs}\rangle+\sqrt{\tfrac{l}{N-1+l}}\,|\text{loop}\rangle,\quad |\text{nbrs}\rangle=\tfrac{1}{\sqrt{N-1}}\sum_{c\ne\text{loop}}|c\rangle
$$

Coin state weighted by loop count. For N=4 and l=1 it has 4 components, each of amplitude 1/2, i.e. it is the uniform state.

Provenance: `assumption`. Taken from the sketch's weighted-loop construction; the abstract does not give it.

Equation assumptions:

- Coin dimension equals N-1+l=4, so no padding is needed
- l=1 gives the uniform state, so Hadamards suffice

## eq_2: Coin operators

$$
C_0=2|s_c\rangle\langle s_c|-I,\quad C_1=-I,\quad C'=|w\rangle\langle w|\otimes C_1+\sum_{v\ne w}|v\rangle\langle v|\otimes C_0
$$

Phase-flip coin: Grover diffusion on unmarked vertices and -I on the marked vertex. Circuit: controlled on position=w apply a global -I on the coin (a Z-type phase on the control pattern), otherwise apply H^{2} X^{2} CZ X^{2} H^{2} diffusion.

Provenance: `abstract_inferred`. The abstract names the phase-flip coin; the specific forms of C_0 and C_1 are recalled from the standard lackadaisical-walk literature.

Abstract evidence: using the phase flip coin

Equation assumptions:

- Marked-vertex oracle is built from known constants with standard gates

## eq_3: Flip-flop shift

$$
S|v,c\rangle=|c',v'\rangle\ \text{with arc }(u,v)\mapsto(v,u);\ \text{loops fixed: }S|v,\text{loop}\rangle=|v,\text{loop}\rangle
$$

The shift swaps arc (u,v) with (v,u). For the complete graph, label the coin of a non-loop arc by its target neighbor. Then S swaps position and coin registers when the coin is not the loop. Implemented as a permutation with CX/Toffoli/SWAP gates. The loop-direction state must be fixed by an explicit encoding.

Provenance: `assumption`. The shift is described in the sketch; the abstract only implies self-loops.

Equation assumptions:

- Arc encoding for N=4 must map the 4 coin values to 3 neighbors plus 1 loop relative to the current vertex, e.g. coin c means target v XOR (c+1) for c=0..2 and the loop is c=3
- With this relative encoding the shift becomes |v,c> -> |v XOR (c+1), c> for c<3, with the loop fixed. This is an involution.

## eq_4: Walk evolution and readout

$$
|\psi_T\rangle=(S\,C')^{T}|\psi_0\rangle,\quad |\psi_0\rangle=\tfrac{1}{\sqrt{N(N-1+l)}}\sum_{v,c}|v,c\rangle,\quad p_w(T)=\sum_c|\langle w,c|\psi_T\rangle|^2
$$

Uniform initial superposition over arcs, T steps, and the marked-vertex probability read from the position register.

Provenance: `abstract_inferred`. The abstract implies a discrete-time walk with success probability p_w; the explicit form is the standard construction.

Abstract evidence: adding a self-loop to each vertex boosts the success probability from $1/2$ to $1$

Equation assumptions:

- Position qubits measured; coin qubits left unmeasured

## eq_5: Target success probabilities

$$
\max_T p_w(T)=1/2\ (l=0),\quad \max_T p_w(T)=1\ (l=1)
$$

Claimed peak success probabilities for the phase-flip coin. A simulation check for N=4 and l=1 should show a peak near 1 at T of order (\pi/2)\sqrt{N}.

Provenance: `abstract_explicit`. Stated in the abstract. The step count T≈(π/2)√N comes from the sketch and is not in the abstract.

Abstract evidence: adding a self-loop to each vertex boosts the success probability from $1/2$ to $1$

Equation assumptions:

- For l=1 the peak is reached asymptotically in N; for small N such as 4 it may be only approximate
- Peak found by scanning T

## Registers

- pos: 2 qubits; vertex index v, little-endian
- coin: 2 qubits; arc label c: 3 neighbors plus 1 self-loop

## Initial state

H on all 4 qubits, giving the uniform superposition over 16 arcs.

## Measurement

Measure the 2 pos qubits into 2 classical bits. In Qiskit counts, the last character is classical bit 0, i.e. pos qubit 0. Marked-vertex frequency estimates p_w(T).

## Classical postprocessing

Compute p_w(T) from counts for each T, and report the T of maximum p_w and its value.

## Algorithm steps

1. Prepare uniform superposition over all arcs with Hadamards on the pos and coin qubits. (eq_4)
2. Repeat T times: apply the coin C' (controlled on pos==w, -I on coin; otherwise the Grover diffusion on coin, with weighted |s_c> prepared by Ry then H and X conjugation for general l), then the shift S as a permutation. (eq_1, eq_2, eq_3)
3. Measure the pos qubits only. Repeat for T=0..Tmax and pick the T with the largest p_w. (eq_4, eq_5)

## Assumptions

- Choose N=4, l=1, w=0 as the smallest useful instance
- Coin dimension is a power of two so no padding is needed
- No black box; the oracle is a known constant
- Relative-XOR neighbor encoding is chosen here, not given by the abstract

## Missing information

- Exact coin-arc encoding and shift used in the paper
- Exact optimal T
- SKW coin details and runtime formula
- Behavior for l>1, which requires non-power-of-two coin dimension and padding
- Continuous-time Hamiltonian details and the multiple-marked-vertex generalization
