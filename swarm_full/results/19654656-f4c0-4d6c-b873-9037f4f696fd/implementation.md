# Equation to Qiskit

Builds a Draper-style QFT controlled weighted sum (inner-product accumulator) with classical integer weights. Data registers x_i (n_x qubits each) act as controls, and the accumulator acc (n_acc qubits) goes through QFTGate, then controlled-phase rotations, then the inverse QFT. This maps |x>|s> to |x>|s + sum_i w_i x_i mod 2^n_acc>, which is the weighted sum when acc starts at 0. Multipliers and modular variants are not implemented.

Source equation run: `889816a6-f394-4258-8af0-e5c8d25fe9d1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Example: m=2 inputs, n_x=2, n_acc=4 (8 qubits total)
- Qubits 0-1: x0 (index 0 = LSB of x_0)
- Qubits 2-3: x1 (index 2 = LSB of x_1)
- Qubits 4-7: acc accumulator (index 4 = LSB), computational basis integer encoding on input and output
- General: x_i bit j at index i*n_x + j; acc bit t at index m*n_x + t

## Assumptions

- Weights are classical integers compiled into rotation angles
- Data bits are the controls, and each x_i is n_x bits with index 0 as the LSB
- Unsigned input by default, with optional two's complement input
- Overflow is avoided by choosing n_acc large enough, otherwise the result wraps mod 2^n_acc
- The runner prepares the inputs, including acc=0 when the plain weighted sum is wanted
- Total qubits m*n_x + n_acc are capped at 12

## Unresolved issues

- Exact circuits of the paper's modular, signed, and multiplier variants are unknown
- The weighted-average normalization and any transform-domain readout are not specified in the abstract and are not implemented
- No public validation contract was supplied

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.append(QFTGate(n_acc), acc_qubits) and the inverse QFTGate append. QFTGate matches the stated convention |j> -> 2^(-n/2) sum_k exp(2 pi i j k/2^n)|k>, including bit reversal. It is applied to the accumulator before the phase rotations and inverted afterwards.
- `eq_2`: implemented; build_circuit: the loop of qc.cp(angle, x_i[j], acc[t]) between the QFT and inverse QFT. After QFTGate the acc basis index k = sum_t k_t 2^t, so Phi(a) with phases exp(2 pi i a k/2^n) factorizes into per-qubit phases 2 pi a 2^t/2^n on acc[t]. Each phase is controlled here by a data bit.
- `eq_3`: implemented; build_circuit: the loops over inputs i and bits j with coefficient w_i * 2^j mod 2^n_acc. Summing the controlled phases over all x_i bits j gives phase 2 pi k sum_i w_i x_i / 2^n. The inverse QFT then yields |s + sum_i w_i x_i mod 2^n>, which is the weighted sum for s=0.

## Specification changes

- eq_3: Implemented as an accumulating add, |x>|s> -> |x>|s + sum w_i x_i mod 2^n>. This reduces to the specified map when acc starts in |0>. The circuit itself is a unitary operation and does not prepare |0>. Reason: No state preparation is allowed in the operation, and the Draper adder naturally adds into the existing register value.
- eq_3: Added an optional 'signed' flag. When it is set, the top bit of each x_i has weight -2^(n_x-1), giving two's complement inputs. The default is unsigned. Reason: The abstract mentions signed integers. Two's complement is the assumed encoding, and it is implemented as a sign flip on the top-bit coefficient.
- eq_1, eq_2, eq_3: Scope is narrowed to the non-modular-by-design weighted sum with classical weights. Arithmetic is mod 2^n_acc, and a weighted-average normalization is not implemented. Multipliers and other modular variants are not implemented. The number of inputs m is set by len(weights). Reason: The abstract gives no gate-level details for these variants, so only the weighted-sum instance is reconstructable.
