# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantum Viterbi algorithm (QVA): find the most probable path through a decoding trellis (hidden Markov model, e.g. convolutional code with constraint length Q and N decode frames) by building a superposition over all legal paths with phase depending on path probability given received data, then using specialized amplitude amplification so the most probable path is likely to be measured.

Scope: Abstract-level reconstruction of the QVA problem and key relations only; exact state-preparation circuits, oracle construction, and complexity bounds are not given in the abstract. Small finite trellis instance assumed for any illustration.

## Symbols

- $Q$: constraint length of the convolutional code (state-space size scale); domain: positive integer
- $N$: number of frames in the decode window (trellis length); domain: positive integer
- $F$: fanout: number of possible transitions from a given state in the hidden Markov model; domain: positive integer, generally much less than Q
- $\pi$: a legal path through the decoding lattice; domain: sequence of N states consistent with trellis transitions
- $P(\pi|r)$: probability of path pi given received data r; domain: [0,1]

## eq_1: Path superposition with probability-dependent phase

$$
|\Psi\rangle=\frac{1}{\sqrt{|\mathcal{L}|}}\sum_{\pi\in\mathcal{L}} e^{i\phi(P(\pi|r))}|\pi\rangle
$$

Uniform superposition over the set L of legal paths with phase a function of path probability.

Provenance: `abstract_inferred`. Direct formalization of the abstract sentence; phase function phi and uniform amplitudes are assumed.

Abstract evidence: The QVA constructs a superposition of states which correspond to all legal paths through the decoding lattice, with phase a function of the probability of the path being taken given received data.

Equation assumptions:

- Uniform amplitudes over legal paths
- phi is an unspecified monotone function

## eq_2: Most probable path objective

$$
\pi^*=\arg\max_{\pi\in\mathcal{L}}P(\pi|r)
$$

The Viterbi goal: the maximum-likelihood path.

Provenance: `abstract_inferred`. Target of amplification stated in the abstract.

Abstract evidence: the most probable path has a high probability of being measured

## eq_3: Number of legal paths

$$
|\mathcal{L}|\approx Q\,F^{N}
$$

Count of trellis paths for Q start states and fanout F over N steps (approximate, background).

Provenance: `standard_background`. Standard trellis counting; consistent with performance depending on fanout F rather than Q.

Equation assumptions:

- Each state has exactly F outgoing transitions

## Registers

- path: N registers of ceil(log2 F) qubits each, plus start-state register of ceil(log2 Q) qubits (assumed encoding) qubits; encodes a legal path as start state plus a branch choice per frame
- phase/metric ancilla: unknown qubits; holds the path metric used to impose phase phi(P(pi|r)); uncomputed afterwards

## Initial state

All-zero registers; assumed encoding of a path as start state plus N branch choices.

## Measurement

Measure the path registers (start state and branch choices) in the computational basis after amplitude amplification; the outcome is the candidate most probable path pi*, with high probability if amplification succeeds.

## Classical postprocessing

Decode the measured bits into the state sequence and the corresponding information bits. Optionally compute P(pi|r) classically to check the candidate and repeat the run if it is not satisfactory.

## Algorithm steps

1. Prepare a uniform superposition over legal paths using the tensor-product (butterfly-like) structure, e.g. Hadamard-type gates on the start-state and branch registers. (eq_3, eq_1)
2. Compute the path metric from received data r into an ancilla, apply a phase phi(P(pi|r)), and uncompute the ancilla to obtain |Psi>. (eq_1)
3. Apply the specialized amplitude amplification (oracle details unspecified in the abstract) one or more times to boost the amplitude of the maximum-probability path. (eq_2)

## Assumptions

- Uniform fanout F
- Phase function phi unspecified
- Path register encoding assumed as start state plus branch choices
- Computational-basis measurement of path registers assumed
- Optional classical verification and repetition assumed

## Missing information

- Explicit phase function
- State-preparation circuit details
- Amplitude amplification oracle and iteration count
- Complexity bounds
- Metric ancilla size
- Success probability and number of repetitions
