# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate a lazy discrete-time quantum walk (coin states L,S,R) on a cycle of N=2^n sites with a 3x3 DFT coin, and classically compute position distributions, moments, and occupancy number/rate for comparison with Hadamard, classical and lazy classical walks.

Scope: One tiny instance: n=4 (N=16), coin in 2 qubits with |3> idle, t=1..5 steps (2t+1<N), statevector readout, no measurements. Occupancy number/rate comparison and moment-scaling fit are classical post-processing. Out of scope: analytic derivation of moment orders, the exact DFT-coin limiting density, and the paper's exact occupancy definition and threshold.

## Symbols

- $n$: number of position qubits; domain: integer, n=4
- $N$: cycle size 2^n; domain: integer, 16
- $t$: number of walk steps; domain: integer, 1..5 so that 2t+1<=N
- $x$: position, taken as a signed representative mod N; domain: integer in [-N/2, N/2-1]
- $C$: 3x3 DFT coin embedded in the 2-qubit coin space, with |3> fixed; domain: 4x4 unitary
- $S$: conditional shift; domain: unitary on coin⊗position
- $P(x,t)$: position probability distribution; domain: [0,1]
- $M_k(t)$: k-th moment of position; domain: real
- $\theta$: occupancy threshold; domain: positive real, assumed 1/(2t+1)
- $\rho(t)$: occupancy rate; domain: [0,1]

## eq_1: Lazy walk step

$$
U=S\,(C\otimes I),\quad S=|L\rangle\langle L|\otimes T^{-1}+|S\rangle\langle S|\otimes I+|R\rangle\langle R|\otimes T+|3\rangle\langle 3|\otimes I,\quad T|x\rangle=|x+1 \bmod N\rangle
$$

One step of the lazy walk with a stay option; the idle coin state |3> gets no shift (never populated).

Provenance: `assumption`. The abstract mentions lazy walks with a DFT coin; the specific 2-qubit encoding is a proposed construction.

Equation assumptions:

- Coin encoding |L>=|00>, |S>=|01>, |R>=|10>, |3>=|11>
- The coin acts as identity on |3>

## eq_2: DFT coin

$$
C=\begin{pmatrix}F_3&0\\0&1\end{pmatrix},\ (F_3)_{jk}=\tfrac{1}{\sqrt3}e^{2\pi i jk/3}
$$

3-dimensional DFT coin padded to 4 dimensions.

Provenance: `standard_background`. The abstract names a DFT coin; the matrix is the standard DFT. The sign convention and embedding are assumptions.

Equation assumptions:

- F_3 is not a standard-library gate; it must be built from ordinary gates (for example via decomposition into rotations and controlled gates), or the coin must be replaced by a Hadamard-like 3-state coin. This is unresolved.

## eq_3: State and distribution

$$
|\psi_t\rangle=U^t|\psi_0\rangle,\ |\psi_0\rangle=\tfrac{1}{\sqrt2}(|L\rangle+i|R\rangle)\otimes|0\rangle,\ P(x,t)=\sum_{c}|\langle c,x|\psi_t\rangle|^2
$$

Initial symmetric coin state, evolution, and marginal position distribution.

Provenance: `assumption`. Symmetric initial state is a proposed choice; the marginal is standard.

Equation assumptions:

- Initial coin state is symmetric, giving a symmetric distribution only if the coin and shifts respect the symmetry; this is not guaranteed for a DFT coin and must be checked numerically

## eq_4: Moments

$$
M_k(t)=\sum_x x^k P(x,t),\quad M_k(t)=O(t^k)
$$

k-th moment, with the claim of O(t^k) growth.

Provenance: `abstract_inferred`. The abstract states O(t^n) growth for the n-th moment; the log-log slope fit is a proposed test. For k=1 the moment may be zero by symmetry, so use |x|^k or even k.

Abstract evidence: lazy quantum walks have $O(t^{n})$ order of the n-th moment of the corresponding probability distribution

Equation assumptions:

- Cycle wraparound is negligible because 2t+1<N

## eq_5: Occupancy number and rate

$$
\mathrm{Occ}(t)=\#\{x:|x|\le t,\ P(x,t)>\theta\},\quad \rho(t)=\frac{\mathrm{Occ}(t)}{2t+1},\ \theta=\frac1{2t+1}
$$

Occupancy number and rate over the reachable range.

Provenance: `assumption`. The abstract introduces occupancy number and rate but does not define them; this is a guessed definition with a guessed threshold.

Equation assumptions:

- Threshold 1/(2t+1) is chosen; the paper's may differ

## Registers

- pos: 4 qubits; position on the cycle, little-endian integer encoding, qubits 0..3
- coin: 2 qubits; coin, qubits 4..5, little-endian value 0=L, 1=S, 2=R, 3 idle

## Initial state

pos=|0>, coin=(|L>+i|R>)/sqrt2 = (|00>+i|10>)/sqrt2 in coin bits (c1c0). Prepare with H on coin qubit 1, S on it, and a coin-qubit-0 stay in |0>; the coin value then encodes L=0, R=2. No initialize.

## Classical postprocessing

From the statevector index = coin*N + pos (coin as the high qubits), sum |amp|^2 over coin to get P(x,t). Map x>=N/2 to x-N. Compute M_k(t), fit slope of log M_k vs log t, find the interval holding most of the probability, and compute Occ and rho for each walk type; classical comparison distributions come from convolution or the Hadamard-walk simulation.

## Algorithm steps

1. Prepare the initial coin state with H and S on the coin MSB. (eq_3)
2. Repeat t times: apply coin C on the coin register, then conditional shifts: a controlled decrement when the coin is |00>, a controlled increment when the coin is |10>, built from multi-controlled X gates (ripple of MCX), nothing for |01>. Ancillas not needed. (eq_1, eq_2)
3. Read the statevector (no measurement), marginalise over coin to get P(x,t), then compute moments, a log-log slope fit, the concentration interval, and the occupancy number and rate; compare against a classical simulation of the Hadamard, binomial and lazy classical walks. (eq_3, eq_4, eq_5)

## Assumptions

- n=4 positions, t<=5 so wraparound is absent
- 3-state DFT coin padded into 2 qubits with an idle 4th state
- Occupancy threshold 1/(2t+1) and range |x|<=t are assumed definitions
- Total 6 qubits, within the cap if the cap is at least 6

## Missing information

- Paper's exact lazy walk definition (the coin may be mixed with a laziness parameter instead of a 3-state coin)
- Exact occupancy number/rate definition and threshold
- Gate decomposition of the 3x3 DFT coin into standard gates
- Whether the claim about the interval compares to t/sqrt2 for a specific coin and initial state
