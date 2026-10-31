# Equation to Qiskit

Builds a Draper QFT adder for a classical constant a on an n-qubit register: QFTGate, then per-qubit phase gates implementing exp(2*pi*i*a*k/2^n), then the inverse QFTGate. This maps |x> to |x+a mod 2^n>. An optional control qubit turns the phase gates into controlled-phase gates, giving a controlled constant adder. The weighted-average and inner-product constructions are not implemented.

Source equation run: `08d85f16-46e9-4f63-9452-9f7c67d15bd6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data register x, little-endian (qubit 0 is the least significant bit), integer x = sum_q x_q 2^q
- qubit n (present only when controlled=true): control qubit; the addition is applied only when it is |1>

## Assumptions

- N = 2^n
- The addend is a classical constant, not a quantum register
- The control qubit, when used, is placed at index n, and the runner prepares the inputs (x on the data register, control state)
- The Fourier-domain phase uses the integer index k with qubit q weighted 2^q, which holds because QFTGate includes the swaps

## Unresolved issues

- Weighted-average and inner-product circuits are not implemented
- Multipliers, signed-integer encodings and non-modular arithmetic are not implemented
- Adding a quantum-register addend (a controlled weighted sum) would need a specification that is not available

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.append(QFTGate(n), targets). The QFT on the data register uses QFTGate, which matches the stated basis-state action including bit reversal.
- `eq_2`: implemented; build_circuit: phase loop (qc.p / qc.cp) between QFTGate(n) and QFTGate(n).inverse(). The Fourier-domain phase exp(2*pi*i*a*k/N) is factorized into single-qubit phases of angle 2*pi*a*2^q/N, followed by the inverse QFT, giving addition of a mod N.
- `eq_3`: out_of_scope; no code location. The classical weighted-average formula is not implemented, because the abstract does not specify its quantum circuit.
- `eq_4`: out_of_scope; no code location. The inner-product formula is not implemented. A controlled weighted sum needs a multi-register encoding that the abstract does not specify.

## Specification changes

- eq_3, eq_4: Scope narrowed to the QFT constant adder (eq_1, eq_2), with an optional control qubit. The weighted-average and inner-product circuits are not built. Reason: The abstract and specification give no circuit constructions or encodings for these, so any implementation would be invented.
- eq_2: The addend a is a classical parameter restricted to 0 <= a < 2^n. Only modular (mod 2^n) unsigned addition is implemented. The optional control qubit makes the addition a controlled constant adder. Reason: The signed-integer and non-modular variants are not specified. The control qubit follows the specification's assumed ctrl register.
