# Equation to Qiskit

build_circuit(instance) returns the second-order (symmetric) Trotter product formula S_2(t/r)^r for a Pauli-sum Hamiltonian H = sum_j c_j P_j supplied in the instance. Each term exp(-i c_j P_j dt/2) is built from basis changes, a CX parity ladder, an Rz and the uncompute. There is no state preparation or measurement. The commutator bound, coalescing and scaling fits are not implemented.

Source equation run: `5a91ddbe-11b2-4a1f-9ddd-22473c2cad85`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register of N qubits (N = num_qubits, 4 in the example).
- Qubit i is spin orbital i under Jordan-Wigner; qubit 0 is the least significant bit.
- Pauli string character at position i acts on qubit i, so the string 'ZIII' is Z on qubit 0.
- No ancilla qubits.

## Assumptions

- Jordan-Wigner qubit i corresponds to orbital i, little-endian.
- The term order is fixed as given in the instance list.
- The same step size dt = t/r is used for all terms.
- Caps: at most 12 qubits, 200 steps, 200 terms, and 20000 total rotations (r * 2 * number of terms).

## Unresolved issues

- The paper's alternative simulation scheme is not known and is not implemented.
- The coalescing grouping rule and the choice of r_k are unspecified.
- The exact constants of the commutator error bound are unavailable.
- No molecular integrals are given, so the example coefficients are illustrative, H2-like and not derived from integrals.

## Equation mapping

- `eq_1`: background; build_circuit (terms input). The Jordan-Wigner Pauli decomposition is done classically by the caller. The instance supplies (c_j, P_j) directly, and no fermionic integrals are processed in the module.
- `eq_2`: implemented; build_circuit and _pauli_rotation. Implements S_2(t/r)^r. Each repetition applies the half-step rotations in order j=1..L and then j=L..1. Each rotation is a basis change, a CX ladder onto the last support qubit, Rz(c_j*dt), and the uncompute.
- `eq_3`: out_of_scope; no code location. The commutator-norm error bound is a classical calculation and not part of the circuit operation. The module only takes the step count r as input.
- `eq_4`: out_of_scope; no code location. The coalesced multi-rate formula is not implemented. Its grouping rule and interleaving are unspecified in the abstract and the specification.
- `eq_5`: out_of_scope; no code location. The scaling-exponent fit is a classical analysis across molecule families and not a circuit.

## Specification changes

- eq_2: Scoped to the uniform-step second-order Trotter circuit for caller-supplied Pauli terms, with an explicit string-position convention (character i acts on qubit i). The identity term is a global phase, and the circuit's global_phase is set so that it matches exp(-iHt) up to the Trotter error. Reason: This gives a well-defined unitary operation. The ordering of the product notation is irrelevant because the formula is palindromic.
- eq_1: The integral-to-Pauli Jordan-Wigner transformation is not implemented. The Pauli sum is the input. Reason: The molecule family and integrals are not specified, so the Hamiltonian is supplied by the instance.
- eq_3, eq_4, eq_5: Narrowed scope: error bound, coalescing and scaling fit are excluded from the circuit. Reason: They are classical analyses or have unspecified details, and so cannot be reconstructed faithfully.
