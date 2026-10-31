# Equation to Qiskit

Implements the single scoped construction U = C_f (H^{⊗m} ⊗ I^{⊗(n-m)}) that maps the computational basis |a⟩|b⟩ to the 2^m-term Bell-like orthonormal basis |B_{a,b}⟩. The control register receives a Hadamard layer; a generic multi-qubit controlled-XOR gate C_f, specified by a truth table, XORs f(k) into the target register using X-conjugated multi-controlled-X gates. The example is the tiny instance n=3, m=2, f(k)=k_1 XOR k_2 from eq_6. The paper's two specific controlled-unitary gates, the entanglement/monogamy analysis and the qudit extension are out of scope.

Source equation run: `211f646a-7631-4b5a-a558-b69d986377e9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit 0: target register, target qubit 1 of the spec (n-m=1 target qubit); receives b XOR f(k)
- Qiskit qubit 1: control register, control qubit 2 of the spec (bit 0 of k, i.e. k_2)
- Qiskit qubit 2: control register, control qubit 1 of the spec (bit 1 of k, i.e. k_1, most significant)
- Basis-state integer = big-endian reading of the spec label string 'ab' = a*2^(n-m) + b; e.g. input |000> -> (|000>+|011>+|101>+|110>)/2, input integer 5 (a=10,b=1) -> (|001>+|010>-|100>-|111>)/2 (eq_6)
- f_table[k] indexed by k = integer of the control register (control qubit 1 as MSB); f_table[k] bit t targets Qiskit qubit t

## Assumptions

- No validation contract or requested instance was supplied; the example instance is the tiny instance of eq_6.
- C_f is a placeholder permutation unitary and is not claimed to reproduce the paper's gates or their entanglement properties.
- The circuit returned is the operation U only; the runner prepares the computational-basis input |a>|b> that selects the basis element.
- Gate count of C_f scales as O(2^m (n-m)) multi-controlled-X gates, acceptable within the 12-qubit cap.

## Unresolved issues

- The actual working principles of the paper's two controlled-unitary gates, and hence which entangled bases they produce, remain unknown.
- Whether the paper's gates are permutation (XOR-type) unitaries or involve other phase structures cannot be determined from the abstract.

## Equation mapping

- `eq_1`: background; no code location. Property of the output state (2^m distinct terms, amplitudes ±1/sqrt(2^m)); it follows from eq_3 and eq_4 by linearity and is not a separately coded operation.
- `eq_2`: background; no code location. Orthonormality follows from unitarity of the generated circuit acting on orthonormal computational inputs; no separate code.
- `eq_3`: implemented; _apply_hadamard_layer. Hadamard on each control qubit (Qiskit indices n-m..n-1).
- `eq_4`: implemented; _apply_controlled_xor (C_f) and build_circuit (composition U). C_f realised as X-conjugated multi-controlled-X gates for every control string k and every set bit of f(k); build_circuit composes it after the Hadamard layer.
- `eq_5`: implemented; build_circuit. The returned circuit is exactly U; applying it to |a>|b> yields |B_{a,b}>. Input preparation is left to the runner.
- `eq_6`: implemented; example_instance_json / build_circuit with f_table=[0,1,1,0]. The example instance n=3, m=2, f(k)=k_1 XOR k_2 reproduces the two listed states for inputs |000> and |101>.

## Specification changes

- eq_5, eq_6: Qubit ordering mapped to Qiskit little-endian: the target register occupies Qiskit qubits 0..n-m-1 and the control register occupies n-m..n-1, with spec qubit 1 of each register at the highest index of that register. Reason: The spec writes kets big-endian with control qubit 1 leftmost; this layout makes the Qiskit basis-state integer equal to the spec's big-endian reading of the label 'ab'.
- eq_4: The Boolean map f is supplied as an explicit truth table (f_table) or the keyword 'parity'; constant f is rejected with ValueError. Reason: A concrete interface is needed for arbitrary f; the spec's eq_4 assumption states f must be non-constant for the output basis to be entangled, so constant maps are treated as invalid instances.
- eq_4, eq_5: Scope narrowed to the agent-chosen generic controlled-XOR construction; the paper's two specific multi-qubit controlled-unitary gates are not implemented. Reason: Their definitions are not available in the abstract (listed under missing_information).
