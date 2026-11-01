# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Search for one marked vertex on the complete graph of N vertices using a discrete-time quantum walk in which each vertex has l self-loops (lackadaisical quantum walk), with the phase-flip coin; compare success probability for l=0 and l=1.

Scope: Smallest useful construction: a single marked vertex, the phase-flip coin (Grover diffusion on each vertex's coin space of dimension N-1+l), and a tiny instance with N=4 and l in {0,1}. Outside scope: the SKW coin, continuous-time walks, multiple marked vertices, runtime scaling versus classical search, and the detailed proofs of the abstract's claims.

## Symbols

- $N$: number of vertices of the complete graph; domain: integer, N>=2
- $l$: number of self-loops per vertex; domain: non-negative integer
- $d=N-1+l$: degree of each vertex including self-loops (coin space dimension); domain: integer
- $|v,c\rangle$: walker at vertex v with coin state c labelling an outgoing edge or self-loop; domain: v in {0..N-1}, c in {1..d}
- $w$: marked vertex; domain: {0..N-1}
- $C_0$: coin operator on unmarked vertices; domain: d x d unitary
- $C_1$: coin operator on the marked vertex; domain: d x d unitary
- $S$: shift operator swapping the two arc states of each edge, with each self-loop fixed; domain: permutation on the vertex-coin space
- $U$: one walk step; domain: unitary
- $P_{succ}$: probability of measuring the marked vertex; domain: [0,1]

## eq_1: Walk step

$$
U = S\,\big(\textstyle\sum_{v\neq w}|v\rangle\langle v|\otimes C_0 + |w\rangle\langle w|\otimes C_1\big)
$$

Standard coined-walk search step: coin on each vertex, then shift.

Provenance: `standard_background`. Generic coined quantum-walk search form; the abstract names the discrete-time walk with coin but gives no operators.

Equation assumptions:

- Coin applied before the shift
- Marked vertex gets a different coin

## eq_2: Phase-flip coin choice

$$
C_0 = 2|s_c\rangle\langle s_c| - I_d,\quad C_1 = -I_d,\quad |s_c\rangle = \tfrac{1}{\sqrt d}\sum_{c=1}^{d}|c\rangle
$$

Grover diffusion coin on unmarked vertices and a phase flip (-I) on the marked vertex.

Provenance: `assumption`. Common definition of the 'phase flip' coin in the walk-search literature, assumed here because the abstract does not define it.

Equation assumptions:

- The abstract's 'phase flip coin' means this construction

## eq_3: Initial state

$$
|\psi_0\rangle = \tfrac{1}{\sqrt{N}}\sum_{v=0}^{N-1}|v\rangle\otimes|s_c\rangle
$$

Uniform superposition over all vertex and coin states.

Provenance: `assumption`. Typical initial state for walk search; not stated in the abstract.

Equation assumptions:

- Uniform start over vertices and coin directions

## eq_4: Success probability

$$
P_{succ}(t)=\sum_{c=1}^{d}\big|\langle w,c|U^t|\psi_0\rangle\big|^2
$$

Probability of finding the walker at the marked vertex after t steps.

Provenance: `standard_background`. Born rule applied to the vertex register.

## eq_5: Reported success probabilities

$$
\max_t P_{succ}\to \tfrac12 \text{ for } l=0,\qquad \max_t P_{succ}\to 1 \text{ for } l=1
$$

Abstract's claim for the phase-flip coin, taken as the target behavior to reproduce (asymptotically in N).

Provenance: `abstract_inferred`. The abstract states the success probability boosts from 1/2 to 1 with one self-loop; the asymptotic-in-N reading is my inference.

Abstract evidence: adding a self-loop to each vertex boosts the success probability from $1/2$ to $1$

Equation assumptions:

- Maximum over t
- Large N

## Registers

- vertex: ceil(log2 N) qubits (2 for N=4) qubits; vertex position, computational-basis encoding of v
- coin: ceil(log2(N-1+l)) qubits (2 for N=4,l=0; 2 for N=4,l=1 with padding to 4 states) qubits; edge and self-loop label; unused basis states if d is not a power of 2 must be excluded or padded

## Initial state

Uniform superposition over vertices and coin states (see eq_3)

## Measurement

Measure the vertex register in the computational basis; success if the outcome equals w.

## Classical postprocessing

Estimate P_succ from repeated runs and scan t to find the maximum; for the tiny instance, compare to the exact simulated value.

## Algorithm steps

1. Prepare the uniform initial state over vertex and coin registers. (eq_3)
2. Repeat t times: apply the coin (Grover diffusion on unmarked vertices, -I on the marked vertex), then the shift. (eq_1, eq_2)
3. Measure the vertex register and compare the success probability with the abstract's claim for l=0 versus l=1. (eq_4, eq_5)

## Assumptions

- Single marked vertex
- Phase-flip coin as defined in eq_2
- Tiny instance N=4, l in {0,1}
- Shift swaps the arc states (v,c) and (v',c') of each edge; self-loops are fixed
- The N=4 instance is far from the asymptotic regime, so the 1/2 and 1 values will only be approximate

## Missing information

- Exact definition of the phase-flip coin and of the shift used in the paper
- Initial state used in the paper
- Optimal number of steps and formulas for success probability versus l
- Definitions of the SKW coin and continuous-time Hamiltonian
- Weight or normalization of the self-loops, e.g. whether the weighting differs for l non-integer
- Analysis of the multi-marked-vertex case
