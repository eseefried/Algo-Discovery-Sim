# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Characterize lazy discrete-time quantum walks on the line: moment scaling, spread of the probability distribution (DFT coin vs Hadamard), and occupancy number/rate. The abstract gives no explicit formulas.

Scope: Smallest useful construction: a 1D lazy quantum walk with a 3-dimensional coin (move left, stay, move right) and DFT coin, started at the origin, with the position distribution and n-th moment. Out of scope: the occupancy number/rate definitions (not given), the proofs, the comparison with classical and lazy classical walks, and the exact concentration interval.

## Symbols

- $t$: number of time steps; domain: non-negative integer
- $x$: lattice position; domain: integer
- $c$: coin basis label (left, stay, right); domain: {-1,0,1}
- $C$: coin operator, assumed 3x3 DFT; domain: 3x3 unitary
- $S$: conditional shift operator; domain: unitary on position x coin
- $P_t(x)$: probability of position x at step t; domain: [0,1]
- $M_n(t)$: n-th moment of position distribution; domain: real, non-negative for even n
- $\omega$: primitive cube root of unity; domain: complex

## eq_1: Moment scaling

$$
M_n(t)=\sum_x x^n P_t(x)=O(t^n)
$$

Order of the n-th moment of the lazy walk's distribution.

Provenance: `abstract_explicit`. The abstract states the O(t^n) order; the sum form is the standard moment definition.

Abstract evidence: lazy quantum walks have $O(t^{n})$ order of the n-th moment of the corresponding probability distribution

Equation assumptions:

- P_t is the position distribution after t steps

## eq_2: Lazy walk step (assumed)

$$
|\psi_{t+1}\rangle=S(I\otimes C)|\psi_t\rangle,\quad S|x,c\rangle=|x+c,c\rangle
$$

One step of a lazy walk with 3-dimensional coin; c=0 means staying.

Provenance: `assumption`. A common lazy-walk model; the abstract does not give the exact construction, which may differ (e.g. Childs' lazy walk).

Equation assumptions:

- Stay amplitude via coin state c=0
- Line graph

## eq_3: DFT coin

$$
C_{jk}=\frac{1}{\sqrt3}\omega^{jk},\ \omega=e^{2\pi i/3},\ j,k\in\{0,1,2\}
$$

3x3 DFT coin matrix, with basis indices identified with c via a fixed relabeling.

Provenance: `standard_background`. Standard DFT matrix; the abstract only names a DFT coin without dimension.

Equation assumptions:

- Coin dimension 3

## eq_4: Position distribution

$$
P_t(x)=\sum_{c\in\{-1,0,1\}}|\langle x,c|\psi_t\rangle|^2
$$

Marginal probability over coin states.

Provenance: `standard_background`. Born rule.

## eq_5: Initial state

$$
|\psi_0\rangle=|0\rangle_x\otimes|\chi\rangle_c
$$

Walker at origin with a coin state chi.

Provenance: `assumption`. Initial coin state not given in the abstract.

Equation assumptions:

- chi to be chosen, e.g. |0>

## Registers

- position: ceil(log2(2t+1)) qubits for t steps, symbolic qubits; walker position x, offset-encoded
- coin: 2 qubits (3 of 4 levels used) qubits; 3-level coin: left, stay, right

## Initial state

Walker at x=0 with coin state |chi> (assumed, e.g. stay).

## Measurement

Measure the position register in the computational basis, repeated to estimate P_t(x).

## Classical postprocessing

Estimate moments M_n(t) from the histogram; occupancy number/rate cannot be computed since their definitions are not given.

## Algorithm steps

1. Prepare the initial state. (eq_5)
2. Repeat t times: apply the DFT coin, then the conditional shift. (eq_2, eq_3)
3. Compute the position distribution and moments. (eq_4, eq_1)

## Assumptions

- Walk on the integer line
- 3-state coin with DFT
- Coin and initial state chosen by me
- Tiny instance such as t=3 suggested

## Missing information

- Exact lazy walk definition used
- Definitions of occupancy number and occupancy rate
- Initial coin state
- Precise concentration interval for the DFT walk
- Details of the classical and lazy classical comparison
