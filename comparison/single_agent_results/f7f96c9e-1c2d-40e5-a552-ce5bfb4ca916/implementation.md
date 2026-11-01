# Equation to Qiskit

Qiskit operation for the QFT-domain controlled weighted sum (Draper phase adder with classical integer weights, controlled on single-qubit inputs). It maps |x_1..x_m>|a> to |x>|(a + sum_j w_j x_j) mod 2^n> using QFTGate on the accumulator, controlled-phase gates from each input qubit to each accumulator qubit, then the inverse QFTGate. Example instance: n=3, weights=(1,2).

Source equation run: `54859f3b-096b-4f7b-8ddb-9f3f184609bf`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: inp[0] = x_1 (control, weight w_1), computational basis bit
- qubit 1: inp[1] = x_2 (control, weight w_2)
- qubit 2: acc[0] = accumulator least significant bit (spec qubit l=3)
- qubit 3: acc[1] = accumulator middle bit (spec qubit l=2)
- qubit 4: acc[2] = accumulator most significant bit (spec qubit l=1)
- accumulator integer a = sum_t a_t 2^t with a_t on qubit m+t (Qiskit little-endian); general layout: m input qubits first, then n accumulator qubits

## Assumptions

- Inputs are single-qubit bits and weights are classical integers, as in the specification.
- Arithmetic is modular 2^n with no overflow qubit and no signed handling beyond reduction of negative weights modulo 2^n.
- The QFT is exact, with no approximate-QFT truncation.
- Input qubits come first in the register order, then the accumulator.
- Total qubits n + len(weights) must be at most 12.

## Unresolved issues

- The paper's exact circuit arrangement is not known; this is the standard Draper-style controlled adder reconstruction.
- Non-modular, signed-integer, multiplier and weighted-average constructions are not implemented.
- Multi-qubit quantum inputs (both inner-product vectors quantum) are not supported.

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.append(QFTGate(n), acc_idx) and QFTGate(n).inverse(). QFT of the accumulator is done with QFTGate, whose convention |j> -> 2^(-n/2) sum_k exp(2 pi i jk/2^n)|k> is the left-hand form of eq_1. The factorised form is only used to derive the per-qubit phase angles.
- `eq_2`: implemented; build_circuit: loop over t computing angle = 2*pi*wm/2^(n-t) applied via qc.cp. Phi(c) is applied as a product of phase rotations, here controlled by input qubit j. Spec qubit l maps to Qiskit accumulator bit t = n-l, so R_l angle 2*pi*c/2^l becomes 2*pi*c/2^(n-t).
- `eq_3`: implemented; build_circuit: outer loop over j inputs with qc.cp(angle, j, m+t). Each input qubit x_j controls Phi(w_j) on the accumulator in the Fourier domain. The blocks are diagonal and commute, so the accumulator receives a_0 + sum_j w_j x_j mod 2^n. The surrounding QFT and inverse QFT are included in the operation.
- `eq_4`: background; no code location. Inner-product interpretation and the numeric check instance (n=3, w=(1,2), x=(1,1) -> 3). The circuit supports it as an input to the generic operation, but the module contains no state preparation or expected result. The example instance only fixes n and the weights.
- `eq_5`: out_of_scope; no code location. The weighted-average variant (phase rescaling by 1/W, exact only when W divides S) is a speculative reconstruction and is excluded from the single scoped construction.

## Specification changes

- eq_1, eq_2, eq_3: Qubit ordering: the spec's big-endian accumulator (qubit l=1 is the MSB, angle 2*pi*c/2^l) is mapped to the Qiskit little-endian accumulator, with accumulator bit t carrying angle 2*pi*c/2^(n-t) on qubit m+t. QFTGate acts on the accumulator indices in ascending order, with no extra swaps. Reason: QFTGate includes bit-reversal swaps and uses Qiskit's little-endian convention, so the physical phase on bit t must be 2*pi*c*2^t/2^n, which is the spec's R_l with l=n-t. Copying the factorised-form index order directly would be wrong.
- eq_3: The returned operation includes the QFT and inverse QFT on the accumulator, so it maps computational-basis |x>|a> to |x>|a+S mod 2^n> rather than only applying the Fourier-domain phase block. Reason: The runner prepares inputs and the operation must be a self-contained unitary acting on computational basis states. The spec's X-gate preparation of x and the |0> initial state are left to the runner, so the accumulator can start at any a_0, not only 0.
- eq_2, eq_3: Weights are accepted as any integers (including negative) and reduced modulo 2^n. Rotations whose angle is a multiple of 2*pi are omitted. Reason: Arithmetic is modular, so this does not change the unitary. It generalises the spec's example weights, all of which still lie in the supported range, and reduces gate count.
- eq_4: The instance is parametrised by n and weights, with the number of single-qubit inputs equal to len(weights), instead of being fixed at n=3, m=2. Reason: The task requires the operation to work for varying valid parameters.
- eq_5: The weighted-average variant is omitted. Reason: It is only an inferred construction that is exact only under divisibility. The scope is narrowed to the modular controlled weighted sum.
