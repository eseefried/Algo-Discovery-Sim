# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Find the most probable legal path through a decoding trellis (hidden Markov model with fanout f much less than the number of states) given received data, by preparing a superposition over all legal paths with path-probability-dependent phase and applying amplitude amplification.

Scope: Tiny assumed instance: a trellis with N=2 decode steps, binary fanout f=2, and 2^(Q-1) states with Q=3. The scope covers uniform path superposition over legal paths, a generic path-score phase, and a generic amplitude amplification iteration. The specialized amplitude amplification, the FFT-butterfly-based state preparation, the speedup analysis and the Quantum Function Optimum Finding details are outside scope.

## Symbols

- $Q$: constraint length of the convolutional code (state space size grows exponentially with Q); domain: positive integer
- $N$: decode frame length (number of trellis steps); domain: positive integer
- $f$: fanout: number of possible transitions from a given state; domain: integer, 1<=f<<2^(Q-1) typically
- $p$: legal path (s_0,...,s_N) through the trellis; domain: element of legal path set P
- $P$: set of legal paths, |P| = S_0 f^N for S_0 allowed start states; domain: finite set
- $y$: received data; domain: sequence of length N
- $\Pr(p|y)$: probability of path p given received data; domain: [0,1]
- $\phi(p)$: phase assigned to path p as a function of its probability (form not specified); domain: real
- $\theta$: Grover-type angle with sin^2(theta)=M/|P|; domain: (0,pi/2)

## eq_1: Legal path count

$$
|P| = S_0\, f^{N}
$$

Number of legal paths when each state has f outgoing transitions and S_0 start states are allowed.

Provenance: `abstract_inferred`. Inferred from the fanout-dependence claim; the counting itself is elementary trellis combinatorics.

Abstract evidence: the performance of the QVA depends on the fanout (number of possible transitions from any given state in the hidden Markov model)

Equation assumptions:

- Constant fanout f
- S_0 start states

## eq_2: Path superposition with phase

$$
|\psi\rangle = \frac{1}{\sqrt{|P|}}\sum_{p\in P} e^{i\phi(p)}|p\rangle
$$

Superposition of all legal paths with phase being a function of path probability given y.

Provenance: `abstract_inferred`. Direct reading of the claim; uniform amplitudes are assumed since the abstract does not state them.

Abstract evidence: constructs a superposition of states which correspond to all legal paths through the decoding lattice, with phase a function of the probability of the path being taken given received data

Equation assumptions:

- Uniform amplitudes
- Phase function phi unspecified

## eq_3: Phase as function of path probability

$$
\phi(p)=g\big(\Pr(p\mid y)\big),\quad \Pr(p\mid y)\propto \prod_{t=1}^{N}\Pr(y_t\mid s_{t-1},s_t)\Pr(s_t\mid s_{t-1})
$$

Phase depends on the path posterior, factorized by the HMM structure; g is not specified.

Provenance: `assumption`. Standard HMM factorization; the mapping g is a placeholder because the abstract gives no schedule.

Equation assumptions:

- g unspecified
- Memoryless first-order HMM

## eq_4: Grover-type amplification

$$
|\psi_k\rangle=(-U_\psi U_{\mathrm{mark}})^k|\psi\rangle,\quad \Pr(\text{success})=\sin^2((2k+1)\theta)
$$

Generic amplitude amplification toward the marked most-probable path; the specialized procedure of the paper is not reproduced.

Provenance: `standard_background`. Textbook amplitude amplification, standing in for the paper's specialized procedure.

Equation assumptions:

- Marking oracle for the best path assumed to exist
- M marked paths, sin^2(theta)=M/|P|

## Registers

- path: N*ceil(log2 f) qubits (plus start-state qubits) qubits; encodes the sequence of transition choices defining a legal path
- phase_ancilla: unknown qubits; workspace to compute path score and phase, uncomputed afterward

## Initial state

All-zero state on the path register, assumed.

## Measurement

Measure the path register in the computational basis to read out the candidate most probable path.

## Classical postprocessing

Map the measured transition choices to a state sequence and decoded bits; optionally verify the path score classically.

## Algorithm steps

1. Prepare uniform superposition over legal paths, using a tensor product of per-step transition choices (assumed Hadamards for f=2). (eq_1, eq_2)
2. Apply the path-score-dependent phase. (eq_2, eq_3)
3. Apply generic amplitude amplification iterations toward the most probable path. (eq_4)

## Assumptions

- Tiny instance Q=3, N=2, f=2 chosen by this reconstruction
- Uniform amplitudes and generic Grover amplification used in place of the unspecified specialized procedure
- Phase function g is a placeholder

## Missing information

- Explicit phase function and oracle for marking the optimum path
- Details of the specialized amplitude amplification
- Efficient FFT-butterfly-based state preparation circuit
- Speedup and complexity statements
- Quantum function optimum finding details
