# Equation to Qiskit

Qiskit circuit for a QFT-domain weighted sum (inner product of classical integer weights w with a quantum data vector x) accumulated modulo 2^n. It applies QFTGate to the accumulator, then controlled-phase rotations from each bit of each x_j onto each accumulator qubit, then the inverse QFTGate. The result is acc -> (acc + sum_j w_j x_j) mod 2^n. The inputs are left unchanged.

Source equation run: `90f6ebb1-0699-4a99-ab7a-c903818f4fc2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0..q2: acc (accumulator, little-endian, q0 least significant; holds b and ends as (b + S) mod 8)
- q3..q4: x0 (2-bit input, q3 least significant)
- q5..q6: x1 (2-bit input, q5 least significant)

## Assumptions

- Inputs x_j are unsigned integers held in computational-basis registers (little-endian).
- The accumulator holds an integer b in the computational basis on entry, prepared by the runner.
- Weights are classical integers. Exact (non-wrapping) results need n_acc large enough that the sum stays below 2^n_acc.
- Total qubits are n_acc + sum(input_bits), capped at 12.

## Unresolved issues

- The paper's specific adder and multiplier variants, including controlled and signed ones, are not reconstructed from the abstract.
- The transform-domain weighted-average method is not implemented.
- Quantum-valued weights, that is products of two quantum registers, are not implemented.

## Equation mapping

- `eq_1`: background; build_circuit: QFTGate(n) appended on acc qubits. The QFT definition is supplied by Qiskit's QFTGate, whose convention matches eq_1, including bit reversal. It is not re-implemented.
- `eq_2`: implemented; build_circuit: controlled-phase loop (qc.cp). Addition in the Fourier domain by phase rotations, with angle 2*pi*coeff/N on acc qubit t. Each rotation is controlled by an input bit, so the added amount is the data-dependent value w_j*2^l.
- `eq_3`: implemented; build_circuit: QFTGate, phase block, QFTGate.inverse() on acc. Full pipeline QFT -> phase addition -> inverse QFT, giving (b + S) mod N in the computational basis.
- `eq_4`: implemented; build_circuit: nested loops over j, l, t. For every input j and bit l, controlled phases of 2*pi*w_j*2^(l+t)/N on acc qubit t give the total phase exp(2*pi*i*k*S/N) with S = sum_j w_j x_j. The result is the inner product modulo N.

## Specification changes

- eq_4: Weights are classical integers fixed in the instance. Quantum-register weights are not implemented. Reason: The specification left open whether weights are classical or quantum. Classical weights are the smallest well-defined construction.
- eq_2, eq_4: The accumulator is not restricted to start in |0>. The circuit adds S to whatever computational-basis value b it holds, and the example is not tied to b=0. Reason: The operation must act on runner-prepared inputs. For b=0 it reduces to eq_4.
- eq_4: Bit order is little-endian (qubit 0 least significant) for both the accumulator and the x registers, instead of the big-endian assumption in the initial-state description. Reason: This matches Qiskit and QFTGate conventions. Because QFTGate includes bit reversal, the rotation on acc qubit t is 2*pi*S*2^t/N.
- eq_2, eq_4: Rotation coefficients are reduced mod N, so weights may be negative (two's-complement style mod N), and zero rotations are skipped. Reason: Phases are periodic, which makes modular arithmetic exact and the circuit smaller.
- eq_2, eq_3, eq_4: Scope is narrowed to the modular weighted-sum accumulator. Signed-integer interpretation, extra carry-qubit non-modular variants, a global control qubit, and weighted-average division are not implemented. Reason: The abstract gives no details of those variants, so they cannot be reconstructed reliably.
