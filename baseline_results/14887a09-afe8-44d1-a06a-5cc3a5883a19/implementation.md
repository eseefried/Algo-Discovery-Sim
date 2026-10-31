# Equation to Qiskit

Qiskit module implementing the QFT-domain controlled weighted sum (eq_3): an n-qubit accumulator is moved to the Fourier basis with QFTGate(n), each single-qubit input x_j controls a Draper phase-addition block Phi(w_j) built from cp gates with angles 2*pi*w_j*2^k/2^n on accumulator qubit k (eq_2), and QFTGate(n).inverse() returns the accumulator to |(a0 + sum_j w_j x_j) mod 2^n>. Classical integer weights are compiled into the angles; the operation acts on arbitrary input/accumulator basis states supplied by the runner (linearity gives superposition behaviour). The weighted-average rescaling variant (eq_5) is out of scope.

Source equation run: `f35c9dfb-cf30-4e37-8a8f-dcef118867cb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: acc[0] - accumulator least significant bit (weight 2^0)
- qubit 1: acc[1] - accumulator bit of weight 2^1
- qubit 2: acc[2] - accumulator most significant bit (weight 2^2); arithmetic is modulo 2^3 = 8
- qubit 3: inp[0] - input bit x_1, weight w_1 = 1
- qubit 4: inp[1] - input bit x_2, weight w_2 = 2
- Expected action for the example: runner prepares inp = |x_2 x_1> = |11> (qubits 4,3) and acc = |000>; the operation maps acc to |011> (integer 3 = 1*1 + 2*1), inputs unchanged. Bitstring read with qubit 0 as the LSB.

## Assumptions

- Inputs are single qubits (bits) and weights are classical integers compiled into controlled-phase angles.
- Arithmetic is modular (mod 2^n) with no overflow qubit; non-modular and signed-integer variants of the paper are not reconstructed.
- Exact QFT (no truncation of small rotations); all angles are reduced modulo 2*pi exactly via integer arithmetic before conversion to float.
- Qubit cap of 12 total (n + m) enforced before register allocation.
- The example instance (n=3, w=(1,2)) and its expected output (acc |000> with inputs |11> -> acc |011>) are chosen by this reconstruction, not taken from the paper.

## Unresolved issues

- The paper's exact gate arrangement for the controlled weighted sum, and whether both data vectors may be quantum registers, are unknown; a classical-weight version was implemented.
- The construction of the transform-domain weighted average (division by total weight, rounding convention) could not be resolved and is not implemented.
- Multi-bit integer inputs (controlled-Phi(w_j 2^t) per input bit) are a straightforward extension not exposed in the instance format.

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.append(QFTGate(n), acc_idx) and qc.append(QFTGate(n).inverse(), acc_idx) (comments '# eq_1'). QFT and inverse QFT on the accumulator realised with QFTGate under Qiskit's convention; the spec's big-endian factor index l is mapped to Qiskit qubit k = n - l (see module docstring).
- `eq_2`: implemented; _controlled_phase_add (docstring 'eq_2 (controlled)'). Draper constant addition Phi(c) as a tensor product of phase rotations, implemented in controlled form with cp(2*pi*c*2^k/2^n, control, acc[k]); zero-angle rotations are dropped exactly.
- `eq_3`: implemented; build_circuit loop 'for j in range(m)' (comment '# eq_3'). Each input qubit controls its weight's phase-addition block; the product over inputs yields the weighted sum modulo 2^n on the accumulator.
- `eq_4`: background; no code location. Inner-product interpretation and the chosen check instance; it motivates the example_instance_json (n=3, w=(1,2)) but no reference results or test code are included in the module.
- `eq_5`: out_of_scope; no code location. Weighted-average phase rescaling (angles w_j/W) is not implemented; it is only exact when W divides S and its paper construction is unknown.

## Specification changes

- eq_1, eq_2, eq_3: Qubit ordering: the specification indexes Fourier factors big-endian (l = 1 is the MSB with phase 2*pi*a/2^l). The implementation uses Qiskit's little-endian convention (acc[0] = LSB) and QFTGate's definition, under which acc[k] carries phase 2*pi*a*2^k/2^n; the phase-addition angle on acc[k] is therefore 2*pi*w*2^k/2^n (l = n - k). Reason: Required to match QFTGate's documented action and Qiskit's physical qubit order; the mathematical content (modular addition of w_j x_j) is unchanged.
- eq_3, eq_4: The module returns only the operation: no X-gate preparation of x, no initialisation of a_0, no measurement. The input bit values x and a_0 are not instance parameters; the runner supplies the input state. The instance only carries n and the classical weight vector. Reason: Task requires an operation, not an experiment; the operation is valid for all basis (and superposed) inputs by linearity.
- eq_2, eq_3: Weights may be any Python integers, including negative or >= 2^n; they are reduced modulo 2^n, so negative weights act as subtraction mod 2^n. Reason: Follows directly from the 2^n-periodicity of the Fourier phases; it is a harmless generalisation and does not implement the paper's signed-integer handling, which remains out of scope.
- eq_5: Scope narrowed to the controlled weighted sum; the weighted-average variant is excluded. Reason: Its exact construction is unknown and the rescaled version is only exact when W divides S.
