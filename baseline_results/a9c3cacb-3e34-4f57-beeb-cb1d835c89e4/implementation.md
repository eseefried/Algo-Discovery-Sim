# Equation to Qiskit

Qiskit implementation of one Durr-Hoyer-style threshold-oracle amplitude-amplification stage of the baseline quantum Viterbi reconstruction for a rate-1/2, memory-1 (Q=2) binary convolutional code with generators (1, 1+D) on a hard-decision BSC. build_circuit(instance) builds: optional H^{⊗N} path superposition (eq_1), then `iterations` Grover iterates, each consisting of the threshold oracle O_T = U_d^† C_{<T} U_d (U_d reversibly computes the Hamming-distance metric d(x) between the received word and the codeword into a little-endian metric register via controlled increments; C_{<T} applies a -1 phase to every metric value below the threshold using multi-controlled Z gates) followed by the reflection about the uniform superposition. All ancillas start and end in |0>. The classical outer loop (measure, update threshold, repeat) is left to the runner.

Source equation run: `4150f22e-1abc-4ba5-9d05-848d0ea0fc09`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..2 : path register, qubit i holds information bit x_{i+1} (x_1 on qubit 0, x_3 on qubit 2); x_0 = 0 is implicit
- qubits 3..5 : metric register, little-endian unsigned Hamming distance d(x) (qubit 3 = LSB); starts in |0>, returned to |0> after each oracle
- total 6 qubits for the example (N + ceil(log2(2N+1))); cap 12
- input state expected from runner: |0...0>; with prepare_superposition=true the circuit applies H^{3} itself; expected dominant output path for the example is x=(1,0,1) i.e. bitstring '101' read as path[2]path[1]path[0]

## Assumptions

- Hard-decision BSC with 0 < p < 1/2, so minimum Hamming distance equals maximum likelihood.
- Metric register width m = ceil(log2(2N+1)) guarantees no modular wrap-around since 0 <= d(x) <= 2N.
- Path qubit i (0-indexed) stores x_{i+1}; Qiskit's little-endian bitstring therefore reads x_N ... x_1.
- Threshold T is an integer in 0..2N+1 chosen classically by the runner (T = 2N+1 marks every path; T = 0 marks none).
- For the example instance (y = 11,01,11, T = 2, k = 2) the unique marked path is x = 101 with d = 1 and the analytic success probability is sin^2(5*asin(1/sqrt(8))) ~ 0.945; this is not verified here.
- Qubit cap N + m <= 12 (e.g. N <= 7 for this code).

## Unresolved issues

- The paper's specialised amplitude-amplification procedure and phase function phi are unknown; the generic Durr-Hoyer Grover iterate is a stand-in and may differ materially.
- Number of marked paths for a given threshold is generally unknown, so the runner must choose iteration counts (e.g. randomised/exponential schedule) classically.
- Soft-decision metrics, general HMM emission probabilities, large constraint length Q and the efficient butterfly-structured preparation of constrained legal-path superpositions are not implemented.
- Multi-controlled gates (mcx/mcp) are used as logical gates; no ancilla-based decomposition or depth optimisation is attempted.

## Equation mapping

- `eq_1`: implemented; build_circuit: H on every path qubit when prepare_superposition is true (comment '# eq_1'). Uniform tensor-product superposition over all 2^N input sequences, which are all legal paths for the fanout-2 trellis.
- `eq_2`: implemented; _metric_circuit: c^(1)_t = x_t uses path[i] directly; c^(2)_t = x_t XOR x_{t-1} realised by temporarily CNOTing path[i-1] into path[i] (x_0 = 0 handled by the i == 0 branch). Memory-1 encoder with generators (1, 1+D).
- `eq_3`: implemented; _add_code_bit and _controlled_increment inside _metric_circuit. Hamming distance accumulated bit by bit: X-conjugation with the received bit computes c XOR y, and a controlled increment adds its weight. The affine log-likelihood relation and argmin are classical facts motivating the minimum search, not circuit elements.
- `eq_4`: implemented; _metric_circuit (U_d), composed and inverted in build_circuit. The reversible metric computation U_d|x>|0> = |x>|d(x)> (second form) is implemented; the paper's unspecified phase function phi is not implemented.
- `eq_5`: implemented; build_circuit loop: compose(u_d) -> _threshold_phase -> compose(u_d_inv); _threshold_phase implements C_{<T}. Threshold oracle applies -1 to every path with d(x) < T; comparator realised by enumerating metric values below T with multi-controlled Z gates and uncomputing U_d.
- `eq_6`: implemented; _diffusion and the iteration loop in build_circuit. Grover iterate G_T = (2|psi_0><psi_0| - I) O_T repeated `iterations` times; the success-probability formula is analysis only and is not part of the circuit.

## Specification changes

- eq_5: The flag/phase-kickback ancilla prepared in |-> has been removed; the comparator phase C_{<T} is applied directly on the metric register as multi-controlled Z gates (one per metric value v < T). Reason: Avoids requiring the runner to prepare a non-|0> ancilla and reduces qubit count; the resulting unitary on path+metric is identical to the kickback construction.
- eq_1: H^{⊗N} path-superposition preparation is included as part of the returned operation (toggle `prepare_superposition`, default true) rather than as an externally prepared input state. Reason: Equation eq_1 is the first step of the QVA algorithm and the Grover reflection assumes this basis; with the toggle the runner can also supply its own superposed input.
- eq_3, eq_6: Only a single threshold T and a fixed number of Grover iterations are compiled; the Durr-Hoyer outer loop (measure, classically compute d(x'), update T, repeat) is not included. Reason: The module must return a measurement-free unitary operation; the adaptive loop is classical post-processing left to the runner.
- eq_4: The paper's phase function phi(P(y|x)) is not implemented; only the reversible computed-metric substitute U_d is realised. Reason: phi and the specialised amplitude amplification procedure are not described in the abstract.
- eq_2: Code fixed to the rate-1/2, memory-1 generators (1, 1+D) with zero initial state; general Q, fanout and HMM transition structure are out of scope. Reason: Scope narrowing chosen in the math stage; the general butterfly-structured legal-path preparation is not reconstructed.
