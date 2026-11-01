# Equation to Qiskit

Weighted-sum accumulator operation |x_1>...|x_k>|a> -> |x_1>...|x_k>|a + sum_j w_j x_j mod 2^m>. It applies QFTGate to the accumulator, then controlled-phase gates from each input bit to each accumulator qubit with classical integer weights, then the inverse QFTGate. Unsigned inputs are the default; two's-complement inputs are optional. No state preparation, measurement or classical averaging is included.

Source equation run: `9bbb128d-02c9-4280-a13f-e0881f2bfe8e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Example (n=2, k=2, weights [1,2], default m=4): 8 qubits.
- qubits 0-1: x_1 (qubit 0 = LSB)
- qubits 2-3: x_2 (qubit 2 = LSB)
- qubits 4-7: accumulator A (qubit 4 = LSB), computational-basis little-endian encoding of a; output is a + w_1 x_1 + w_2 x_2 mod 2^m
- general: input j bit i at index j*n+i; accumulator bit l at index k*n+l

## Assumptions

- Inputs are prepared externally; the accumulator is expected in a computational-basis state, typically |0>.
- Weights are integers with |w| <= 4096; n in 1..10; at most 12 input registers; total qubits <= 12.
- Unsigned inputs unless signed_inputs is true (two's complement).
- Default m is the smallest value avoiding overflow over the full input range; an explicit m gives modular arithmetic.

## Unresolved issues

- The paper's exact circuit layouts, gate counts and fixed-point weighted-average scheme are not reconstructed.
- The controlled weighted sum and quantum-quantum inner product variants are not implemented.

## Equation mapping

- `eq_1`: background; build_circuit: qc.append(QFTGate(m), acc_idx). The Fourier-basis product form is the background for the phase addition. QFTGate includes swaps, so the per-qubit phase index differs from the no-swap form (see specification_changes).
- `eq_2`: implemented; build_circuit: qc.cp(...) loop over j, i, l. Controlled phases from each input bit onto each accumulator qubit perform Draper addition mod 2^m. The angles use the swap-corrected index for QFTGate.
- `eq_3`: implemented; build_circuit: coef = weights[j] * 2**i; val = (coef * 2**l) % mod. Classical integer weight multiplies each angle; negative weights subtract. Angles are reduced mod 2*pi exactly via integer arithmetic. Optional two's-complement signed inputs give the MSB weight -2^(n-1).
- `eq_4`: out_of_scope; no code location. The quantum-quantum inner product with doubly controlled phases is not implemented; weights are classical.
- `eq_5`: implemented; build_circuit: qc.append(QFTGate(m).inverse(), acc_idx). The inverse QFT returns the accumulator to the computational basis. Measurement and the classical division for the weighted average are not part of the operation and are not implemented.

## Specification changes

- eq_1, eq_2, eq_3: Accumulator qubit l receives phase 2*pi*v*2^l/2^m (angle 2*pi*(w*2^(i+l) mod 2^m)/2^m) instead of 2*pi*v/2^(l+1). Reason: QFTGate includes bit-reversal swaps, so in the output of QFTGate(m) qubit l carries phase exp(2*pi*i*a/2^(m-l)). The no-swap angle index 2^(l+1) would be wrong for it.
- eq_2, eq_5: The QFT and inverse QFT are done with QFTGate (with swaps) inside the operation, rather than the no-swap QFT. Reason: This follows the required API; the swap-corrected angles give the same overall map a -> a + S mod 2^m.
- eq_3, eq_5: Scope narrowed to classical integer weights on basis-state or superposed input registers. Accumulator size m is validated and defaults to the no-overflow size, and the circuit is modular mod 2^m if m is given smaller. The spec's non-negative weights are extended to any integers. Reason: Smallest well-defined construction; negative weights follow directly from phase additivity.
- eq_5: The operation excludes measurement and classical averaging S/sum(w). Reason: The task requires a measurement-free unitary operation.
- eq_4: The doubly controlled inner-product variant is omitted. Reason: Marked out of scope for the smallest instance.
