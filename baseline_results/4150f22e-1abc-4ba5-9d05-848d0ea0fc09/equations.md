# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Maximum-likelihood (Viterbi) decoding of a binary convolutional code: given a received noisy word y of N frames, find the input sequence x (equivalently the legal trellis path) that maximises P(y|x). The abstract proposes a quantum Viterbi algorithm (QVA) that prepares a superposition over all legal trellis paths with a probability-dependent phase and then applies a specialised amplitude-amplification / quantum optimum-finding procedure so that the most probable path is measured with high probability.

Scope: No experiment scope was supplied, so one smallest useful construction is chosen (assumption): a rate-1/2, memory-1 (constraint length Q=2, fanout 2) binary convolutional code, hard-decision BSC channel, N=3 decode frames, trellis starting in the zero state. In this fanout-2 setting every input bit string x in {0,1}^N is a legal path, so the 'tensor-product' path superposition is H^{\otimes N}. The path metric is the Hamming distance d(x) between y and the codeword, which is an affine function of log P(y|x). Because the paper's specialised amplitude-amplification procedure is not described in the abstract, the baseline uses the standard Durr-Hoyer threshold-oracle minimum finding (Grover iterations) as a stand-in. A concrete received word y=(11,01,11) is fixed so that the unique ML path is x=101 with d=1. Outside scope: large-Q codes, general HMMs with fanout-restricted transition structure, the explicit butterfly/FFT-style preparation of constrained path superpositions, the paper's actual phase function and specialised amplification, and any complexity/speedup claims.

## Symbols

- $N$: number of decode frames (trellis depth); instance value N=3; domain: positive integer
- $Q$: constraint length of the convolutional code; instance value Q=2 (memory 1, 2 trellis states); domain: positive integer
- $x=(x_1,\dots,x_N)$: input (information) bit sequence; indexes a legal trellis path; x_0:=0 is the initial encoder state; domain: \{0,1\}^N
- $c_t(x)=(c_t^{(1)},c_t^{(2)})$: pair of code bits emitted at frame t; domain: \{0,1\}^2
- $y=(y_1,\dots,y_N)$: received hard-decision word, y_t in {0,1}^2; instance y=(11,01,11); domain: \{0,1\}^{2N}
- $p$: crossover probability of the binary symmetric channel; domain: (0,1/2)
- $d(x)$: path metric: Hamming distance between y and the codeword of x; domain: \{0,\dots,2N\}
- $T$: current threshold in the minimum-finding loop; domain: \{0,\dots,2N+1\}
- $\varphi(\cdot)$: unspecified phase function of the path probability used by the paper's QVA; domain: real-valued function
- $O_T$: threshold phase oracle marking paths with d(x)<T; domain: unitary on the path register
- $G_T$: Grover/amplitude-amplification iterate for threshold T; domain: unitary on the path register
- $m$: metric register width, m=\lceil\log_2(2N+1)\rceil; instance m=3; domain: positive integer

## eq_1: Tensor-product superposition over all legal paths

$$
|\psi_0\rangle = H^{\otimes N}|0\rangle^{\otimes N} = \frac{1}{\sqrt{2^N}}\sum_{x\in\{0,1\}^N}|x_1 x_2 \cdots x_N\rangle
$$

Uniform superposition over all input sequences; for a fanout-2 trellis with unconstrained inputs every x is a legal path, so the path superposition factorises as a tensor product of single-qubit states.

Provenance: `abstract_inferred`. The abstract claims the legal-path superposition has tensor-product structure and is efficiently preparable; for the chosen fanout-2 instance this is exactly H^{\otimes N}. The general constrained-HMM preparation is not reconstructed.

Abstract evidence: The tensor-product structure of the butterfly diagram corresponds to a quantum superposition that we show can be efficiently prepared.

Equation assumptions:

- Fanout 2 with every input sequence legal (binary convolutional code, zero initial state).
- Qubit t of the path register holds x_t; register ordering x_1 is the most significant / leftmost qubit.

