# Equation to Qiskit

Qiskit phase-estimation operation for Shor order finding: H on t control qubits, controlled multiplication by a^(2^j) mod N on the work register (synthesized as cycles of basis-state transpositions using multi-controlled X gates), then inverse QFTGate on the control register. Input state (work=|1>, control=|0>) and measurement are left to the runner. Classical post-processing is not part of the circuit.

Source equation run: `deb7193d-b487-4a93-95b3-9ae792363a60`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..t-1: control register, little-endian (qubit j has weight 2^j in y); controls controlled-U^(2^j)
- qubits t..t+n-1: work register, n=ceil(log2 N), little-endian; work bit 0 is qubit t; runner should prepare |1> (qubit t set to 1)
- example N=21,a=4,t=6: control qubits 0-5, work qubits 6-10 (11 qubits total)
- control output after inverse QFT encodes y with y/2^t ≈ s/r

## Assumptions

- N>=3, 1<a<N, gcd(a,N)=1; n=ceil(log2 N) work qubits and t+n<=12.
- The runner prepares the work register in |1> (qubit t = 1) and the controls in |0>.
- Controlled U^(2^j) uses multiplier a^(2^j) mod N, skipped when it equals 1.
- N need not be the product of two primes for the circuit itself.

## Unresolved issues

- Gate count grows with the number of cycles and may be large for larger N (still within the 12-qubit cap).
- The paper's two-run relation-combining technique is not reconstructed.

## Equation mapping

- `eq_1`: background; _controlled_mult / build_circuit: multiplier pow(a, 2**j, N). Order definition is the property the circuit's eigenphases encode; r is not computed in the circuit, and the code only requires gcd(a,N)=1.
- `eq_2`: out_of_scope; no code location. Classical gcd post-processing of even orders; not part of the circuit operation.
- `eq_3`: implemented; build_circuit: H layer, controlled-U^(2^j) loop via _controlled_mult, QFTGate(t).inverse() on control qubits. Phase-estimation circuit whose measured control outcome has distribution P(y). Measurement and continued fractions are left to the runner and post-processing.
- `eq_4`: out_of_scope; no code location. Classical odd-order gcd rule for square a using b^r; no quantum content.
- `eq_5`: out_of_scope; no code location. Classical relation between orders of a and sqrt(a); the paper's procedure is not specified.
- `eq_6`: out_of_scope; no code location. Classical square-root-of-unity gcd check.

## Specification changes

- eq_3: The circuit contains only the phase-estimation operation (H on controls, controlled modular multiplications, inverse QFT). Work-register |1> preparation, measurement, and continued fractions are excluded. Reason: Task requires an operation without state prep or measurement; the runner prepares inputs.
- eq_3: The U_a black box is synthesized with standard gates: the permutation x -> m x mod N is split into cycles, then transpositions realized by CX conjugation and a multi-controlled X, instead of an opaque oracle. It acts as the identity on x >= N. Reason: Opaque dense unitaries are forbidden; this keeps the construction explicit and unitary.
- eq_3: Control-register size t defaults to min(2n, 12-n) and is user-selectable, so for N=21 it is at most 7 rather than about 2n. Reason: 12-qubit cap.
- eq_3: The inverse QFT is QFTGate(t).inverse() on qubits 0..t-1, with no manual index reordering. Reason: Little-endian control encoding y=sum c_i 2^i makes QFTGate's bit-reversal convention match directly; no factorized-QFT index conflict arises.
- eq_1, eq_2, eq_4, eq_5, eq_6: Scope is narrowed to the quantum order-finding circuit for any valid (N,a,t); odd-order/square-coprime classical rules and relation combining are not implemented. Reason: They are classical post-processing and the paper's exact technique is not given.
