# Equation to Qiskit

Qiskit module implementing the unitary part of one quantum order finding (QOFA) run for Shor's algorithm: Hadamards on a t-qubit control register, controlled modular multiplications by a^(2^j) mod N built from CNOT/multi-controlled-X transposition circuits (no dense unitaries), and the inverse QFT on the control register. Example instance is the square-coprime odd-order case N = 21, a = 4 = 2^2 (r = 3), with t = 7 control qubits so that the total is 12 qubits. Measurement, continued fractions, and the classical gcd post-processing (even-order and odd-order square-coprime rules) are outside the circuit.

Source equation run: `93f24fa4-b4ef-4d8e-8286-de4e30a7f1e0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-6: control (phase) register 'ctrl', t = 7 qubits, little-endian; qubit j controls U_{4^(2^j) mod 21}; after the inverse QFT the register holds m with qubit 0 the least significant bit, peaks expected near m ≈ 128*s/3 ∈ {0, 42.67, 85.33}
- qubits 7-11: work register 'work', n = 5 qubits, integer y mod 21 in binary with qubit 7 the least significant bit; expected input |1> (qubit 7 set), untouched for basis states y >= 21
- total 12 qubits; runner prepares |0>^7 ⊗ |00001> (work register integer 1)

## Assumptions

- Runner prepares the input state |0>^t on qubits 0..t-1 and the integer 1 (qubit t set, others zero) on the work register.
- Little-endian encoding in both registers: qubit j of the control register is bit j of x and of m; qubit t+j is bit j of the work integer.
- QFTGate(t).inverse() applied to control indices [0..t-1] maps sum_x e^{2 pi i x s/r}|x> to peaks at m ≈ 2^t s/r in the same little-endian convention.
- Instance keys: integers N >= 3, 1 < a < N with gcd(a,N) = 1, t >= 1 with t + ceil(log2 N) <= 12; optional integer b with b^2 ≡ a (mod N); optional boolean include_hadamards (default true).
- Basis states y >= N of the work register are left unchanged by U_c (identity on the unused part of the space).

## Unresolved issues

- With t = 7 for N = 21 the standard precision condition 2^t >= 2N^2 is violated; recovery of r = 3 from the measured m relies on r being small relative to 2^t and must be checked classically via a^{r'} mod N.
- Multi-controlled X gates with up to n controls are left to Qiskit's default synthesis; gate count is not optimized.
- The paper's second technique ('new order finding relations in case of failure') and its quantitative success-probability analysis remain unreconstructed and are not reflected in the circuit.

## Equation mapping

- `eq_1`: background; _validate (gcd(a,N)=1 check). Definition of the order; it is the quantity the circuit's measurement statistics encode, not an operation. Only the coprimality precondition is enforced in code.
- `eq_2`: out_of_scope; no code location. Classical even-order gcd post-processing after measurement; the module returns only the unitary circuit.
- `eq_3`: implemented; _mult_permutation, _cycles_to_transpositions, _controlled_transposition, _controlled_mod_mult. Controlled U_c|y> = |c y mod N> (identity for y >= N) is built exactly as a permutation from CNOT and multi-controlled-X transposition circuits; eigenstate structure is background used only to interpret the output.
- `eq_4`: implemented; build_circuit (Hadamard loop, controlled U_{a^(2^j)} loop, QFTGate(t).inverse() append). The unitary part of phase estimation (superposition, controlled modular exponentiation with control qubit j for power 2^j, inverse QFT on little-endian control qubits 0..t-1) is implemented; measurement and continued fractions are left to the runner. With the 12-qubit cap the condition 2^t >= 2N^2 cannot be met for N = 21.
- `eq_5`: out_of_scope; no code location. Classical odd-order square-coprime gcd rule; only the precondition a = b^2 mod N is validated in _validate when 'b' is supplied.
- `eq_6`: implemented; example_instance_json consumed by build_circuit / _validate. The explicit instance N = 21, b = 2, a = 4 (order r = 3) is the example instance; the circuit realizes its QOFA run with t = 7 instead of t = 10.

## Specification changes

- eq_4, eq_6: Control register reduced from t = 10 to t = 7 qubits for the N = 21 example (total 12 qubits), so 2^t = 128 < 2N^2 = 882; t is an instance parameter with t + ceil(log2 N) <= 12 enforced. Reason: Hard cap of 12 total qubits; 10 + 5 = 15 would exceed it. For r = 3 the outcome peaks near m ≈ 128 s/3 are still well separated and continued fractions with denominator bound N recover r = 3, but the generic uniqueness guarantee of eq_4 is not met.
- eq_4: Measurement of the control register and continued-fraction recovery of r are omitted; the module returns a measurement-free unitary circuit. Reason: Task requires an operation, not an experiment; the runner performs measurement and post-processing.
- eq_2, eq_5: Classical gcd post-processing (even-order rule and odd-order square-coprime rule) is not implemented in code. Reason: It is classical post-processing outside the quantum circuit; only the square-coprime precondition b^2 ≡ a (mod N) is validated when 'b' is given.
- eq_3: Controlled modular multiplication is realized as an exact basis-state permutation decomposed into cycles and transpositions, each transposition using CNOTs plus one multi-controlled X with the control qubit added; no arithmetic adder-based decomposition is used. Reason: The specification left the circuit-level decomposition open and dense/opaque unitaries are disallowed; the permutation construction is exact and generic for any coprime a and small N.
- eq_4: The initial work-register state |1> is not prepared inside the circuit; Hadamards on the control register are included as part of the operation (switchable via 'include_hadamards'). Reason: Inputs are prepared by the runner per task rules; the Hadamard layer is part of the QOFA operation rather than input preparation.