## eq_2: Trellis / encoder for the Q=2 rate-1/2 instance

$$
c_t^{(1)} = x_t,\qquad c_t^{(2)} = x_t \oplus x_{t-1},\qquad x_0 = 0,\quad t=1,\dots,N
$$

Memory-1 convolutional encoder (generators (1, 1+D)); the trellis state at time t is x_t and each state has fanout 2.

Provenance: `assumption`. A concrete smallest nontrivial convolutional code is needed to make the metric computable; this specific code is not given in the abstract.

Equation assumptions:

- Code choice is illustrative only.

## eq_3: Path metric and its relation to path probability (BSC)

$$
d(x) = \sum_{t=1}^{N}\mathrm{wt}\big(y_t \oplus c_t(x)\big),\qquad \log P(y\mid x) = -\,d(x)\,\log\frac{1-p}{p} + 2N\log(1-p),\qquad \hat{x} = \arg\min_{x} d(x)
$$

Hamming-distance path metric; on a memoryless BSC the log-likelihood is an exactly affine, strictly decreasing function of d(x), so the most probable path is the minimum-metric path. For the instance y=(11,01,11), d(101)=1 is the unique minimum.

Provenance: `standard_background`. Standard Viterbi/ML decoding relation for hard-decision BSC; needed to connect 'probability of the path' in the abstract to a computable integer metric.

Equation assumptions:

- Hard-decision BSC with 0<p<1/2, equiprobable inputs.

## eq_4: Phase-encoded path superposition (paper's construction, form unknown)

$$
|\psi_\varphi\rangle = \frac{1}{\sqrt{2^N}}\sum_{x} e^{\,i\,\varphi\left(P(y\mid x)\right)}|x\rangle,\qquad \text{reversible metric computation: } U_d|x\rangle|0\rangle^{\otimes m} = |x\rangle|d(x)\rangle
$$

