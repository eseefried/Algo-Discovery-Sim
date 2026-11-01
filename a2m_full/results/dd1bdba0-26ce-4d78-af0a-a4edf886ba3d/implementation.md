# Equation to Qiskit

Gate-level emulation of the Bose-Hubbard quantum-walk universal gate set on n qubits, one qubit per dual-rail walker. The instance supplies an ordered list of Rx(theta), Rz(theta), CP(phi) and SWAP operations. The lattice Hamiltonian, measurement, and Steane encoder are not implemented. The circuit is unitary, measurement-free, and uses no ancillas.

Source equation run: `6a9393c5-7906-4d73-943e-2ee265d051ca`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[i] = qubit index i (Qiskit little-endian, index 0 least significant) = logical qubit i, encoding the walker position on a two-site pair: |0> left site, |1> right site
- No ancilla qubits; total qubits = n, capped at 12
- No classical register; no measurements

## Assumptions

- Instance format: {'n': int 1..12, 'ops': [{'gate': 'rx'|'rz', 'qubits': [i], 'theta': float} | {'gate': 'cp', 'qubits': [i, j], 'phi': float} | {'gate': 'swap', 'qubits': [i, j]}]}, applied in list order.
- Angles are in radians and must be finite; a CP angle is effectively defined mod 2*pi.
- Operation count is capped at 2000.
- Idealised exact evolution with freely tunable angles; no loss or errors.
- The cp gate is symmetric in its two qubits.

## Unresolved issues

- The sign convention for phi relative to Ut/hbar is unresolved, so phi is passed directly.
- The paper's Steane-code logical encoding and the lattice construction are not reconstructed.
- No public validation contract was supplied, so the expected output format and angle values are unknown.

## Equation mapping

- `eq_1`: implemented; build_circuit, branch gate == 'rz' (qc.rz). Qiskit rz(theta) equals exp(-i theta Z/2) = diag(e^{-i theta/2}, e^{i theta/2}), matching eq_1 exactly.
- `eq_2`: implemented; build_circuit, branch gate == 'rx' (qc.rx). Qiskit rx(theta) equals exp(-i theta X/2), matching eq_2 exactly.
- `eq_3`: implemented; build_circuit, branch gate == 'cp' (qc.cp). cp(phi) applies diag(1,1,1,e^{i phi}) on the two chosen qubits. phi is supplied directly as an angle.
- `eq_4`: implemented; build_circuit, branch gate == 'swap' (qc.swap). Standard SWAP on two distinct qubits, with Qiskit's native swap gate rather than three explicit CX gates.
- `eq_5`: out_of_scope; no code location. Z-basis readout probabilities describe measurement, which the operation-only module excludes. The runner prepares inputs and performs any sampling or statevector analysis.

## Specification changes

- eq_3: The circuit takes phi as a direct input angle rather than computing it from U, t, and hbar. Reason: The specification gives phi = -Ut/hbar in eq_3 but phi = Ut/hbar in the symbol table, so the sign is inconsistent. Taking phi directly avoids the ambiguity, and the sign is only a convention.
- eq_1, eq_2, eq_3, eq_4: Scope narrowed to a gate-level n-qubit circuit driven by an instance-specified operation list. No Bose-Hubbard dynamics or graph structure is simulated, and the dual-rail encoding is idealised as one qubit per logical qubit. Reason: The graph layout, Hamiltonian parameters, and the paper's gate constructions are not available in the specification.
- eq_5: Measurement and X-basis readout are omitted. The Steane-code encoder extension is not implemented. Reason: The task requires a measurement-free unitary operation. The Steane encoding details are unresolved in the specification.
