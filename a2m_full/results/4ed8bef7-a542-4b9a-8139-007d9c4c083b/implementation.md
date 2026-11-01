# Equation to Qiskit

Grover search over all 2^N input-bit paths of a small binary rate-1/n convolutional-code trellis (example: Q=3, generators (7,5) octal, N=3, hard-decision Hamming metric, start state 0, no tail). Optional H layer builds the uniform path superposition. Each of R iterations is a threshold phase oracle (M<T) followed by diffusion on the path register. The oracle computes the Hamming metric into a work register, applies a phase to every metric value below T, then uncomputes the metric. No flag qubit is used and no measurements are made.

Source equation run: `c4baa7fa-280c-49ec-aa6e-c992bb1aba61`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..N-1: path register, qubit t-1 = input/branch bit b_t (little-endian, qubit 0 = b_1)
- qubits N..N+n-1: err work register (n = number of generators), reused per step and returned to |0>
- qubits N+n..N+n+m-1: metric work register, m=bit_length(n*N), little-endian Hamming-distance counter, returned to |0>
- example: N=3, n=2, m=3 -> path 0-2, err 3-4, metric 5-7 (8 qubits)
- received integer r_t: bit j is the received bit for generator j; generator tap k=0 (current bit) is the MSB of the generator value

## Assumptions

- f=2, binary rate-1/n feedforward code, hard-decision Hamming metric, start state 0, no tail termination
- Generator integers use MSB = tap on the current input bit; instance fields are N, Q, generators, received, threshold (1..nN+1), iterations, prepare_uniform
- Work registers (err, metric) start in |0> and are returned to |0>
- The example received word 3,1,0 is the encoding of input bits 1,0,1 with generators (7,5), so M=0 for that path; T=1 gives K=1 and R=2 is near-optimal for 8 paths

## Unresolved issues

- The paper's actual phase function of path probability and its specialized amplitude amplification are not reproduced
- K is not computed in the circuit; the caller must choose R
- Whether the runner expects the uniform-superposition layer inside the operation is uncertain, hence the prepare_uniform switch

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.h(path) when prepare_uniform is true. Hadamards on the path register give the uniform superposition over all 2^N branch sequences (f=2).
- `eq_2`: implemented; _metric_circuit. The branch outputs are the parity of the shift-register taps, computed with CNOTs from the path bits. They are XORed with the hardwired received bits and the mismatch weight is accumulated into the metric register by controlled increments. The state register is not stored explicitly.
- `eq_3`: implemented; build_circuit oracle block: compose(comp), per-value _mcz loop, compose(comp_inv). Metric computation, a -1 phase on every metric value v<T via multi-controlled Z, then metric uncomputation. The phase is applied directly, so no flag ancilla in |-> is needed.
- `eq_4`: implemented; build_circuit: diffusion block (h, x, _mcz, x, h on path). Standard Grover diffusion 2|psi0><psi0|-I on the path register, up to global phase.
- `eq_5`: background; build_circuit: for _ in range(R) loop. The count and success formula are classical analysis. Only the iteration count R is taken as an input parameter and repeated.

## Specification changes

- eq_2: The trellis state register is not materialized. The code outputs are computed directly as XOR parities of the current and previous Q-1 path bits, with bits before step 1 treated as 0. Reason: With s_0=0 the shift-register state is exactly the last Q-1 input bits, so this is equivalent and saves qubits under the 12-qubit cap.
- eq_3: The flag ancilla in |-> is replaced by a direct phase (multi-controlled Z) on each metric value below T. The err register is reused per step and uncomputed. Reason: This avoids input-state preparation of an ancilla and saves a qubit, with the same phase action on the path register.
- eq_1, eq_4, eq_5: Scope narrowed to one threshold-marking Grover operation with fixed T and R. The paper's specialized amplitude amplification, butterfly/FFT efficiency structure, soft-decision metrics and the outer Durr-Hoyer loop are omitted. Reason: The abstract does not specify these procedures.
- eq_1: The uniform H layer is included in the circuit by default and can be disabled with prepare_uniform=false. Reason: The Grover circuit needs the uniform superposition from |0...0>, and the spec lists this preparation as step 1.
