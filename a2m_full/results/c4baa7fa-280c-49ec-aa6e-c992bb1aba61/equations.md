# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Find the minimum-metric (maximum-likelihood) path through a convolutional-code decoding trellis with known received data, using a uniform superposition over all f^N legal paths, a phase oracle on the path metric, and Grover-style amplitude amplification.

Scope: One tiny instance: binary rate-1/2 convolutional code with f=2, small constraint length (e.g. Q=3, so 4 states), N=3 or 4 steps, hard-decision Hamming metric, known start state 0, no tail. Build one Grover iteration (threshold-marking oracle plus diffusion) with a fixed classical threshold T and a known or swept iteration count. Out of scope: the paper's specialized amplitude amplification, the butterfly/FFT efficiency analysis, soft-decision metrics, and the full Durr-Hoyer loop (classical outer loop only, described in postprocessing).

## Symbols

- $N$: number of decode steps (frame length); domain: positive integer, small (3 or 4)
- $Q$: constraint length; the trellis has 2^{Q-1} states; domain: integer >= 2
- $f$: fanout, number of transitions out of each state; domain: power of 2, f=2 here
- $b_t$: branch choice (input bit) at step t; domain: {0,..,f-1}
- $s_t$: trellis state after t steps, s_0=0; domain: {0,..,2^{Q-1}-1}
- $g$: branch output map (state, branch) -> n code bits, fixed by generator polynomials; domain: {0,1}^n
- $r_t$: received n-bit symbol at step t (classical constant); domain: {0,1}^n
- $M(b)$: total path metric (Hamming distance) of path b; domain: integer in [0, nN]
- $T$: threshold; paths with M<T are marked; domain: integer
- $K$: number of marked paths; domain: integer >= 1
- $R$: number of Grover iterations; domain: nonnegative integer

## eq_1: Uniform path superposition

$$
|\psi_0\rangle = H^{\otimes N\log_2 f}|0\rangle = f^{-N/2}\sum_{b\in\{0,\dots,f-1\}^N}|b\rangle
$$

Tensor-product state over all legal paths, identified with branch sequences from the known start state.

Provenance: `abstract_inferred`. The abstract claims an efficiently preparable tensor-product superposition of legal paths; Hadamards on the branch registers are the simplest realization, which is my assumption.

Abstract evidence: The tensor-product structure of the butterfly diagram corresponds to a quantum superposition that we show can be efficiently prepared.

Equation assumptions:

- f is a power of 2
- Hadamards are used instead of a paper-specific preparation

## eq_2: Shift-register trellis update and path metric

$$
s_{t}=\big((s_{t-1}\ll 1)\,|\,b_t\big)\bmod 2^{Q-1},\quad M(b)=\sum_{t=1}^{N}d_H\big(g(s_{t-1},b_t),r_t\big)
$$

Exact (not approximate) state update and Hamming-distance accumulation along the path.

Provenance: `standard_background`. Standard convolutional-code trellis and hard-decision metric; the sketch supplies this form, the abstract does not state it.

Equation assumptions:

- binary shift-register code
- s_0=0
- hard-decision Hamming metric
- received data hardwired as constants

## eq_3: Threshold phase oracle

$$
O_T|b\rangle=(-1)^{[M(b)<T]}|b\rangle
$$

Compute M into a work register, compare with T into an ancilla held in |->, then uncompute so only the path register keeps the phase.

Provenance: `assumption`. Abstract says the phase is a function of path probability and that the method is function-optimum finding; the threshold form is a proposed concrete choice. The paper's actual phase function is not given.

Equation assumptions:

- Grover-threshold variant, not the direct exp(i pi M/Mmax) phase
- Work and ancilla qubits are returned to |0>

## eq_4: Diffusion about uniform superposition

$$
D=H^{\otimes m}\,(2|0\rangle\langle0|-I)\,H^{\otimes m}=2|\psi_0\rangle\langle\psi_0|-I,\quad m=N\log_2 f
$$

Standard Grover reflection about the uniform path state.

Provenance: `standard_background`. Standard amplitude amplification; the paper uses a specialized procedure not specified in the abstract.

Equation assumptions:

- Plain Grover diffusion substitutes for the specialized procedure

## eq_5: Iteration count and success probability

$$
R\approx\frac{\pi}{4}\sqrt{\frac{f^N}{K}},\quad P_{succ}=\sin^2\big((2R+1)\theta\big),\ \sin\theta=\sqrt{K/f^N}
$$

Standard Grover count; the final state is (D O_T)^R |psi_0>.

Provenance: `standard_background`. Textbook Grover analysis; K unknown in practice so randomized counts are used.

Equation assumptions:

- K is known for a fixed-R test, or R is swept/randomized

## Registers

- path: N*log2(f) (= N for f=2) qubits; branch choices b_1..b_N; measured at the end
- state: Q-1 per step or reused with uncompute qubits; work: trellis state s_t, uncomputed afterwards
- metric: ceil(log2(nN+1)) qubits; work: accumulates Hamming distance M
- flag: 1 qubits; oracle ancilla in |-> for phase kickback

## Initial state

All qubits |0>, flag prepared in |-> (X then H); path register put into uniform superposition by H.

## Measurement

Measure only the path qubits. In Qiskit, bit i (little-endian, bits[::-1][i]) is the branch bit b_{i+1}.

## Classical postprocessing

Recompute M for the measured path classically and check M<T. Decode the message bits from the branch bits (the input bits are the branch choices). Optionally lower T to the measured M and repeat (Durr-Hoyer style) until no marked path remains. Compare against brute-force minimum for the tiny instance.

## Algorithm steps

1. Apply H to every path qubit and prepare the flag in |->. (eq_1)
2. Compute states s_t by shift-register update (CNOT/SWAP), compute branch outputs, XOR with the hardwired r_t, and add the Hamming weights into the metric register. (eq_2)
3. Compare metric < T into the flag for phase kickback, then uncompute the metric and state registers. (eq_3)
4. Apply diffusion on the path register. (eq_4)
5. Repeat the oracle plus diffusion R times, with R chosen per the Grover count or randomized for unknown K. (eq_5)

## Assumptions

- Chosen instance: f=2, Q=3, N=3 or 4, generators like (7,5) octal, small received word
- Hamming metric, known start state, no tail
- Threshold-marking oracle replaces the paper's phase function
- Total qubits must fit under the cap, so state and metric registers are reused or the instance is kept very small

## Missing information

- The paper's exact phase function of path probability
- The specialized amplitude amplification procedure
- How the butterfly/FFT structure reduces cost, and the exact complexity claim
- Concrete code generators, the trellis termination convention, and the soft-decision metric
- Qubit cap and query budget for this task
