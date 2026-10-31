# Equation to Qiskit

Implements the ideal Toffoli (CCNOT) target unitary of eq_1/eq_2 as a Qiskit operation on a register of 3..12 qubits with user-selected control_1, control_2 and target indices. Two equivalent realisations are offered: a single CCX gate ('single_shot', mirroring the abstract's single-shot gate at the logical level) or the standard H/T/CX decomposition ('decomposed', the sequential baseline the abstract contrasts against). The pulse-level control problem (eq_3-eq_6) cannot be reconstructed from the abstract and is out of scope.

Source equation run: `16a653bb-85a1-464d-9af4-8c9c156bafd5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: t (target), least significant bit of x = 4*c_1 + 2*c_2 + t
- qubit 1: c_2 (second control)
- qubit 2: c_1 (first control), most significant bit of x
- Computational basis label x = sum_k b_k 2^k with Qiskit qubit k holding bit b_k; the gate swaps x=6 (|110>) and x=7 (|111>) and fixes x=0..5
- For num_qubits > 3 the remaining qubits are idle spectators (identity)

## Assumptions

- Register convention: c_1 most significant, t least significant, so the example places t on qubit 0, c_2 on qubit 1, c_1 on qubit 2.
- Total register size may exceed 3 (up to 12); additional qubits are idle spectators to allow embedding the gate in a larger register.
- The 'single_shot' implementation is the logical CCX gate; no claim is made about pulse-level realisation.
- The decomposed variant is the standard Nielsen-Chuang Clifford+T Toffoli circuit, exactly equal to CCX including phases.

## Unresolved issues

- The paper's actual transmon Hamiltonian, control pulses, gate time, fidelity definition and Differential-Evolution enhancements remain unknown and are not represented in the circuit.
- Truth-table verification of the eight basis states checks only the permutation action, not relative phases or the 99.9% process-level fidelity claimed in the abstract.

## Equation mapping

- `eq_1`: implemented; _toffoli_single_shot (qc.ccx) and module/function docstrings; layout t->q0, c_2->q1, c_1->q2 in example. The CCX gate realises |c1 c2 t> -> |c1, c2, t XOR (c1 AND c2)> exactly; with c_1 on the highest-index qubit and t on qubit 0 the integer encoding x = 4c_1 + 2c_2 + t of the spec is reproduced.
- `eq_2`: implemented; _toffoli_decomposed (H/T/Tdg/CX sequence) and _toffoli_single_shot; selected by instance['implementation']. The operator I - |11><11| (x) (I - X) is realised either as a single CCX or as the standard phase-exact Clifford+T decomposition, which equals CCX as a unitary (no relative phases).
- `eq_3`: out_of_scope; no code location. Time-ordered propagator of a pulse-level transmon Hamiltonian; requires the unknown Hamiltonian and controls and is not a gate-level Qiskit operation.
- `eq_4`: out_of_scope; no code location. Assumed Duffing-transmon chain Hamiltonian; parameter values and drives are unknown and multi-level dynamics cannot be built from standard qubit gates without dense unitaries.
- `eq_5`: out_of_scope; no code location. Gate-fidelity functional is a classical post-processing/verification quantity, not part of the returned operation; the module must not include reference or test code.
- `eq_6`: out_of_scope; no code location. Differential-Evolution control optimisation is a classical search over unknown pulse parameters; not reconstructible from the abstract and not a circuit.

## Specification changes

- eq_1, eq_2: Scope narrowed to the ideal logical Toffoli unitary only; the 'single_shot' option is a single CCX gate at the gate level, not a pulse-level single-shot implementation. Reason: The abstract provides no Hamiltonian, pulse parametrisation, or optimiser details, so only the target gate (eq_1/eq_2) can be implemented faithfully.
- eq_1: Mapped the spec's bit-string convention (c_1 most significant, x = 4c_1 + 2c_2 + t) onto Qiskit's little-endian indexing by placing t on qubit 0, c_2 on qubit 1, c_1 on qubit 2 in the example instance; indices are user-configurable. Reason: Qiskit qubit 0 is the least significant computational-basis bit, so the spec's ordering must be reversed in physical index to preserve the integer labels x=6 and x=7 as the swapped states.
- eq_2: Added an optional 'decomposed' realisation using the standard 15-gate H/T/Tdg/CX Toffoli decomposition as a sequential baseline. Reason: The abstract contrasts single-shot with decomposed implementations; the decomposition is exactly equal to CCX as a unitary and uses only standard gates.
- eq_3, eq_4, eq_5, eq_6: Not implemented. Reason: Essential details (Hamiltonian parameters, controls, fidelity definition, optimiser) are missing from the abstract; implementing them would require fabrication or dense unitaries.