The abstract states that each legal path carries a phase that is a function of its posterior/likelihood; the specific function \varphi is not given. The baseline realises the needed information instead by reversibly computing d(x) into an m-qubit metric register (first equality is the abstract's claim; second is the baseline substitute).

Provenance: `abstract_inferred`. Directly paraphrases the abstract's description of the constructed superposition; the exact \varphi and its use in the specialised amplification are unknown, so the baseline uses a computed-metric register.

Abstract evidence: with phase a function of the probability of the path being taken given received data

Equation assumptions:

- \varphi is unspecified; the baseline does not rely on it.
- U_d is a reversible arithmetic circuit computing eq_3 from eq_2 (XOR and popcount adders).

## eq_5: Threshold marking oracle

$$
O_T|x\rangle = (-1)^{[\,d(x) < T\,]}\,|x\rangle,\qquad O_T = U_d^{\dagger}\,(I\otimes C_{<T})\,U_d
$$

Phase oracle that flips the sign of every path whose metric is strictly below the current threshold; implemented by computing d(x), applying a comparator-controlled phase, and uncomputing.

Provenance: `standard_background`. Standard construction for Durr-Hoyer quantum minimum finding; used as a stand-in for the paper's 'specialized amplitude amplification procedure', which the abstract does not specify.

Equation assumptions:

- C_{<T} is a comparator phase gate acting on the metric register (phase kickback on an ancilla).

## eq_6: Amplitude-amplification iterate and success probability

$$
G_T = \big(2|\psi_0\rangle\langle\psi_0| - I\big)\,O_T,\qquad P_{\text{succ}}(k) = \sin^2\!\big((2k+1)\theta_T\big),\quad \sin\theta_T = \sqrt{\frac{|\{x: d(x)<T\}|}{2^N}}
$$

Grover iterate with the uniform-superposition reflection; after k iterations the probability of measuring a path with metric below T is sin^2((2k+1)theta_T). For the instance (N=3, T=2, one marked path) k=2 gives P_succ = sin^2(5 asin(1/sqrt 8)) ~ 0.945.

Provenance: `standard_background`. Standard amplitude amplification; the abstract only states that a specialised procedure is applied 'one or more times' to boost the most probable path, consistent with an iterative minimum-finding loop.

Equation assumptions:

- Number of marked paths unknown in general; Durr-Hoyer randomised iteration counts (or exponential search) handle this.
- The paper's specialised procedure may differ materially from this generic iterate.

## Registers

- path: N (instance: 3) qubits; Holds the input bit sequence x; one qubit per frame, qubit t = x_t; indexes the legal trellis path
- metric: m = ceil(log2(2N+1)) (instance: 3) qubits; Reversibly computed Hamming-distance metric d(x) in binary (unsigned, little-endian assumed)
- flag: 1 qubits; Comparator output / phase-kickback ancilla for the threshold test d(x) < T

## Initial state

|0\rangle^{\otimes N}_{\text{path}} \otimes |0\rangle^{\otimes m}_{\text{metric}} \otimes |-\rangle_{\text{flag}} (flag prepared as (|0\rangle-|1\rangle)/\sqrt{2} for phase kickback)

## Measurement

Computational-basis measurement of the N-qubit path register yielding a candidate input sequence x'. The metric register is returned to |0...0> by uncomputation and need not be measured.

## Classical postprocessing

Compute d(x') classically (eq_3); keep the best candidate and update the threshold T; repeat the quantum loop until the threshold stops decreasing or an iteration budget is exhausted. Output x̂ = best candidate as the decoded information bits (instance: expected x̂ = 101 with d=1).

## Algorithm steps

1. Prepare the tensor-product superposition over all legal trellis paths by applying H to every path qubit. (eq_1)
2. Classically fix the received word y (instance y=(11,01,11)) and the encoder/trellis map; initialise threshold T (e.g. T = 2N+1, or T = d(x_r)+? from a random classical path x_r as in Durr-Hoyer). (eq_2, eq_3)
3. Apply the threshold oracle: compute d(x) into the metric register with U_d, apply the comparator phase for d(x) < T via the flag ancilla, and uncompute U_d. (eq_4, eq_5)
4. Apply the reflection about |psi_0> (H^{\otimes N}, phase flip on |0...0>, H^{\otimes N}) to complete one Grover iterate G_T; repeat k times with k chosen for the (possibly unknown) number of marked paths. (eq_6)
5. Measure the path register, obtain candidate x'; classically compute d(x'); if d(x') < T set T = d(x') and repeat from step 1 ('applied one or more times'), otherwise stop. (eq_3, eq_6)

## Assumptions

- No experiment scope was given; a smallest useful instance was chosen: Q=2, rate-1/2, generators (1, 1+D), N=3, zero initial state, hard-decision BSC, received word y=(11,01,11).
- In this fanout-2 instance all 2^N input sequences are legal paths, so the legal-path superposition is exactly H^{\otimes N}; the paper's general butterfly/tensor-product preparation for constrained HMMs is not reconstructed.
- The paper's 'specialized amplitude amplification procedure' and the phase function \varphi are unknown; the baseline substitutes standard Durr-Hoyer threshold-oracle minimum finding with a reversibly computed metric register.
- Metric register is unsigned binary of width ceil(log2(2N+1)); no modular wrap-around occurs since d(x) <= 2N.

## Missing information

- Exact phase function \varphi relating path probability to the phase of each path amplitude, and how that phase is consumed by the amplification procedure.
- Definition of the 'specialized amplitude amplification procedure' and its iteration schedule ('one or more times').
- How the trellis/butterfly tensor-product structure is used to prepare the superposition over legal paths for general fanout and constrained HMM transition structure (large Q, non-binary inputs).
- Conditions under which the claimed better-than-classical performance holds (dependence on fanout, Q, N) and the asserted complexity.
- Treatment of soft-decision metrics / general HMM emission probabilities (only hard-decision Hamming metric is used here).
- Termination/tail-biting conventions for the trellis and the final encoder state.
