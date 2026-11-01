# Equation to Qiskit

Builds the eq_1 path-superposition state-preparation operation for a rate-1/n binary feedforward convolutional-code trellis. Hadamards on all path bits create a uniform superposition over all legal paths (start memory plus N input bits). A diagonal, ancilla-free phase exp(-i*gamma*HammingDistance(path output, received data)) is then applied using CNOT-parity, phase and uncompute. Amplitude amplification is not implemented because the abstract gives no oracle.

Source equation run: `e594cc32-cf6b-4228-8c46-dc45e598b6a6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit i (0..M-1, M=(K-1)+N) holds path bit x_i; qubit 0 is the earliest bit (initial encoder memory), least significant in basis index
- Example: K=3, N=4 gives 6 qubits: q0,q1 = start memory bits, q2..q5 = input bits of frames 0..3
- Frame t uses window qubits t..t+K-1; no ancillas

## Assumptions

- Binary feedforward rate-1/n convolutional code with n=len(generators); generator bit j acts on window position j
- Hard-decision received bits; BSC-like additive metric
- All start memory states are legal and uniformly weighted
- Input state is |0...0> prepared by the runner; Hadamards create the superposition inside the operation
- gamma is a real user-supplied scale

## Unresolved issues

- Specialized amplitude amplification not implemented
- Abstract does not specify the true phase function phi or encoding used by the QVA
- Complexity advantages (dependence on fanout) are not represented
- Trellis structure/butterfly FFT-based preparation is not used; plain Hadamards suffice for uniform superposition here

## Equation mapping

- `eq_1`: implemented; build_circuit: Hadamard layer (uniform amplitudes over legal paths) and parity-phase loop (phi = -gamma*Hamming distance). Prepares (1/sqrt(2^M)) sum_pi exp(i*phi(pi))|pi> from an all-zero input, with concrete phi(P(pi|r)) = -gamma*d_H(output(pi), r), which is a monotone function of the BSC log-likelihood.
- `eq_2`: out_of_scope; no code location. The argmax objective is the goal of the amplitude amplification, which the abstract does not specify and is not implemented. The circuit only encodes path quality in phase.
- `eq_3`: background; no code location. Path count Q*F^N: for the shift-register trellis here Q=2^(K-1), F=2, so |L|=2^(K-1+N)=2^M, matching the number of basis states superposed. Used only for the sizing and validation of qubit count.

## Specification changes

- eq_1: Chose a concrete phase function: phi = -gamma times Hamming distance between convolutional-encoder output and received hard-decision bits; the path is encoded as raw bit string x (initial memory plus input bits) with fanout F=2 rather than a ceil(log2 F)-qubit branch register. Reason: The abstract leaves phi and the encoding unspecified; a concrete additive metric is required for a unitary circuit without ancilla metric register.
- eq_2: Amplitude amplification and optimal-path search are omitted; the construction is narrowed to the state preparation of eq_1. Reason: No oracle, reflection, or iteration count is given in the abstract.
- eq_3: Replaced the approximate count Q F^N by exact 2^(K-1+N) for binary feedforward encoders; the start state is a free (uniformly superposed) memory. Reason: Exact for the chosen trellis.
- eq_1: The ancilla metric compute/uncompute step is replaced by direct CNOT-parity phase gates. Reason: Additive Hamming metric is diagonal, so no ancilla is needed.
