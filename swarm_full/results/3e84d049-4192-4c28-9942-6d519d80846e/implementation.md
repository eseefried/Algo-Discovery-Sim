# Equation to Qiskit

Textbook quantum order-finding (QOFA) operation for small N: Hadamards on a t-qubit control register, controlled multiplications by a^(2^k) mod N on an n-qubit target register, then inverse QFT on the control register. Each controlled modular multiplication is built from CX and multi-controlled X gates that realize the basis permutation x -> m*x mod N (identity for x >= N). There is no dense unitary, no state preparation and no measurement. The runner should prepare the target in |1>. Classical postprocessing (continued fractions, gcd factor extraction) and the odd-order techniques are out of scope.

Source equation run: `981fe678-71f8-4abd-b0a4-c086a89d0a39`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..t-1: control/phase-estimation register, little-endian (qubit k controls multiplication by a^(2^k) mod N); inverse QFT acts on these qubits
- qubits t..t+n-1: target/work register holding x in binary, little-endian, n=ceil(log2 N); runner should prepare |1> (x=1)
- example (N=15, a=7, t=6): control qubits 0-5, target qubits 6-9, 10 qubits total

## Assumptions

- Control register size t defaults to min(2n, 12-n) when not supplied.
- Target register size n = ceil(log2 N).
- Target register is initialized to |1> by the runner; the control register starts in |0...0>.
- Controlled multiplier for control qubit k is a^(2^k) mod N, computed classically at build time.
- Total qubits t+n are capped at 12, so N up to 2047 is accepted by the parser but only small N are practical.

## Unresolved issues

- Odd-order techniques and square-coprime handling from the paper are unspecified in the abstract and not implemented.
- Postprocessing (continued fractions, gcd) is left to the runner.
- Multi-controlled X decomposition may produce deep circuits for larger N.

## Equation mapping

- `eq_1`: implemented; _controlled_modmul / build_circuit: controlled multiplications by a^(2^k) mod N. The periodic function x -> a^x mod N, whose period is the order r, is encoded by controlled modular multiplications; the order itself is not computed in the circuit.
- `eq_2`: implemented; build_circuit: validation 'gcd(a,N)=1' raising ValueError. Coprimality is enforced so each multiplier is invertible mod N and the map is a valid permutation (unitary).
- `eq_3`: out_of_scope; no code location. Classical gcd postprocessing from an even order; not part of the quantum operation.
- `eq_4`: out_of_scope; no code location. Classical gcd postprocessing from an even order; not part of the quantum operation.

## Specification changes

- eq_1, eq_2: Scope narrowed to the generic textbook QOFA circuit (Hadamards, controlled modular multiplications, inverse QFT) for small N. Measurement, continued fractions and order extraction are omitted. Reason: The abstract gives no circuit details and the task requires a measurement-free unitary operation; the circuit skeleton is an assumption from the spec.
- eq_3, eq_4: Factor-extraction equations and the paper's odd-order / square-coprime techniques are not implemented. Reason: They are classical postprocessing, and the abstract does not specify the odd-order techniques.
- eq_1: Modular multiplication is built as an explicit permutation (cycle decomposition into transpositions via CX and multi-controlled X), acting as identity on x >= N. The Hadamard layer is included in the operation, and the control register is little-endian with inverse QFT via QFTGate(t).inverse() on qubits 0..t-1. Reason: Avoids opaque dense unitaries and follows the Qiskit convention; the target must be prepared in |1> by the runner.
